# an earlier experiment; still pretty interesting

import time
import numm
import numpy as np

last = None

def video_in(a):
    global last
    last = a

def rect_set(a, x, dx, y, dy, b):
    a[np.clip(x,0,a.shape[0]-1):np.clip(x+dx,0,a.shape[0]-1),
      np.clip(y,0,a.shape[1]-1):np.clip(y+dy,0,a.shape[1]-1), :] = b

def rect_get(a, x, dx, y, dy):
    return a[np.clip(x,0,a.shape[0]-1):np.clip(x+dx,0,a.shape[0]-1),
             np.clip(y,0,a.shape[1]-1):np.clip(y+dy,0,a.shape[1]-1), :]

def rect_apply(a, x, dx, y, dy, f):
    rect_set(a, x, dx, y, dy, f(rect_get(a, x, dx, y, dy)))

def sawtooth(x):
    return float(0 if (x%2)<1 else 1)

buff = np.zeros((240,320,3), np.uint8)

def video_out(a):
    new = np.zeros((240,320,3), np.uint8)
    #new[:] = (100+100*np.cos(time.time()/2),100+100*np.sin(time.time()/3),255)
    #new[:] = last
    def cube_root(a):
        return np.sign(a)*(abs(a)**(1.4))
    def sigmoid(a):
        return (cube_root(2*a-1)+1)/2
    retime = (time.time()-last_press)/period
    o=sigmoid(retime%1)
    if (retime%2)<1 : o = 1-o
    for i in range(-2,6):
        for j in range(-2,6):
            x=100*(i-sawtooth(retime)/2+np.sin(retime*np.pi/2))
            y=100*(j-sawtooth(retime)/2+np.cos(retime*np.pi/2))
            rect_apply(new, 10+x, 25, 10+y+50*o, 25, lambda x: 255-x)
            rect_apply(new, 10+x+50*o, 25, 60+y, 25, lambda x: 255-x)
            rect_apply(new, 60+x, 25, 60+y-50*o, 25, lambda x: 255-x)
            rect_apply(new, 60+x-50*o, 25, 10+y, 25, lambda x: 255-x)

    global buff
    buff = buff*0.5 + new*0.5
    a[:] = buff

period = 1
last_press = 0
def keyboard_in(type, key):
    if type == 'key-press':
        global period, last_press
        now = time.time()
        print now-last_press
        if now - last_press < 2:
            period = (period + (now - last_press))/2
            print period
        last_press = now

if __name__ == '__main__':
    numm.run(**globals())
