### MacOS / Windows / Linux remote control Telegram bot ###

## List of controls:
- Play previous song
- Play/Pause
- Play next song
- Volume down
- Mute / Unmute
- Volume up
- Disable screen
- Mac: Display brightness down, Win: Set brightness to 10%
- Mac: Display brightness up, Win: Set brightness to 100%
- Mac: Sleep, Win: Hibernate
- Reboot
- Shutdown

## Windows install steps:
1. Install [Python](https://www.python.org/downloads/)
2. Start powershell as administrator and run `py -m pip install python-telegram-bot psutil`
3. Create your [Telegram bot](https://core.telegram.org/bots)
4. Clone this repository to your user dir `C:\Users\<username>\RemoteControlBot`
5. Run cmd (Win+R) and enter `shell:common startup`. In the folder that opens, create a `RemoteControlBot.bat` file with content:
   ```
   powershell pythonw {DIR}\run.py '{TOKEN}' '{CHAT_ID}'
   ```
6. If you are using Windows 10, start powershell as administrator and run:
   ```
   Set-ExecutionPolicy unrestricted
   ```
7. Double click `RemoteControlBot.bat` to start the bot
8. Send message `/start` to your bot

## MacOS install steps:

### Dependencies
- [nowplaying-cli](https://github.com/kirtan-mehta/nowplaying-cli) — media control (play/pause, next, previous) via macOS MediaRemote API

### Install

1. Install dependencies:
   ```
   brew install python nowplaying-cli
   ```

2. Install Python package:
   ```
   pip3 install python-telegram-bot --break-system-packages
   ```

3. Clone this repository:
   ```
   git clone https://github.com/your-username/RemoteControlBot ~/RemoteControlBot
   ```

4. Create your [Telegram bot](https://core.telegram.org/bots) and get the token and your chat_id.

5. Set up autostart via Automator:
   - Open Automator.app
   - Select **Application**
   - Click **Show library** in the toolbar (if hidden)
   - Add **Run shell script** (from Actions/Utilities)
   - Paste the following script:
     ```
     source ~/.zprofile
     python3 ~/RemoteControlBot/run.py '{TOKEN}' '{CHAT_ID}'
     ```
   - Save as `RemoteControlBot.app` (e.g. in your home folder)

6. Add the app to login items:
   - Go to **System Settings -> General -> Login items**
   - Add `RemoteControlBot.app`

7. Reboot and send `/start` to your bot.

## Linux install steps (Ubuntu / Debian):

### Dependencies
- **playerctl** — media control via MPRIS
- **brightnessctl** — display brightness
- **pactl** — volume control (pre-installed with PulseAudio/PipeWire)
- **systemctl** — sleep/reboot/shutdown (pre-installed)

### Install

1. Install dependencies:
   ```
   sudo apt install playerctl brightnessctl
   ```

2. Install Python and the required package:
   ```
   sudo apt install python3 python3-pip
   pip3 install python-telegram-bot psutil --break-system-packages
   ```

3. Clone this repository:
   ```
   git clone https://github.com/your-username/RemoteControlBot ~/RemoteControlBot
   ```

4. Create your [Telegram bot](https://core.telegram.org/bots) and get the token and your chat_id.

5. Set up autostart via systemd user service:
   ```
   mkdir -p ~/.config/systemd/user
   ```
   Create `~/.config/systemd/user/remotecontrolbot.service`:
   ```ini
   [Unit]
   Description=RemoteControlBot

   [Service]
   ExecStart=python3 %h/RemoteControlBot/run.py '{TOKEN}' '{CHAT_ID}'
   Restart=on-failure

   [Install]
   WantedBy=default.target
   ```
   Then enable and start:
   ```
   systemctl --user enable remotecontrolbot
   systemctl --user start remotecontrolbot
   ```

6. Send `/start` to your bot.

> **Note:** Display off uses `xset dpms force off` on X11 and falls back to D-Bus ScreenSaver on Wayland.

Where:
- `{TOKEN}` — your Telegram bot token
- `{CHAT_ID}` — your Telegram account chat_id (required to restrict access to the bot)
- `{DIR}` — folder with RemoteControlBot files (Windows only)
