from picamera import PiCamera
from time import sleep
from subprocess import call

time = 5
incidentNumber = 0
videoFolder = "/home/pi/Desktop/Projet3/Camera/videoFiles"
RaspVidFormat = ".h264"
MP4Format = ".mp4"
fileName = ""
# Setup the camera
camera = PiCamera()
camera.resolution = (1920, 1080)

# Fonction to create a video file name
def createVideoFileName():
    fileName = ("incident_" + str(incidentNumber))
    print ("New file name is " + fileName + RaspVidFormat)

# Fonction to convert the video file to MP4
def h264ToMp4():
    command = ("MP4Box -add " + fileName + RaspVidFormat + " " + fileName + MP4Format)
    call ([command], shell = True)
    print ("Video converted")

# Fonction to capture a video
def videoCapture():
    createVideoFileName()
    # Start recording
    camera.start_recording(videoFolder + fileName + RaspVidFormat)
    sleep(time)
    # Stop recording
    camera.stop_recording()
    # The camera is now closed
    print ("New incident no." + str(incidentNumber) + " as been saved to " + videoFolder + " as " + fileName + RaspVidFormat)
    #h264ToMp4()

incidentNumber += 1
videoCapture()
incidentNumber += 1
videoCapture()
incidentNumber += 1
videoCapture()
incidentNumber += 1
videoCapture()
incidentNumber += 1
videoCapture()




# Start recording
#camera.start_recording("/home/pi/Desktop/Projet3/Camera/incident_1.h264")
#sleep(5)
#camera.stop_recording()
#print ("New incident no.1 as been saved to /home/pi/Desktop/Projet3/Camera as incident_1.h264")
