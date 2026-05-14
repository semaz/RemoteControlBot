import logging
import os
import subprocess

from telegram import ReplyKeyboardMarkup

from bot_base import make_label, run_bot

logger = logging.getLogger(__name__)


def remote_bot(i18, icons, token, chat_id):
    def shell(cmd):
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error('%s: %s', cmd[0], result.stderr.strip())
        return result.returncode

    def media(action):
        shell(['playerctl', action])

    def volume_up():
        shell(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+10%'])

    def volume_down():
        shell(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-10%'])

    def volume_mute():
        shell(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle'])

    def brightness_up():
        shell(['brightnessctl', 'set', '+10%'])

    def brightness_down():
        shell(['brightnessctl', 'set', '10%-'])

    def display_off():
        # X11
        if shell(['xset', 'dpms', 'force', 'off']) != 0:
            # Wayland fallback: freedesktop ScreenSaver D-Bus (GNOME, KDE, и др.)
            shell([
                'gdbus', 'call', '--session',
                '--dest', 'org.freedesktop.ScreenSaver',
                '--object-path', '/ScreenSaver',
                '--method', 'org.freedesktop.ScreenSaver.SetActive', 'true',
            ])

    lang = 'ru' if os.environ.get('LANG', '').startswith('ru') else 'en'

    label = make_label(icons, i18[lang])

    commands = {
        label('play_prev'):         lambda: media('previous'),
        label('play_pause'):        lambda: media('play-pause'),
        label('play_next'):         lambda: media('next'),
        label('volume_down'):       volume_down,
        label('volume_mute'):       volume_mute,
        label('volume_up'):         volume_up,
        label('screen_off'):        display_off,
        label('brightness', ' -'):  brightness_down,
        label('brightness', ' +'):  brightness_up,
        label('sleep'):             lambda: shell(['systemctl', 'suspend']),
        label('reboot'):            lambda: shell(['systemctl', 'reboot']),
        label('shutdown'):          lambda: shell(['systemctl', 'poweroff']),
    }

    keyboard = ReplyKeyboardMarkup([
        [label('play_prev'),   label('play_pause'),      label('play_next')],
        [label('volume_down'), label('volume_mute'),      label('volume_up')],
        [label('screen_off'),  label('brightness', ' -'), label('brightness', ' +')],
        [label('sleep'),       label('reboot'),           label('shutdown')],
    ], resize_keyboard=True)

    run_bot(token, chat_id, keyboard, commands)
