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
import unittest
import urllib2
#from smb.SMBHandler import SMBHandler
#import PortalWebGUICore
#from robot.api import logger
#from smb.SMBHandler import SMBHandler
import ftplib 
from ftplib import FTP
from ftplib import error_perm
from threading import Timer
count=0 # Count Port range
n=0     # log count point
TestResult="" # TestResult ,will return to 

class UDP_Client_init(object):


       #def __init__(self,interfaceIP,startport,endport,ftpserver):
    def __init__(self,interfaceIP,startport,endport):  

        """
        Local UDP Client Site 

        """  
                
        self.interfaceIP=interfaceIP
        self.startport=startport
        self.endport=endport

        #self.ftpserver=ftpserver
        count=int(self.endport)-int(self.startport)
        self.username="pap1"
        self.password="12345678"
        self.log1path="TCP-Client.log"         # for All history
        self.logpath2="TCP-Client-latest.log"  # for Latest log 


    def CheckStatus(self,File1,Need_Delete):  # detect Latest log rule
        if Need_Delete == True :
            if os.path.exists(File1):
              os.remove(File1)     
        else:
            while not os.path.exists(File1):           
              time.sleep(1)
              pass

    def udpclient_control(self):
        

        #--define cinterfaceIP=self.interfaceIP / cstartport=self.startport / cendport=self.endport 
        #   The client_control use only

        hostname1=""
        os_platform=""
        c_sessions=0 #Current Session count
        n=0 #"Log event count"
        STARTTIME="" # Session start time ,default null
        ENDTIME=""   # Session End time
          
        os_platform=platform.system()
        if 'Windows' in os_platform:
            print "**********************************************************************"
            print "*                                                                    *"
            print "*  Ignitiondl Portal   -----     UDP Client   (Windows version)      *"
            print "*                                                                    *"
            print "**********************************************************************"

        elif 'Linux' or 'Darwin' in os_platform:

            print "**********************************************************************"
            print "*                                                                    *"
            print "*  Ignitiondl Portal   -----     UDP Client   (Linux / Mac version)  *"
            print "*                                                                    *"
            print "**********************************************************************"
                                                                   
    # Ask for input


            # Ask for input
        #subprocess.call('clear', shell=True)
        print "--Start Port is : "+str(self.startport)+"---End Port is : "+str(self.endport)

        cstartport=int(self.startport)  # Start port transfer to int
        cendport=int(self.endport)      # End port transfer to int
        cendport=int(cendport+1)       
        print "Your Server IP address : ",self.interfaceIP
        #remoteServer=raw_input("Enter a TCP Server Address : ")
        remoteServer=self.interfaceIP
        remoteServerIP=socket.gethostbyname(remoteServer)

        # Print a nice banner with information on which host we are about to scan
        print "-" * 60
        print "Please wait, scanning remote host", remoteServerIP
        print "-" * 60

        # Check what time the scan started
        t1 = datetime.now()



        # Using the range function to specify ports (here it will scans all ports between 1 and 1024)

        # We also put in some error handling for catching errors
        cmd="HELLO, Ignitiondl Firewall UDP Test tool."
        """
        try:
            startport=raw_input("Enter a Start port number : ")
        except:
            print "The start port is not NULL ,please entry again"
            sys.exit()
          
        try:
            endport=raw_input("Enter a End port number : ")
        except:
            print "The start port is not NULL ,please entry again"
            sys.exit()
        

        startport=int(startport)  # Start port transfer to int
        endport=int(endport)      # End port transfer to int

        """
       #---File Management
        # 2017/01/09 Open Log file first and close when done range test
        localtime = time.asctime( time.localtime(time.time()) )
        #for linux using as below:
        curDir=os.path.dirname(os.path.abspath(__file__))            
        curDir=str(curDir)
    
        if 'Windows' in os_platform:
            #--------------------------------------- --------------
            filename=curDir+"/"+"UDP-Client.log"            #save all history
            filelatest=curDir+"/"+"UDP-Client-latest.log"   #Save latest log
            #File name replace role as below:
            #filename=re.sub(r"\\", r"\'", filename) # if have d:/xxx/xxx
            #filename=re.sub(r'//', r"\'", filename) 
            #print filename
            fo1=open(filename,"ab+")
            fo2=open(filelatest,"ab+")
            topen = datetime.now()   # Record start record time
            print "\n\n"+str(topen)  # print start time in monitor
            STARTTIME="\nSTART : ->"+str(topen)
            print STARTTIME  # print start time in monitor
            fo1.write(STARTTIME)
            fo2.write(STARTTIME)

        elif 'Linux' or 'Darwin' in os_platform:
            #--------------------------------------- --------------
            filename=curDir+"/"+"UDP-Client.log"
            filelatest=curDir+"/"+"UDP-Client-latest.log"   #Save latest log
            #File name replace role as below:
            #filename=re.sub(r'\\', r'/', filename) # if have d:/xxx/xxx
            #filename=re.sub(r'//', r'\\', filename) # if d:/ or c:/ only
            #print filename
            fo1=open(filename,"ab+")
            fo2=open(filelatest,"ab+")
            topen = datetime.now()   # Record start record time
            STARTTIME="\nSTART : ->"+str(topen)
            print STARTTIME  # print start time in monitor
            fo1.write(STARTTIME)
            fo2.write(STARTTIME)
            #-----------------------------------------------------"START : ->"+str(topen)--------------
            #------------------------------------------------------------------------------------


        for port in range(cstartport,cendport): 
            try:
              s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
              s.settimeout(0.5) 
              address=(remoteServerIP,port)
              s.sendto(cmd,address) 
              if 'Windows' in os_platform:
                  #--------------------------------------- --------------

                  fo2=open(filelatest,"ab+")
                  RESULT ="\n# "+str(remoteServerIP)+"  Port  {}    PASS  ".format(port)+" "+str(localtime)
                  fo1.write(RESULT)
                  fo2.write(RESULT)                    
                  RESULT="" 
                  print str(remoteServerIP)+"  Port  {}    PASS  ".format(port)+" "+str(localtime)


              elif 'Linux' or 'Darwin' in os_platform:
                  #--------------------------------------- --------------

                  RESULT ="\n# "+str(remoteServerIP)+"  Port  {}    PASS  ".format(port)+" "+str(localtime)
                  fo1.write(RESULT)
                  fo2.write(RESULT)                    
                  RESULT="" 
                  print str(remoteServerIP)+"  Port  {}    PASS  ".format(port)+" "+str(localtime)
                
              c_sessions=c_sessions+1 
              #print "Remote Server IP  / Port is : ",remoteServerIP,port
              s.close()  

            except KeyboardInterrupt:
              print "You pressed Ctrl+C"
              sys.exit()

            except socket.gaierror:
              print 'Hostname could not be resolved. Exiting'
          
            except socket.error:
          
              print str(remoteServerIP)+"  Port  {}    FAIL  ".format(port)+" "+str(localtime)
                

        # Checking the time again
        t2 = datetime.now()

        # Calculates the difference of time, to see how long it took to run the script
        total =  t2 - t1

        # Printing the information to screen
        print 'Scanning Completed in: ', total
