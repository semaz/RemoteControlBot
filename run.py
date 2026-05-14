import platform
import sys

i18 = {
    'ru': {
        'play_prev':   'Назад',
        'play_pause':  'Играть/Пауза',
        'play_next':   'Далее',
        'volume_down': 'Тише',
        'volume_mute': 'Звук',
        'volume_up':   'Громче',
        'screen_off':  'Выключить экран',
        'brightness':  'Яркость',
        'hibernate':   'Гибернация',
        'sleep':       'Сон',
        'reboot':      'Перезагрузка',
        'shutdown':    'Выключение',
    },
    'en': {
        'play_prev':   'Prev',
        'play_pause':  'Play/Pause',
        'play_next':   'Next',
        'volume_down': 'Volume Down',
        'volume_mute': 'Mute',
        'volume_up':   'Volume Up',
        'screen_off':  'Screen Off',
        'brightness':  'Brightness',
        'hibernate':   'Hibernation',
        'sleep':       'Sleep',
        'reboot':      'Restart',
        'shutdown':    'Shutdown',
    },
}

icons = {
    'play_prev':   '⏮',
    'play_pause':  '⏯',
    'play_next':   '⏭',
    'volume_down': '🔽',
    'volume_mute': '🔈',
    'volume_up':   '🔼',
    'screen_off':  '🖥',
    'brightness':  '🔅',
    'sleep':       '🟡',
    'hibernate':   '🟡',
    'reboot':      '🟠',
    'shutdown':    '🔴',
}

if len(sys.argv) < 3:
    sys.exit('Usage: run.py <TOKEN> <CHAT_ID>')

token = sys.argv[1]
chat_id = int(sys.argv[2])

if platform.system() == 'Darwin':
    import mac
    mac.remote_bot(i18, icons, token, chat_id)
elif platform.system() == 'Windows':
    import win
    win.remote_bot(i18, icons, token, chat_id)
elif platform.system() == 'Linux':
    import linux
    linux.remote_bot(i18, icons, token, chat_id)
else:
    sys.exit('Error: Unsupported operating system!')
