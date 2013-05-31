"""
File: calc.py

Minecraft-pi script that creates an environment
for interacting with a breadboarded adder circuit
connected to the Raspberry pi's GPIOs.

Note: Accessing the GPIO's in Python requires
root access.  So to run this script use
the following command

sudo python calc.py

Author: Brandon Blodget 
URL: https://github.com/bblodget/RaspberryPi

Copyright (c) 2013, Brandon Blodget
All rights reserved.
"""

import minecraft.minecraft as minecraft
import minecraft.block as block
import time
import RPi.GPIO as GPIO

####################
# Constants
####################

# Tile coordinates (X,Y,Z) 
# where Y is up/down dimension
FLOOR_ORIGIN = (0,0,0)
FLOOR_SIZE = (25,1,16)
FLOOR_TYPE = block.DIAMOND_BLOCK

AIR_SIZE = (10,100,10)

A_BITS_LOC = [ (6,0,3), (8,0,3), (10,0,3)]
B_BITS_LOC = [ (14,0,3), (16,0,3), (18,0,3)]
BIT_TYPE = block.GOLD_BLOCK

####################
# Global Variables
####################

led_on = False
mc = minecraft.Minecraft.create()

####################
# Functions
####################

def setup():
    global mc

    # init the GPIO
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.OUT)
    GPIO.output(7,GPIO.LOW)

    # Create the diamond floor
    mc.setBlocks(FLOOR_ORIGIN[0], FLOOR_ORIGIN[1], FLOOR_ORIGIN[2],
                 FLOOR_ORIGIN[0]+FLOOR_SIZE[0]-1, 
                 FLOOR_ORIGIN[1],
                 FLOOR_ORIGIN[2]+FLOOR_SIZE[2]-1, 
                 FLOOR_TYPE)

    # Create Air Pad around the floor
    # make sure it is not burried in the ground.
    mc.setBlocks(FLOOR_ORIGIN[0]-AIR_SIZE[0], 
                 FLOOR_ORIGIN[1]+1, 
                 FLOOR_ORIGIN[2]-AIR_SIZE[2],

                 FLOOR_ORIGIN[0]+FLOOR_SIZE[0]+AIR_SIZE[0], 
                 FLOOR_ORIGIN[1]+AIR_SIZE[1],
                 FLOOR_ORIGIN[2]+FLOOR_SIZE[0]+AIR_SIZE[2], 
                 block.AIR)

    # create the A "bit blocks".
    # represents the A addend.
    for tile in A_BITS_LOC:
        mc.setBlocks(tile[0],tile[1],tile[2],
                    tile[0],tile[1],tile[2], BIT_TYPE)

    # create the B "bit blocks".
    # represents the B addend.
    for tile in B_BITS_LOC:
        mc.setBlocks(tile[0],tile[1],tile[2],
                    tile[0],tile[1],tile[2], BIT_TYPE)

    # move the player to the floor
    mc.player.setPos(0,0,0)


####################
# Main
####################

def main():
    global led_on, mc
    time.sleep(2)
    mc.postToChat("Minecraft Calc, Hit (Right Click) Grass Block\n"\
                  "on Diamond floor to light torch and LED")
    setup()

    #loop until Ctrl C
    try:
        while True:
            blockHits = mc.events.pollBlockHits()
            if blockHits:
                for blockHit in blockHits:
                    x,y,z = blockHit.pos
                    print x,y,z
                    if (x == -9 and z==11):
                        if (led_on):
                            GPIO.output(7,GPIO.LOW)
                            mc.setBlock(-9,3,11,0)
                            led_on = False;
                        else:
                            GPIO.output(7,GPIO.HIGH)
                            mc.setBlock(-9,3,11,50)
                            led_on = True;
                            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("stopped")


if __name__ == "__main__": main()

