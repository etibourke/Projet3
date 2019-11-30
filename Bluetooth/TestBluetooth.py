
import os
import sys
from bluetooth import *
from wifi import Cell, Scheme
import subprocess
import time

i = 0

def WIFISetup():
    SSID= client_sock.recv(1024)
    Username= client_sock.recv(1024)
    Password= client_sock.recv(1024)
    print (Username)
    if Username == b'Username (if applicable)':
        wifi = 'network={' + '\n\t' + 'ssid="'
        print (wifi)

def StartActivity():
    
    
 
#set up bluetooth server
while i==0:
    server_sock= BluetoothSocket( RFCOMM )
    port = 0x1101 #make sure you've set up an RFCOMM sdptool
    server_sock.bind(("",port))
    server_sock.listen(1)
    print ("listening ")

    try:
        client_sock,address = server_sock.accept()
        print ("Accepted connection from ",address)
        print ("waiting for commands")
        while i==0:
            data= client_sock.recv(1024)
            message = str(data)
            print (message.replace('b','',1))
            if data == b'Android Connected':
                print ("Android Connected")
            if data == b'WIFI Configuration':
                print ("WIFI Configuration Start")
                WIFISetup()
                print ("WIFI Configuration Completed")
            if data == b'StartActivity':
                print ("Activity Start")
                StartActivity()
                print ("WIFI Configuration Completed")
            if data == b'Android Disconnected':
                print ("Android Disconnected")
                server_sock.close()
                break
            
            server_sock.close()

    except:
        print ("Exiting")
        server_sock.close()

