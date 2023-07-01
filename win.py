def remote_bot():
    import sys, telepot, time, subprocess, os, psutil
    from telepot.namedtuple import ReplyKeyboardMarkup

    cmd_play_prev = '⏮ Назад'
    cmd_play_pause = '⏯ Играть/Пауза'
    cmd_play_next = '⏭ Далее'
    cmd_volume_down = '⏭ Далее'
    cmd_volume_mute = '🔈 Звук'
    cmd_volume_up = '🔼 Громче'
    cmd_screen_off = '🖥 Выключить экран'
    cmd_brightness_10 = '🔅 Яркость 10%'
    cmd_brightness_100 = '🔅 Яркость 100%'
    cmd_hibernate = '🟡 Гибернация'
    cmd_reboot = '🟠 Перезагрузка'
    cmd_shutdown = '🔴 Выключение'

    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if (content_type == 'text' and chat_id and msg['chat']['id'] == chat_id):
            cmd_repeat = 1
            command = msg['text']
            markup = ReplyKeyboardMarkup(keyboard=[
                [cmd_play_prev, cmd_play_pause, cmd_play_next],
                [cmd_volume_down, cmd_volume_mute, cmd_volume_up],
                [cmd_screen_off, cmd_brightness_10, cmd_brightness_100],
                [cmd_hibernate, cmd_reboot, cmd_shutdown],
            ])

            if command == '/start':
                bot.sendMessage (chat_id, str("Добро пожаловать!"), reply_markup=markup)

            elif cmd_play_prev == command:
                cmd = keypress % '0xB0'

            elif cmd_play_pause == command:
                cmd = keypress % '0xB3'

            elif cmd_play_prev == command:
                cmd = keypress % '0xB1'

            elif cmd_volume_up == command:
                cmd = keypress % '0xAF'
                cmd_repeat = 2

            elif cmd_volume_mute == command:
                cmd = keypress % '0xAD'

            elif cmd_volume_down == command:
                cmd = keypress % '0xAE'
                cmd_repeat = 2

            elif cmd_screen_off == command:
                cmd = screen_off

            elif cmd_brightness_10 == command:
                cmd = brightness % 10

            elif cmd_brightness_100 == command:
                cmd = brightness % 100

            elif cmd_hibernate == command:
                cmd = 'shutdown.exe /h /f'

            elif cmd_reboot == command:
                cmd = 'shutdown /r /f'

            elif cmd_shutdown == command:
                cmd = 'shutdown /s /f /t 0'

            else:
                cmd_repeat = None

            if cmd_repeat:
                for number in range(cmd_repeat):
                    subprocess.Popen(cmd, shell=True)

            bot.sendMessage(chat_id, 'Команда: %s' % command, reply_markup=markup)

    # get settings from command-line
    TOKEN = sys.argv[1]

    if len(sys.argv) > 2:
        chat_id = sys.argv[2]
    else:
        chat_id = None

    bot = telepot.Bot(TOKEN)

    path = os.path.dirname(os.path.abspath(__file__))
    screen_off = 'powershell ' + path + '\screen_off.ps1'
    keypress = 'powershell ' + path + '\keypress.ps1 -KeyCode %s'
    brightness = 'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(0,%d)'

    bot.message_loop(handle)

    while 1:
        time.sleep(20)
