"""

File: digit_wall.py

This module defines a class DigitWall which
creates a wall that can display a 7-segment
digit in a Minecraft world.

It provides a method to update the digit 
that is displayed.

Author: Brandon Blodget 
URL: https://github.com/bblodget/RaspberryPi

Copyright (c) 2013, Brandon Blodget
All rights reserved.

"""

from __future__ import division


####################
# Module Constants
####################

# states of a segment
ON = True
OFF = False

# used to index into DIGIT
SEG_A = 0
SEG_B = 1
SEG_C = 2
SEG_D = 3
SEG_E = 4
SEG_F = 5
SEG_G = 6

# Define the segments used in each digit.
#
#   --a--
#   |   |
#   f   b
#   |   |
#   --g--         
#   |   |
#   e   c
#   |   |
#   --d--         
#
# DIGIT[x] = [a,b,c,d,e,f,g]
# ON = Illuminated segment

DIGIT = [
    [ON,  ON, ON,  ON,  ON,  ON,  OFF],
    [OFF, ON, ON,  OFF, OFF, OFF, OFF],
    [ON,  ON, OFF, ON,  ON,  OFF, ON],
    [ON,  ON, ON,  ON,  OFF, OFF, ON],
    [OFF, ON, ON,  OFF, OFF, ON,  ON],
    [ON,  ON, OFF, ON,  OFF, ON,  ON],
    [ON,  ON, OFF, ON,  ON,  ON,  ON],
    [ON,  ON, ON,  OFF, OFF, OFF, OFF],
    [ON,  ON, ON,  ON,  ON,  ON,  ON],
    [ON,  ON, ON,  ON,  OFF, ON,  ON],
]


####################
# Classes
####################

class DigitWall:

    def __init__(self, mc, xpos, ypos, zpos, width, height,
                 thickness, wall_block, digit_block, digit_value):
        # save a copy of the minecraft object
        self.mc = mc

        # position to place the wall
        # y is the vertical dimension
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos

        # shape of the wall
        self.wall_width = width
        self.wall_height = height
        self.wall_thickness = thickness
        
        # blocks that the wall is made of
        self.wall_block = wall_block
        self.digit_block = digit_block

        # the initial digit value.
        self.digit_value = digit_value

        # initialize the segment fields
        self._init_segments()

        # create the wall
        self._draw_wall()

    def _init_segments(self):
        # compute segment length and width
        w = self.wall_width // 2
        h = self.wall_height // 4
        if (w > h):
            seg_length = h
        else:
            seg_length = w
        if seg_length < 1:
            seg_length = 1
        seg_width = seg_length // 4
        if seg_width < 1:
            seg_width = 1

        # store segment width and length
        self.seg_length = seg_length
        self.seg_width = seg_width

        print "seg_length: ",seg_length, " seg_width: ",seg_width

        # compute digit width, height and origin
        digit_width = (seg_width*2) + seg_length
        digit_height = (seg_width*3) + (seg_length*2)
        digit_x =  self.xpos + (self.wall_width//2) - (digit_width//2)
        digit_y = self.ypos + (self.wall_height//2) - (digit_height//2)

        # compute segments origins
        a_x = digit_x + seg_width
        a_y = digit_y
        b_x = a_x + seg_length
        b_y = digit_y + seg_width
        c_x = b_x
        c_y = b_y + seg_width
        d_x = a_x
        d_y = digit_height - seg_width
        e_x = digit_x
        e_y = c_y
        f_x = digit_x
        f_y = b_y
        g_x = a_x
        g_y = c_y - seg_width

        # create block arrays that represent the segments
        self.segment = [
            [], [], [], [], [], [], []
        ]
        self._init_horiz_segment(SEG_A, a_x, a_y)
        self._init_vert_segment(SEG_B, b_x, b_y)
        self._init_vert_segment(SEG_C, c_x, c_y)
        self._init_horiz_segment(SEG_D, d_x, d_y)
        self._init_vert_segment(SEG_E, e_x, e_y)
        self._init_vert_segment(SEG_F, f_x, f_y)
        self._init_horiz_segment(SEG_G, g_x, g_y)

    def _init_horiz_segment(self, seg, x, y):
        mirror_y =self.ypos+self.wall_height-y
        mirror_x =self.xpos+self.wall_width-x
        self.segment[seg].append(mirror_x)
        self.segment[seg].append(mirror_y)
        self.segment[seg].append(self.zpos)
        self.segment[seg].append(mirror_x-self.seg_length-1)
        self.segment[seg].append(mirror_y-self.seg_width-1)
        self.segment[seg].append(self.zpos)

    def _init_vert_segment(self, seg, x, y):
        mirror_y =self.ypos+self.wall_height-y
        mirror_x =self.xpos+self.wall_width-x
        self.segment[seg].append(mirror_x)
        self.segment[seg].append(mirror_y)
        self.segment[seg].append(self.zpos)
        self.segment[seg].append(mirror_x-self.seg_width-1)
        self.segment[seg].append(mirror_y-self.seg_length-1)
        self.segment[seg].append(self.zpos)


    def _draw_wall(self):
        self.mc.setBlocks(self.xpos, self.ypos, self.zpos,
                          self.xpos+self.wall_width-1,
                          self.ypos+self.wall_height-1,
                          self.zpos+self.wall_thickness-1,
                          self.wall_block)
        self._draw_digit(self.digit_value,ON)

    def _draw_digit(self, digit, on):
        block = self.wall_block
        if (on):
            block = self.digit_block
        seg_on = DIGIT[digit]
        i =0        # segment index 
        for seg in self.segment:
            if (seg_on[i]):
                self.mc.setBlocks(seg[0], seg[1], seg[2],
                                  seg[3], seg[4], seg[5],
                                  block)
            i = i + 1

    def update(self, digit_value):
        # Erase the old value 
        # Draw the new value
        self._draw_digit(self.digit_value,OFF)
        self.digit_value = digit_value
        self._draw_digit(self.digit_value,OFF)



        

        


        

