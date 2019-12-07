#This code is greatly inspired from this link :
#https://www.raspberrypi.org/forums/viewtopic.php?t=77534
###########################################################################

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print ("Waiting For Sensor")
time.sleep(2)

def get_distance ():

    if GPIO.input (ECHO):                                               # If the 'Echo' pin is already high
        return (100)                                                    # then exit with 100 (sensor fault)

    distance = 0                                                        # Set initial distance to zero

    GPIO.output (TRIG,False)                                            # Ensure the 'Trig' pin is low for at
    time.sleep (0.05)                                                   # least 50mS (recommended re-sample time)

    GPIO.output (TRIG,True)                                             # Turn on the 'Trig' pin for 10uS (ish!)
    dummy_variable = 0                                                  # No need to use the 'time' module here,
    dummy_variable = 0                                                  # a couple of 'dummy' statements will do fine
    
    GPIO.output (TRIG,False)                                            # Turn off the 'Trig' pin
    time1, time2 = time.time(), time.time()                             # Set inital time values to current time
    
    while not GPIO.input (ECHO):                                        # Wait for the start of the 'Echo' pulse
        time1 = time.time()                                             # Get the time the 'Echo' pin goes high
        if time1 - time2 > 0.02:                                        # If the 'Echo' pin doesn't go high after 20mS
            distance = 100                                              # then set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
    
    while GPIO.input (ECHO):                                            # Otherwise, wait for the 'Echo' pin to go low
        time2 = time.time()                                             # Get the time the 'Echo' pin goes low
        if time2 - time1 > 0.02:                                        # If the 'Echo' pin doesn't go low after 20mS
            distance = 100                                              # then ignore it and set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
        
                                                                        # Sound travels at approximately 2.95uS per mm
                                                                        # and the reflected sound has travelled twice
                                                                        # the distance we need to measure (sound out,
                                                                        # bounced off object, sound returned)
                                                                        
    distance = (time2 - time1) / 0.00000295 / 2 / 10                    # Convert the timer values into centimetres
    print(distance)
    return distance

f = open("resultats.txt", "w")
f.close
record = 1
increment = 0
while record == 1:
    increment += 1
    print(str(increment))
    distance = get_distance()
    while distance == 100 :
        distance = get_distance()
    f = open("resultats.txt", "a")
    f.write(str(distance) + ";\n")
    f.close
    time.sleep(5)
    if increment >= 5 :
        increment = 0

GPIO.cleanup()
