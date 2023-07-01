import sys, telepot, time, subprocess, os, psutil
from telepot.namedtuple import ReplyKeyboardMarkup

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if (content_type == 'text' and chat_id and msg['chat']['id'] == chat_id):
        cmd_repeat = 1
        response = None
        command = msg['text']
        markup = ReplyKeyboardMarkup(keyboard=[
            ['⏮ Назад', '⏯ Играть/Пауза', '⏭ Далее'],
            ['🔽 Тише', '🔈 Звук', '🔼 Громче'],
            ['🖥 Выключить экран', '🔅 Яркость 10%', '🔆 Яркость 100%'],
            ['🟡 Гибернация', '🟠 Перезагрузка', '🔴 Выключение'],
        ])

        if command == '/start':
            bot.sendMessage (chat_id, str("Добро пожаловать!"), reply_markup=markup)

        elif '🔴 Выключение' == command:
            cmd = 'shutdown /s /f /t 0'
            response = "Компьютер сейчас будет выключен"

        elif '🟠 Перезагрузка' == command:
            cmd = 'shutdown /r /f'
            response = "Компьютер сейчас будет перезагружен"

        elif '🟡 Гибернация' == command:
            cmd = 'shutdown.exe /h /f'
            response = "Компьютер сейчас уйдет в гибернацию"

        elif '🔅 Яркость 10%' == command:
            cmd = brightness % 10

        elif  '🔆 Яркость 100%' == command:
            cmd = brightness % 100

        elif  '🖥 Выключить экран' == command:
            cmd = screen_off

        elif  '🔈 Звук' == command:
            cmd = keypress % '0xAD'

        elif  '🔼 Громче' == command:
            cmd = keypress % '0xAF'
            cmd_repeat = 2

        elif  '🔽 Тише' == command:
            cmd = keypress % '0xAE'
            cmd_repeat = 2

        elif  '⏭ Далее' == command:
            cmd = keypress % '0xB0'

        elif  '⏮ Назад' == command:
            cmd = keypress % '0xB1'

        elif  '⏯ Играть/Пауза' == command:
            cmd = keypress % '0xB3'

        else:
            cmd_repeat = None

        if cmd_repeat:
            for number in range(cmd_repeat):
                subprocess.Popen(cmd, shell=True)

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

path = os.path.dirname(os.path.abspath(__file__))
screen_off = 'powershell ' + path + '\screen_off.ps1'
keypress = 'powershell ' + path + '\keypress.ps1 -KeyCode %s'
brightness = 'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(0,%d)'

bot.message_loop(handle)

while 1:
    time.sleep(20)
