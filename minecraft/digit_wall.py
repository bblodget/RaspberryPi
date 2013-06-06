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
import RPi.GPIO as GPIO


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

# Number of bits to use
NUM_BITS = 3

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
#   ..xaax..
#   ..f..b..
#   ..f..b..
#   ..xggx..
#   ..e..c..
#   ..e..c..
#   ..xddx..
#   .......*
#
# * is the origin. Left is positive x. Up is pos y.
# x is overlap

DIGIT = [
    [ON,  ON, ON,  ON,  ON,  ON,  OFF],
    [OFF, ON, ON,  OFF, OFF, OFF, OFF],
    [ON,  ON, OFF, ON,  ON,  OFF, ON],
    [ON,  ON, ON,  ON,  OFF, OFF, ON],
    [OFF, ON, ON,  OFF, OFF, ON,  ON],
    [ON,  OFF, ON, ON,  OFF, ON,  ON],
    [ON,  OFF, ON, ON,  ON,  ON,  ON],
    [ON,  ON, ON,  OFF, OFF, OFF, OFF],
    [ON,  ON, ON,  ON,  ON,  ON,  ON],
    [ON,  ON, ON,  ON,  OFF, ON,  ON],
]


####################
# Classes
####################


class DigitWall:

    def __init__(self, mc, xpos, ypos, zpos, wall_block, digit_block,
                 digit_value, bit_pin):
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

        # initialize the bit blocks
        self._init_bit_blocks(bit_pin)

        # create the wall
        self._draw_wall()

        # draw the bit blocks
        self._draw_bits()

    def _init_bit_blocks(self, bit_pin):
        # location of the three bit blocks
        # which represent a 3-bit binary number.
        # bit_block[0] is LSB
        z = self.zpos - 14
        self.bit_loc = [
            (self.xpos+1,self.ypos,z), 
            (self.xpos+3,self.ypos,z), 
            (self.xpos+5,self.ypos,z)
        ]

        # Each bit block can be ON or OFF
        # initialize the states
        self.bit_state = [OFF, OFF, OFF]

        # Each bit controls a GPIO pin 
        # This pin is asserted when the 
        # the bit is on and deasserted when
        # the bit is off.
        self.bit_pin = bit_pin

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
        # * is the origin. Left is positive x. Up is pos y.
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
        y = y + self.ypos + 1   # +1 because wall above floor
        z = self.zpos

        # define params to create seg using mc.setBlocks cmd
        self.segment[seg].append(x)
        self.segment[seg].append(y)
        self.segment[seg].append(z)
        self.segment[seg].append(x+SEG_LENGTH-1)
        self.segment[seg].append(y)
        self.segment[seg].append(z)

    def _init_vert_segment(self, seg, x, y):
        # convert x,y to absolute coordinates
        x = x + self.xpos
        y = y + self.ypos + 1   # +1 because wall above floor
        z = self.zpos 

        # define params to create seg using mc.setBlocks cmd
        self.segment[seg].append(x)
        self.segment[seg].append(y)
        self.segment[seg].append(z)
        self.segment[seg].append(x)
        self.segment[seg].append(y+SEG_LENGTH-1)
        self.segment[seg].append(z)


    def _draw_wall(self):
        # ypos+1 because wall above floor
        self.mc.setBlocks(self.xpos, self.ypos+1, self.zpos,
                          self.xpos+WALL_WIDTH-1,
                          self.ypos+WALL_HEIGHT,
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

    def _draw_bits(self):
        """ Redraws all the bit blocks based on their
        state.  Also asserts GPIO pins for bits that
        are ON.  Also calculates a new digit_value based
        on the state of the bits.
        """
        new_value = 0
        for i in range(NUM_BITS):
            if (self.bit_state[i] == ON):
                self.mc.setBlock(self.bit_loc[i][0],
                                 self.bit_loc[i][1],
                                 self.bit_loc[i][2],
                                 self.digit_block)
                GPIO.output(self.bit_pin[i],GPIO.HIGH)
                new_value = new_value + 2**i
            else:
                self.mc.setBlock(self.bit_loc[i][0],
                                 self.bit_loc[i][1],
                                 self.bit_loc[i][2],
                                 self.wall_block)
                GPIO.output(self.bit_pin[i],GPIO.LOW)
        self.digit_value = new_value

    def update(self, blockHits):
        """ Process blockHits events.  Checks
        If any of the bit blocks have been touched.
        If so toggles them and redraws bit blocks
        and digit_wall to represent the new state.
        """
        if blockHits:
            for blockHit in blockHits:
                x,y,z = blockHit.pos
                # check if a block_bit was touched
                for i in range(NUM_BITS):
                    if (self.bit_loc[i][0] == x and
                        self.bit_loc[i][1] == y and
                        self.bit_loc[i][2] == z):

                        # Erase the old wall digit
                        self._draw_digit(self.digit_value,OFF)
                        # Toggle the bit that was touched
                        self.bit_state[i] = not self.bit_state[i]
                        # Draw the bits. Also gets new 
                        # digit value
                        self._draw_bits()
                        # Draw the new wall digit
                        self._draw_digit(self.digit_value,ON)



