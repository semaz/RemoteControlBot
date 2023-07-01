import platform

if platform.system() == 'Darwin':
  import mac
  mac.remote_bot()
elif platform.system() == 'Windows':
  import win
  win.remote_bot()
else:
  sys.exit('Error: Unsupported operating system!')