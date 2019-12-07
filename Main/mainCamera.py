from picamera import PiCamera
import time
from subprocess import call
from datetime import datetime

i=0
dur = 5
incidentNumber = 0
videoFolder = "/home/pi/Desktop/Projet3/Main/videofiles/"
RaspVidFormat = ".h264"
MP4Format = ".mp4"
fileNameInLocation = ""
# Setup the camera
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 180

def getStatus():
    f = open("toCamera.txt", "r")
    status = f.readline()
    f.close
    status = status.replace('\n','')
    return status

def captureCompleted():
    f = open("toCamera.txt", "w")
    f.close

# Fonction to create a video file name
def createVideoFileName():
    fileName = str(str("incident_") + str(incidentNumber))
    print ("New file name is " + fileName + RaspVidFormat)
    return fileName

# Fonction to convert the video file to MP4
def h264ToMp4():
    command = ("MP4Box -add " + fileName + RaspVidFormat + " " + fileName + MP4Format)
    call ([command], shell = True)
    print ("Video converted")

# Fonction to capture a video
def videoCapture():
    fileName = createVideoFileName()
    #write incident
    date = datetime.now()
    f = open("gps.txt", "r")
    gps = f.readline()
    f.close
    f = open("incidents.txt", "a")
    f.write("New incident as been detected on : "  + str(date)+ "\nAt position " + str(gps))
    f.write("\nThis incident as been saved to "  + videoFolder + " as " + fileName + RaspVidFormat + "\n\n")
    f.close
    # Start recording
    fileNameInLocation = str(videoFolder + fileName + RaspVidFormat)
    print(fileNameInLocation)
    camera.start_recording(fileNameInLocation)
    time.sleep(dur)
    # Stop recording
    camera.stop_recording()
    # The camera is now closed
    print ("New incident no." + str(incidentNumber) + " as been saved to " + videoFolder + " as " + fileName + RaspVidFormat)
    
    #h264ToMp4()
f = open("incidents.txt", "w")
f.close
f = open("toCamera.txt", "w")
f.close
print("waiting for new incident")
while i == 0 :
    status = getStatus()
    if status == 'Incident' :
        incidentNumber += 1
        videoCapture()
        captureCompleted()
        print("waiting for new incident")

