import os
import sys
from bluetooth import *
from wifi import Cell, Scheme
import subprocess
import time

i = 0

def getStatus():
    f = open("toPhone.txt", "r")
    status = f.readline()
    f.close
    status = status.replace('\n','')
    return status

def sendIncidents():
    f = open("incidents.txt", "r")
    message = f.read()
    f.close
    print(message)
    client_sock.send(message)

def sendStatus(incidentNumber):
    f = open("toPhone.txt", "r")
    distance = f.read()
    distance = distance.replace('Incident','')
    distance = distance.replace('\n','')
    f.close
    print(distance)
    message = "Voiture detectee a " + distance + " : Incident numero " + str(incidentNumber)
    print(message)
    client_sock.send(message)

def statusSent():
    f = open("toPhone.txt", "w")
    f.close

def writeGPS():
    Latitude = client_sock.recv(1024)
    Longitude = client_sock.recv(1024)
    Latitude = txtConversion(Latitude)
    Longitude = txtConversion(Longitude)
    f = open("gps.txt", "w")
    f.write(Latitude)
    f.write(Longitude)
    f.close

def txtConversion(text):
    text = str(text)
    text = text.replace('b\'','',1)
    text = text.replace('\'','')
    return text

def WIFISetup():
    SSID= client_sock.recv(1024)
    Username = client_sock.recv(1024)
    Password = client_sock.recv(1024)
    SSID = txtConversion(SSID)
    Username = txtConversion(Username)
    Password = txtConversion(Password)
    #f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "a")
    f = open("wifi.txt", "a")
    newWifi = '\nnetwork={\n\tssid=\"' + SSID + '\"\n\tpriority=3\n\t'
    if Username != "true":
        newWifi += 'identity=\"' + Username + '\"\n\t'       
    newWifi += 'psk=\"' + Password + '\"\n\tid_str=\"' + SSID + '\"\n}\n'
    f.write(newWifi)
    f.close

def StartActivity():
    f = open("fromPhone.txt", "w")
    f.write("startActivity")
    f.close

def StopActivity():
    f = open("fromPhone.txt", "w")
    f.write("stopActivity")
    f.close 
    
def Application():
    incidentNumber = 0
    while i==0:
        data = client_sock.recv(1024)
        data = txtConversion(data)
        #print(data)
        if data == "Android Connected":
            print ("Android Connected")
        if data == "WIFI Configuration":
            print ("WIFI Configuration Start")
            WIFISetup()
            print ("WIFI Configuration Completed")
        if data == "StartActivity":
            print ("Activity Start")
            StartActivity()
        if data == "GPS Position":
            print ("GPS Position Received")
            writeGPS()
        if data == "GetIncidents":
            print ("Send Incidents")
            sendIncidents()
            print ("Incidents Sent")
        if data == "EndActivity":
            print ("Activity Ends")
            StopActivity()
        if data == "Android Disconnected":
            print ("Android Disconnected")
            server_sock.close()
            break
        status = getStatus()
        if status == 'Incident':
            incidentNumber += 1
            print("Nouveau incident : " + str(incidentNumber))
            sendStatus(incidentNumber)
            statusSent()    

#clear files before begining
f = open("gps.txt", "w")
f.close
f = open("toPhone.txt", "w")
f.close
while i==0:
    #set up bluetooth server
    server_sock= BluetoothSocket( RFCOMM )
    port = 0x1101 #make sure you've set up an RFCOMM sdptool
    server_sock.bind(("",port))
    server_sock.listen(1)
    print ("listening ")

    try:
        client_sock,address = server_sock.accept()
        print ("Accepted connection from ",address, " : waiting for commands")
        Application()

    except:
        print ("Exiting")
        server_sock.close()


