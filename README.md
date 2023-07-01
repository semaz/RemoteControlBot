### MacOS / Windows remote control bot ###

For Windows:
1. Install [Python](https://www.python.org/downloads/)
2. Start powershell as administrator and run `py -m pip install telepot psutil`
3. Create your [Telegram bot](https://core.telegram.org/bots)
4. Clone this repository to your user dir `C:\Users\<username>\RemoteControlBot`
5. Run cmd (Win+R) and enter `shell:common startup`. In the folder that opens, create a `RemoteControlBot.bat` file with content:
```shell script
powershell pythonw {DIR}\win.py '{TOKEN}}' '{CHAT_ID}}'
```
6. If you are using Windows 10, then you need to start the powershell in administrator mode and run the command
   `Set-ExecutionPolicy unrestricted`
7. Double click `RemoteControlBot.bat` to start script
8. Send message `/start` to your bot

For MacOS:
1. Install Python and BetterTouchTool `brew install python && brew install --cask bettertouchtool && brew install python && pip3 install telepot`
2. Clone this repository to your user dir `~/RemoteControlBot`
3. Open BetterTouchTool and import preset "scripts/mac/RemoteControlBot.bttpreset"
4. Start Automator.app
4. Select Application
5. Click Show library in the toolbar (if hidden)
6. Add Run shell script (from the Actions/Utilities)
7. Copy & paste script into the window:
```shell
source .zprofile
python3 ~/RemoteControlBot/mac.py '{TOKEN}}' '{CHAT_ID}}''{TOKEN}}' '{CHAT_ID}}'
```
8. Save somewhere (for example in your HOME) as RemoteControlBot.app
9. Go to `System Preferences -> GeneralGeneral -> Login items` and add this app
10. Reboot
10. Send message `/start` to your bot

Where:
- {DIR} - folder with RemoteControlBot files
- {TOKEN} - your bot token
- {CHAT_ID} - your Telegram account chat_id (optional param to secure your connection)


