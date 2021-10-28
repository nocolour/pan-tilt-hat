
from time import sleep,strftime,localtime
from vilib import Vilib
from sunfounder_io import PWM,Servo,I2C

import sys
import tty
import termios

# region  read keyboard 
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

manual = '''
Press keys on keyboard to record value!
    W: up
    A: left
    S: right
    D: down
    Q: record/pause/continue
    E: stop

    G: Quit
'''
# endregion

# region init
I2C().reset_mcu()
sleep(0.01)

pan = Servo(PWM("P1"))
tilt = Servo(PWM("P0"))
panAngle = 0
tiltAngle = 0
pan.angle(0)
tilt.angle(0)

Vilib.rec_video_set["path"] = "/home/pi/video/"
vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
Vilib.rec_video_set["name"] = vname

rec_flag = 'stop' # start,pause,stop
# endregion init

# rec control
def rec_control(key):
    global rec_flag
    
    if key == 'q' and rec_flag == 'stop':
        key = None
        rec_flag = 'start'
        Vilib.rec_video_run()
        print('rec start ...')
    if key == 'q' and rec_flag == 'start':
        key = None
        rec_flag = 'pause'
        Vilib.rec_video_pause()
        print('pause')
    if key == 'q' and rec_flag == 'pause':
        key = None
        rec_flag = 'start'
        Vilib.rec_video_start()
        print('continue')    

    if key == 'e' and rec_flag != 'stop':
        Vilib.rec_video_stop()
        print('stop')
        print("The video saved as %s%s.avi"%(Vilib.rec_video_set["path"],vname))  

# region servo control
def limit(x,min,max):
    if x > max:
        return max
    elif x < min:
        return min
    else:
        return x

def servo_control(key):
    global panAngle,tiltAngle       
    if key == 'w':
        tiltAngle -= 1
        tiltAngle = limit(tiltAngle, -90, 90)
        tilt.angle(tiltAngle)
    if key == 's':
        tiltAngle += 1
        tiltAngle = limit(tiltAngle, -90, 90)
        tilt.angle(tiltAngle)
    if key == 'a':
        panAngle += 1
        panAngle = limit(panAngle, -90, 90)
        pan.angle(panAngle)
    if key == 'd':
        panAngle -= 1
        panAngle = limit(panAngle, -90, 90)
        pan.angle(panAngle)

# endregion servo control


def main():

    Vilib.camera_start(inverted_flag=True)
    Vilib.display(local=True,web=True)

    print(manual)
    while True:
        key = readchar()
        # rec control
        rec_control(key)
        # servo control
        servo_control(key)
        # esc
        if key == 'g':
            Vilib.camera_close()
            break 

        sleep(0.1)

if __name__ == "__main__":
    main()