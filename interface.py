import serial
import time
from datetime import datetime as dt


ser = serial.Serial("COM5", 115200, timeout=0)

modes = ['clock', 'select', 'track', 'cancel']
actions = ['UP', 'DOWN', 'ESC', 'OKAY']
mode = modes[0]


while True:
    if ser.in_waiting:
        s = ser.readline().decode().strip()
        if s == "" or s not in modes + actions + ["mode"]:
            continue
        print(s, mode, s in actions)

        if mode == 'clock' and s in actions:
            mode = 'select'
            continue

        elif mode == 'select' and s in actions:
            if s == "ESC":
                mode = 'clock'
            elif s == "OKAY":
                mode = 'track'
            continue

        elif mode == 'track' and s in actions:
            if s == "OKAY":
                mode = 'cancel'
            continue

        elif mode == 'cancel' and s in actions:
            if s == "OKAY":
                mode = 'clock'
            elif s == "ESC":
                mode = 'track'
            continue


        elif s == "echo":
            ser.write('{}\r\n'.format(s).encode())
        elif s == "clock":
            n = dt.now()
            ser.write('{}{}{}\r\n'.format(n.strftime("%H"),
                                          ":" if n.second % 2 == 0 else " ",
                                          n.strftime("%M")).encode())
        elif s == "select":
            pass
        elif s == "track":
            pass
        elif s == "cancel":
            pass
        elif s == "mode":
            ser.write('{}\r\n'.format(modes.index(mode)).encode())
    else:
        time.sleep(0.1)
