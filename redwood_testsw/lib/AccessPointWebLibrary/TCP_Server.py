#!/usr/bin/env python
import os
import time
import socket
import subprocess
import sys
from datetime import datetime
import select
import Queue
import thread
import string
import re
import platform

import urllib2
#from robot.api import logger
#from robot.utils.asserts import *
#from smb.SMBHandler import SMBHandler
#import PortalWebGUICore
#from robot.api import logger
#from smb.SMBHandler import SMBHandler
from ftplib import FTP
from ftplib import error_perm
from threading import Timer

#1230 --TBD , need define Server address function

class TCP_Server_init(object):

        ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'
        def __init__(self,interfaceIP,startport,endport):
            self.interfaceIP=interfaceIP
            self.startport=startport
            self.endport=endport
 
        def server_control(self):

            """
            #--12/29 remark don't use
            try:
              startport=str(sys.argv[1])
              #print sys.argv[1]
              endport=str(sys.argv[2])
              #print sys.argv[2]
            except:
              print "Please argument 1 is Start-port , argument 2 is End-Port . "
              sys.exit()
            """  
            newstartport=int(self.startport)  # Start port transfer to int
            newendport=int(self.endport)      # End port transfer to int
            newendport=int(newendport+1)
            
            print "***********************************************************************"
            print "*                                                                    *"
            print "*  Ignitiondl TCP Server                                             *"
            print "*                                                                    *"
            print "**********************************************************************"

            # Clear the screen   

            #subprocess.call('clear', shell=True)
            print "--Start Port is : "+str(newstartport)+"---End Port is : "+str(newendport)
                                                             

            #get ip command :  ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'

            #get interface command :                                                  

            # Ask for input
            #"eth interface as below,default is eth0"
            #interface="eth0"
            #interfaceIP=os.popen("ifconfig %s | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"%interface)
            #interfaceIP=interfaceIP.read()
            
            print"Your Server IP address : ",self.interfaceIP
            #remoteServer=raw_input("Enter a TCP Server Address : ")
            remoteServer=self.interfaceIP
            remoteServerIP=socket.gethostbyname(remoteServer)
            #remoteServer=raw_input("Enter a TCP Server Address : ")

            # print a nice banner with information on which host we are about to scan
            print "-" * 60
            print "Please wait, trying to connect remote Server", remoteServerIP
            print "-" * 60

            # Check what time the scan started
            t1 = datetime.now()


            

            #-----------------------------------------------------------------


            servers = []     
            print "*****************************************************************"
            try:     
                for port in range(newstartport,newendport):     

                   
                    ds = (remoteServerIP, port)        
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server.bind(ds)
                    server.listen(5)
                    servers.append(server) 
                    print "--------------------------------------------------------------"
                    print "\n",remoteServerIP,"  Port {}  :    Listen".format(port)
                  

                while 1 :

                    readable,_,_ = select.select(servers, [], [])
                    ready_server = readable[0]        
                    connection, address = ready_server.accept()        
                    data = connection.recv(1024) # Get data from connection
                    recIP= address[0]  # Get receive IP from address
                    recPort=address[1] # Get port from address
                    print "---------------------------------------------------------------------------"
                    print "\n","Receive IP: "+str(recIP)+" Port: "+str(recPort)+"-->info is :  "+data
                 
                    #------------------------------------------------------
                    if data == "SHUTDOWN" :
                       print "\n-----TCP Server get shutdown command"
                        


            except socket.gaierror:

                print'Hostname could not be resolved. Exiting'
                sys.exit()

            except socket.error:
                
                print "Couldn't connect to server"
                print "The Server Start Port and End Port is incorrect,please Retry ,thanks"
                sys.exit()

            except KeyboardInterrupt:   
                
                print "You pressed Ctrl+C"
                # Checking the time again
                t2 = datetime.now()

                # Calculates the difference of time, to see how long it took to run the script
                total =  t2 - t1

                # printing the information to screen
                print "******************************************************************************\n"
                print '-------------------Make TCP Connection in: ', total
                print "******************************************************************************\n"
                sys.exit()

#------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    #main()
    tcpserver=TCP_Server_init("127.0.0.1",3000,3010)
    tcpserver.server_control()









