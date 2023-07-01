def remote_bot(i18):
    import sys, telepot, time, os, subprocess
    from telepot.namedtuple import ReplyKeyboardMarkup

    # Get current system language
    lang_request = subprocess.check_output(['osascript', '-e', 'user locale of (get system info)'], text = True)

    if lang_request.startswith('ru'):
        lang = 'ru'
    else:
        lang = 'en'

    # list of commands
    cmd_play_prev = '⏮ ' + i18[lang]['play_prev']
    cmd_play_pause = '⏯ ' + i18[lang]['play_pause']
    cmd_play_next = '⏭ ' + i18[lang]['play_next']
    cmd_volume_down = '🔽 ' + i18[lang]['volume_down']
    cmd_volume_mute = '🔈 ' + i18[lang]['volume_mute']
    cmd_volume_up = '🔼 ' + i18[lang]['volume_up']
    cmd_screen_off = '🖥 ' + i18[lang]['screen_off']
    cmd_brightness_down = '🔅 ' + i18[lang]['brightness'] + ' -'
    cmd_brightness_up = '🔅 ' + i18[lang]['brightness'] + ' +'
    cmd_sleep = '🟡 ' + i18[lang]['sleep']
    cmd_reboot = '🟠 ' + i18[lang]['reboot']
    cmd_shutdown = '🔴 ' + i18[lang]['shutdown']

    # bot logic
    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if (content_type == 'text' and chat_id and msg['chat']['id'] == chat_id):
            command = msg['text']

            # telegram keyboard markup
            markup = ReplyKeyboardMarkup(keyboard=[
                [cmd_play_prev, cmd_play_pause, cmd_play_next],
                [cmd_volume_down, cmd_volume_mute, cmd_volume_up],
                [cmd_screen_off, cmd_brightness_down, cmd_brightness_up],
                [cmd_sleep, cmd_reboot, cmd_shutdown],
            ])

            if command == '/start':
                bot.sendMessage (chat_id, str("Добро пожаловать!"), reply_markup=markup)

            elif cmd_play_prev == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_next_song"
                    end tell'
                ''')

            elif cmd_play_pause == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_play_pause"
                    end tell'
                ''')

            elif cmd_play_next == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_prev_song"
                    end tell'
                ''')

            elif cmd_volume_down == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_volume_down"
                    end tell'
                ''')

            elif cmd_volume_mute == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_mute"
                    end tell'
                ''')

            elif cmd_volume_up == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_volume_up"
                    end tell'
                ''')

            elif cmd_screen_off == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_display_off"
                    end tell'
                ''')

            elif cmd_brightness_down == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_brightness_down"
                    end tell'
                ''')

            elif cmd_brightness_up == command:
                os.system('''
                    osascript -e 'tell application "BetterTouchTool"
                        trigger_named "rmt_brightness_up"
                    end tell'
                ''')

            elif cmd_sleep == command:
                os.system('''
                    osascript -e 'tell application "System Events" to sleep'
                ''')

            elif cmd_reboot == command:
                os.system('''
                    osascript -e 'tell application "System Events" to restart'
                ''')

            elif cmd_shutdown == command:
                os.system('''
                    osascript -e 'tell application "System Events" to shut down'
                ''')

            bot.sendMessage(chat_id, 'Команда: %s' % command, reply_markup=markup)

    # get settings from command-line
    TOKEN = sys.argv[1]

    if len(sys.argv) > 2:
        chat_id = sys.argv[2]
    else:
        chat_id = None

    bot = telepot.Bot(TOKEN)

    bot.message_loop(handle)

    while 1:
        time.sleep(20)
