
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

i = 0
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
incidentNumber = 0

def getStatus():
    f = open("fromPhone.txt", "r")
    status = f.readline()
    f.close
    status = status.replace('\n','')
    return status

def getStatusCamera():
    f = open("toCamera.txt", "r")
    status = f.readline()
    f.close
    status = status.replace('\n','')
    return status

def sendStatus():
    f = open("toPhone.txt", "a")
    f.write("Incident\n" + str(distance))
    f.close
    f = open("incidents.txt", "a")
    f.write("A car as been detected at a distance of : " + str(distance) + " cm\n")
    f.close
    print("Incident\n" + str(distance))
    f = open("toCamera.txt", "a")
    f.write("Incident")
    f.close

def get_distance():
    if GPIO.input (ECHO):                                               
        return (100000)                                                    
    distance = 0                                                        
    GPIO.output (TRIG,False)                                            
    time.sleep (0.05)                                                   
    GPIO.output (TRIG,True)                                             
    dummy_variable = 0                                                  
    dummy_variable = 0                                                 
    GPIO.output (TRIG,False)                                            
    time1, time2 = time.time(), time.time()                             
    while not GPIO.input (ECHO):                                        
        time1 = time.time()                                             
        if time1 - time2 > 0.02:                                        
            return (100000)                                              
            break                                                                                                       
    while GPIO.input (ECHO):                                            
        time2 = time.time()                                             
        if time2 - time1 > 0.02:                                        
            return (100000)                                             
            break                                                                                                                                                                       
    distance = (time2 - time1) / 0.00000295 / 2 / 10
    return (distance)

def DetectIncident():
        distance = get_distance()
        if distance !=100000:
            print (distance)
            if distance < 120 :
                distanceDetected = distance
                distance = get_distance()
                while distance == 100000:
                    distance = get_distance()
                distanceDetected += distance
                distance = get_distance()
                while distance == 100000:
                    distance = get_distance()
                distanceDetected += distance
                distanceDetected = distanceDetected/3
                if distanceDetected <= 100:
                    print ("Voiture detectee a une distance de ", distanceDetected, " : Capture de video en cours")
                    return distanceDetected
        return 0        
#clear files before begining
f = open("toPhone.txt", "w")
f.close
f = open("toCamera.txt", "w")
f.close
print("Waiting for signal to begin")
while i == 0 :
    status = getStatus()
    statusCam = getStatusCamera()
    while status == 'startActivity' and statusCam == '' :
        distance = DetectIncident()
        if distance != 0 :
            sendStatus()
        status = getStatus()
        statusCam = getStatusCamera()
        
