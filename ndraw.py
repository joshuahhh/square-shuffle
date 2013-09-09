# ndraw.py
# (joshuah@alum.mit.edu)

# assorted tools for drawing on numpy arrays
# see "squares" for example usages

import itertools

import numpy as np

def string_list_to_array(strings):
    return np.array([[(int(c) if c!=' ' else 0) for c in s] for s in strings])

numbers = [string_list_to_array(strings) for strings in
           [['11111',
             '1   1',
             '1   1',
             '1   1',
             '11111'],
            
            ['  1  ',
             ' 11  ',
             '  1  ',
             '  1  ',
             ' 111 '],
            
            [' 111 ',
             '1   1',
             '   1 ',
             ' 11  ',
             '11111'],
            
            ['11111',
             '    1',
             ' 1111',
             '    1',
             '11111'],
            
            ['   1 ',
             '  11 ',
             ' 1 1 ',
             '1111 ',
             '   1 '],

            ['11111',
             '1    ',
             '11111',
             '    1',
             '11111'],

            ['11111',
             '1    ',
             '11111',
             '1   1',
             '11111'],

            ['11111',
             '   1 ',
             '  1  ',
             ' 1   ',
             '1    '],

            ['11111',
             '1   1',
             '11111',
             '1   1',
             '11111'],

            ['11111',
             '1   1',
             '11111',
             '    1',
             '11111']]]
for number in numbers: number.flags.writeable = False

def hstack(seq, spacing=0):
    seq = list(seq)
    max_height = max(a.shape[0] for a in seq)
    sum_widths = sum(a.shape[1] for a in seq) + spacing*(len(seq)-1)
    canvas = np.zeros((max_height, sum_widths))
    o = 0
    for a in seq:
        canvas[:a.shape[0],o:o+a.shape[1]] = a
        o += a.shape[1] + spacing
    return canvas

def vstack(seq, spacing=0):
    seq = list(seq)
    max_width = max(a.shape[1] for a in seq)
    sum_heights = sum(a.shape[0] for a in seq) + spacing*(len(seq)-1)
    canvas = np.zeros((sum_heights, max_width))
    o = 0
    for a in seq:
        canvas[o:o+a.shape[0],:a.shape[1]] = a
        o += a.shape[0] + spacing
    return canvas

def num2bmp(n):
    return hstack([numbers[int(c)] for c in str(n)], spacing=1)

def rect_set(a, x, dx, y, dy, b):
    a[np.clip(x,0,a.shape[0]-1):np.clip(x+dx,0,a.shape[0]-1),
      np.clip(y,0,a.shape[1]-1):np.clip(y+dy,0,a.shape[1]-1)] = b

def rect_get(a, x, dx, y, dy):
    return a[np.clip(x,0,a.shape[0]-1):np.clip(x+dx,0,a.shape[0]-1),
             np.clip(y,0,a.shape[1]-1):np.clip(y+dy,0,a.shape[1]-1)]

def rect_apply(a, x, dx, y, dy, f):
    rect_set(a, x, dx, y, dy, f(rect_get(a, x, dx, y, dy)))
    
space = np.zeros((1,1))
nada  = np.zeros((0,0))
