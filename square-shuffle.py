# square-shuffle.py
# (joshuah@alum.mit.edu)

# pretty dancing overengineered squares!
# designed to be used in combination with Discovery's track "Osaka Loop Line"
#   (but that's your call)

# [thanks to PAF for letting me hang out during January 2013]

import time

import numm
import numpy as np

import ndraw

icon_swirl = ndraw.string_list_to_array(
    ['11111   1        ',
     '1   1    1   111 ',
     '1   1 11111  111 ',
     '1   1    1   111 ',
     '11111   1        ',
     '                 ',
     '  1           1  ',
     ' 111          1  ',
     '1 1 1       1 1 1',
     '  1          111 ',
     '  1           1  ',
     '                 ',
     '        1        ',
     ' 111   1     111 ',
     ' 111  11111  111 ',
     ' 111   1     111 ',
     '        1        ',])
icon_rows = ndraw.string_list_to_array(
    ['              1  ',
     '               1 ',
     '11111111111111111',
     '               1 ',
     '              1  ',
     '  1              ',
     ' 1               ',
     '11111111111111111',
     ' 1               ',
     '  1              ',
     '              1  ',
     '               1 ',
     '11111111111111111',
     '               1 ',
     '              1  ',])
icon_cols = icon_rows.T
icon_translate = ndraw.string_list_to_array(
    ['        1        ',
     '       111       ',
     '      11111      ',
     '     1111111     ',
     '    111111111    ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',
     '       111       ',])
icon_sit = ndraw.string_list_to_array(
    ['11111111111111111']*25)

buff = np.zeros((240,320,3), np.uint8)

colors = np.random.randint(0,256,size=(100,100,3))

def func_concat(seq):
    seq = list(seq)
    if len(seq) == 1:
        return seq[0]
    else:
        return lambda *x: seq[0](*func_concat(seq[1:])(*x))
class SquareShuffler:
    def __init__(self, perm, icon):
        self.perm = perm
        self.icon = icon
    @classmethod
    def concat(cls, seq):
        return cls(func_concat(p.perm for p in seq),
                   ndraw.hstack((p.icon for p in seq), spacing=1))
def swirl(ni,nj,r):
    def t(i,j):
        a = {(0,0):(0,1), (0,1):(1,0), (1,1):(0,-1), (1,0):(-1,0)}
        b = {(0,0):(1,0), (1,0):(0,1), (1,1):(-1,0), (0,1):(0,-1)}
        di, dj = (a if r else b)[(i+ni)%2, (j+nj)%2]
        return i+di,j+dj
    return SquareShuffler(t, icon_swirl)
def translate(di,dj):
    def t(i,j):
        return i+di,j+dj
    return SquareShuffler(t, icon_translate)
def rows(seq):
    def t(i,j):
        return i, j+seq[i%len(seq)]
    return SquareShuffler(t, icon_rows)
def cols(seq):
    def t(i,j):
        return i+seq[j%len(seq)], j
    return SquareShuffler(t, icon_cols)
def sit():
    def t(i,j):
        return i, j
    return SquareShuffler(t, icon_sit)
def zigzag(ni,nj):
    def t(i,j):
        a = {(0,0):(0,1), (0,1):(1,-1), (1,1):(1,-1), (1,0):(0,1)}
        di, dj = a[(i+ni)%2, (j+nj)%2]
        return i+di,j+dj
    return SquareShuffler(t, icon_sit)

def video_out(a):
    new = np.zeros((240,320,3), np.uint8)
    def root(a):
        return np.sign(a)*(abs(a)**(0.8))
    def sigmoid(a):
        return (root(2*a-1)+1)/2
    retime = (time.time()-last_press)/period
    o = sigmoid(retime%1)
    t = int(retime)

    new[:] = 128+127*np.cos(time.time())

    """
    seq = [cols([-1,1]),
           swirl(0,0,True),
           concat([translate(0,1), swirl(0,1,False)]),
           swirl(1,1,False),
           rows([1,-1]),
           concat([translate(1,0), swirl(0,0,True)]),
           ]
    """
    
    seq = [SquareShuffler.concat([translate(1,0), swirl(0,0,False)]),
           rows([-1,1]),
           SquareShuffler.concat([translate(0,1), swirl(0,1,True)]),
           cols([-1,1]),
           SquareShuffler.concat([translate(-1,0), swirl(1,1,False)]),
           rows([1,-1]),
           swirl(0,0,True),
           cols([1,2]),
           SquareShuffler.concat([translate(0,-1), swirl(1,0,True)]),
           cols([1,-1]),
           swirl(1,1,True),
           rows([1,2])]
    

    cur = seq[t%len(seq)]
    size = 25
    spacing = 50
    
    for i in range(-3,8):
        for j in range(-3,8):
            di, dj = cur.perm(i,j)
            x=spacing*((1-o)*i+o*di)
            y=spacing*((1-o)*j+o*dj)
            ndraw.rect_set(new, 10+x, size, 10+y, size,
                           (1-o)*colors[i,j]+o*colors[di,dj])

    global buff
    # wanna do motion blur?
    # buff = buff*0.5 + new*0.5
    buff = new
    a[:] = buff

    if info_mode:
        to_draw = ndraw.vstack([p.icon*(2 if p==cur else 1) for p in seq],
                               spacing=1)
        for i in range(3):
            a[:to_draw.shape[0],:to_draw.shape[1],i] = 128*to_draw
        a[to_draw == 2,:] = 255

period = 1
last_press = 0
info_mode = False
def keyboard_in(type, key):
    if key == 'i' and type == 'key-release':
        global info_mode
        info_mode = not info_mode
    elif type == 'key-press':
        global period, last_press
        now = time.time()
        print now-last_press
        if now - last_press < 2:
            period = (period + (now - last_press))/2
            print period
        last_press = now

if __name__ == '__main__':
    numm.run(**globals())
