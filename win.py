import logging
import os
import subprocess

from telegram import ReplyKeyboardMarkup

from bot_base import make_label, run_bot

logger = logging.getLogger(__name__)


def remote_bot(i18, icons, token, chat_id):
    p = subprocess.run(
        ["powershell.exe", "-NoProfile", "Get-UICulture|select -ExpandProperty Name"],
        capture_output=True, text=True
    )
    lang = 'ru' if p.stdout.startswith('ru') else 'en'

    scripts_path = os.path.dirname(os.path.abspath(__file__))
    screen_off = 'powershell ' + scripts_path + r'\scripts\win\screen_off.ps1'
    keypress   = 'powershell ' + scripts_path + r'\scripts\win\keypress.ps1 -KeyCode %s'
    brightness = 'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(0,%d)'

    def run(cmd, repeat=1):
        for _ in range(repeat):
            subprocess.Popen(cmd, shell=True)

    label = make_label(icons, i18[lang])

    commands = {
        label('play_prev'):          lambda: run(keypress % '0xB1'),
        label('play_pause'):         lambda: run(keypress % '0xB3'),
        label('play_next'):          lambda: run(keypress % '0xB0'),
        label('volume_down'):        lambda: run(keypress % '0xAE', 2),
        label('volume_mute'):        lambda: run(keypress % '0xAD'),
        label('volume_up'):          lambda: run(keypress % '0xAF', 2),
        label('screen_off'):         lambda: run(screen_off),
        label('brightness', ' 10'):  lambda: run(brightness % 10),
        label('brightness', ' 100'): lambda: run(brightness % 100),
        label('hibernate'):          lambda: run('shutdown.exe /h /f'),
        label('reboot'):             lambda: run('shutdown /r /f'),
        label('shutdown'):           lambda: run('shutdown /s /f /t 0'),
    }

    keyboard = ReplyKeyboardMarkup([
        [label('play_prev'),   label('play_pause'),       label('play_next')],
        [label('volume_down'), label('volume_mute'),       label('volume_up')],
        [label('screen_off'),  label('brightness', ' 10'), label('brightness', ' 100')],
        [label('hibernate'),   label('reboot'),            label('shutdown')],
    ], resize_keyboard=True)

    run_bot(token, chat_id, keyboard, commands)
