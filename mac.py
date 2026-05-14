import ctypes
import logging
import subprocess

from telegram import ReplyKeyboardMarkup

from bot_base import make_label, run_bot

logger = logging.getLogger(__name__)


def remote_bot(i18, icons, token, chat_id):
    def osascript(script):
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error('osascript: %s', result.stderr.strip())

    def media(action):
        result = subprocess.run(['nowplaying-cli', action], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error('nowplaying-cli: %s', result.stderr.strip())

    def brightness_change(delta):
        try:
            cg = ctypes.cdll.LoadLibrary(
                '/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics'
            )
            cg.CGMainDisplayID.restype = ctypes.c_uint32
            display_id = cg.CGMainDisplayID()

            try:
                # macOS 13+: DisplayServices заменил CoreDisplay
                ds = ctypes.cdll.LoadLibrary(
                    '/System/Library/PrivateFrameworks/DisplayServices.framework/DisplayServices'
                )
                get = ds.DisplayServicesGetBrightness
                get.restype = ctypes.c_int
                get.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_float)]
                set_ = ds.DisplayServicesSetBrightness
                set_.restype = ctypes.c_int
                set_.argtypes = [ctypes.c_uint32, ctypes.c_float]

                current = ctypes.c_float()
                get(display_id, ctypes.byref(current))
                set_(display_id, ctypes.c_float(max(0.0, min(1.0, current.value + delta))))
            except OSError:
                # macOS 12 и старше: CoreDisplay
                cd = ctypes.cdll.LoadLibrary(
                    '/System/Library/PrivateFrameworks/CoreDisplay.framework/CoreDisplay'
                )
                get = cd.CoreDisplay_Display_GetUserBrightness
                get.restype = ctypes.c_double
                get.argtypes = [ctypes.c_uint32]
                set_ = cd.CoreDisplay_Display_SetUserBrightness
                set_.restype = None
                set_.argtypes = [ctypes.c_uint32, ctypes.c_double]

                current = get(display_id)
                set_(display_id, max(0.0, min(1.0, current + delta)))
        except Exception as e:
            logger.error('brightness: %s', e)

    def volume_up():
        osascript(
            'set vol to (output volume of (get volume settings)) + 10\n'
            'if vol > 100 then set vol to 100\n'
            'set volume output volume vol'
        )

    def volume_down():
        osascript(
            'set vol to (output volume of (get volume settings)) - 10\n'
            'if vol < 0 then set vol to 0\n'
            'set volume output volume vol'
        )

    def volume_mute():
        osascript(
            'set s to (get volume settings)\n'
            'if output muted of s then\n'
            '    set volume without output muted\n'
            'else\n'
            '    set volume with output muted\n'
            'end if'
        )

    def display_off():
        subprocess.run(['pmset', 'displaysleepnow'])

    lang_request = subprocess.check_output(
        ['osascript', '-e', 'user locale of (get system info)'], text=True
    )
    lang = 'ru' if lang_request.startswith('ru') else 'en'

    label = make_label(icons, i18[lang])

    commands = {
        label('play_prev'):         lambda: media('previous'),
        label('play_pause'):        lambda: media('togglePlayPause'),
        label('play_next'):         lambda: media('next'),
        label('volume_down'):       volume_down,
        label('volume_mute'):       volume_mute,
        label('volume_up'):         volume_up,
        label('screen_off'):        display_off,
        label('brightness', ' -'):  lambda: brightness_change(-0.1),
        label('brightness', ' +'):  lambda: brightness_change(0.1),
        label('sleep'):             lambda: osascript('tell application "System Events" to sleep'),
        label('reboot'):            lambda: osascript('tell application "System Events" to restart'),
        label('shutdown'):          lambda: osascript('tell application "System Events" to shut down'),
    }

    keyboard = ReplyKeyboardMarkup([
        [label('play_prev'),   label('play_pause'),      label('play_next')],
        [label('volume_down'), label('volume_mute'),      label('volume_up')],
        [label('screen_off'),  label('brightness', ' -'), label('brightness', ' +')],
        [label('sleep'),       label('reboot'),           label('shutdown')],
    ], resize_keyboard=True)

    run_bot(token, chat_id, keyboard, commands)
