import sys, telepot, time, os
from telepot.namedtuple import ReplyKeyboardMarkup

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if (content_type == 'text' and chat_id and msg['chat']['id'] == chat_id):
        response = None
        command = msg['text']
        markup = ReplyKeyboardMarkup(keyboard=[
            ['⏮ Назад', '⏯ Играть/Пауза', '⏭ Далее'],
            ['🔽 Тише', '🔈 Звук', '🔼 Громче'],
            ['🖥 Выключить экран', '🔅 Яркость -', '🔆 Яркость +'],
            ['🟡 Сон', '🟠 Перезагрузка', '🔴 Выключение'],
        ])

        if command == '/start':
            bot.sendMessage (chat_id, str("Добро пожаловать!"), reply_markup=markup)

        elif '🔴 Выключение' == command:
            os.system('''
                osascript -e 'tell application "System Events" to shut down'
            ''')
            response = "Компьютер сейчас будет выключен"

        elif '🟠 Перезагрузка' == command:
            os.system('''
                osascript -e 'tell application "System Events" to restart'
            ''')
            response = "Компьютер сейчас будет перезагружен"

        elif '🟡 Сон' == command:
            os.system('''
                osascript -e 'tell application "System Events" to sleep'
            ''')

        elif '🔅 Яркость -' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_brightness_down"
                end tell'
            ''')

        elif  '🔆 Яркость +' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_brightness_up"
                end tell'
            ''')

        elif  '🖥 Выключить экран' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_display_off"
                end tell'
            ''')

        elif  '🔈 Звук' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_mute"
                end tell'
            ''')

        elif  '🔼 Громче' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_volume_up"
                end tell'
            ''')

        elif  '🔽 Тише' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_volume_down"
                end tell'
            ''')

        elif  '⏭ Далее' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_next_song"
                end tell'
            ''')

        elif  '⏮ Назад' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_prev_song"
                end tell'
            ''')

        elif  '⏯ Играть/Пауза' == command:
            os.system('''
                osascript -e 'tell application "BetterTouchTool"
                    trigger_named "rmt_play_pause"
                end tell'
            ''')

        if response:
            bot.sendMessage(chat_id, response, reply_markup=markup)
        else:
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
