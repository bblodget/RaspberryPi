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

# DigitWall Dimensions
WALL_WIDTH = 8
WALL_HEIGHT = 9

# Segment Dimensions
SEG_LENGTH = 4

# Segment states (illumination)
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
#   ........
#   ...aa...
#   ..f..b..
#   ..f..b..
#   ...gg...
#   ..e..c..
#   ..e..c..
#   ...dd...
#   .......*
#
# DIGIT[x] = [a,b,c,d,e,f,g]
# * is the origin. Left is pos x.
# Up is pos y.

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

    def __init__(self, mc, xpos, ypos, zpos, wall_block, digit_block, digit_value):
        # save a copy of the minecraft object
        self.mc = mc

        # position to place the wall
        # y is the vertical dimension
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos

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
        # create block arrays that represent the segments
        self.segment = [
            [], [], [], [], [], [], []
        ]
        #   ..xaax..
        #   ..f..b..
        #   ..f..b..
        #   ..xggx..
        #   ..e..c..
        #   ..e..c..
        #   ..xddx..
        #   .......*
        #
        # * is the origin. Left is pos x. Up is pos y.
        # x is overlap
        self._init_horiz_segment(SEG_A, 2, 7)
        self._init_vert_segment(SEG_B, 2, 4)
        self._init_vert_segment(SEG_C, 2, 1)
        self._init_horiz_segment(SEG_D, 2, 1)
        self._init_vert_segment(SEG_E, 5, 1)
        self._init_vert_segment(SEG_F, 5, 4)
        self._init_horiz_segment(SEG_G, 2, 4)

    def _init_horiz_segment(self, seg, x, y):
        # convert x,y to absolute coordinates
        x = x + self.xpos
        y = y + self.ypos

        # define params to create seg using mc.setBlocks cmd
        self.segment[seg].append(x)
        self.segment[seg].append(y)
        self.segment[seg].append(self.zpos)
        self.segment[seg].append(x+SEG_LENGTH-1)
        self.segment[seg].append(y)
        self.segment[seg].append(self.zpos)

    def _init_vert_segment(self, seg, x, y):
        # convert x,y to absolute coordinates
        x = x + self.xpos
        y = y + self.ypos

        # define params to create seg using mc.setBlocks cmd
        self.segment[seg].append(x)
        self.segment[seg].append(y)
        self.segment[seg].append(self.zpos)
        self.segment[seg].append(x)
        self.segment[seg].append(y+SEG_LENGTH-1)
        self.segment[seg].append(self.zpos)


    def _draw_wall(self):
        self.mc.setBlocks(self.xpos, self.ypos, self.zpos,
                          self.xpos+WALL_WIDTH-1,
                          self.ypos+WALL_HEIGHT-1,
                          self.zpos,
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
        self._draw_digit(self.digit_value,ON)



