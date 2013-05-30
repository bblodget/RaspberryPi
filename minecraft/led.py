# Touch a block to turn on a torch and an led.

import minecraft.minecraft as minecraft
import minecraft.block as block
import time
import RPi.GPIO as GPIO

led_on = False

def setup():
    mc.setBlock(-9,2,11,2)
    mc.setBlock(-9,3,11,0)

    mc.player.setPos(-7,2,13)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.OUT)
    GPIO.output(7,GPIO.LOW)


if __name__ == "__main__":

    time.sleep(2)
    mc = minecraft.Minecraft.create()
    mc.postToChat("Minecraft LED, Hit (Right Click) Grass Block on Diamond floor to light torch and LED")
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
