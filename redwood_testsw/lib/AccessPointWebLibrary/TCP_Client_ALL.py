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
from robot.api import logger
from robot.utils.asserts import *

from random import randint
#from smb.SMBHandler import SMBHandler
import ftplib 
from ftplib import FTP
from ftplib import error_perm
from threading import Timer
count=0 # Count Port range
n=0     # log count point
TestResult="" # TestResult ,will return to 

Resvalue1=0  #for PASS Value
Resvalue2=0  #for Fail Value


class TCP_Client_init(object):
    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE' 
     
    #def __init__(self,interfaceIP,startport,endport,ftpserver):
    def __init__(self,interfaceIP,startport,endport,expect_result=None):  
        self.interfaceIP=interfaceIP
        self.startport=startport
        self.endport=endport
        self.expect_result=expect_result
        #logger.console("system default is :",expect_result)
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
  



    def client_control(self):        
        #time.sleep(5)  # Wait for tcp server execute
        hostname1=""
        os_platform=""
        c_sessions=0 #Current Session count
        n=0 #"Log event count"
        STARTTIME="" # Session start time ,default null
        ENDTIME=""   # Session End time
            
        os_platform=platform.system()
        if 'Windows' in os_platform:
            logger.console("\n**********************************************************************")
            logger.console("*                                                                      *")
            logger.console("*    Ignitiondl Portal   -----     TCP Client  (Windows version)       *")
            logger.console("*                                                                      *")
            logger.console("***********************************************************************")

        elif 'Linux' or 'Darwin' in os_platform:

            logger.console("\n**********************************************************************")
            logger.console("*                                                                     *")
            logger.console("*   Ignitiondl Portal   -----     TCP Client  (Linux / Mac version)   *")
            logger.console("*                                                                     *")
            logger.console("***********************************************************************")


        # Ask for input
        #subprocess.call('clear', shell=True)
        logger.console("--Start Port is : "+str(self.startport)+"---End Port is : "+str(self.endport))

        cstartport=int(self.startport)  # Start port transfer to int
        cendport=int(self.endport)      # End port transfer to int
        cendport=int(cendport+1)       
        logger.console("Your Server IP address : "+self.interfaceIP)
        #remoteServer=raw_input("Enter a TCP Server Address : ")
        remoteServer=self.interfaceIP
        remoteServerIP=socket.gethostbyname(remoteServer)

        # logger.console a nice banner with information on which host we are about to scan
        logger.console("-" * 60)
        logger.console("Please wait, scanning remote host", remoteServerIP)
        logger.console("-" * 60)

        # Check what time the scan started
        t1 = datetime.now()



        # Using the range function to specify ports (here it will scans all ports between 1 and 1024)

        # We also put in some error handling for catching errors
        cmd="HELLO, Ignitiondl TCP Client."

       #---File Management
        # 2017/01/09 Open Log file first and close when done range test
        localtime = time.asctime( time.localtime(time.time()) )
        #for linux using as below:
        curDir=os.path.dirname(os.path.abspath(__file__))            
        curDir=str(curDir)
    
        if 'Windows' in os_platform:
            #--------------------------------------- --------------
            filename=curDir+"/"+"TCP-Client.log"            #save all history
            filelatest=curDir+"/"+"TCP-Client-latest.log"   #Save latest log
            #File name replace role as below:
            #filename=re.sub(r"\\", r"\'", filename) # if have d:/xxx/xxx
            #filename=re.sub(r'//', r"\'", filename) 
            #logger.console filename
            fo1=open(filename,"ab+")
            fo2=open(filelatest,"ab+")
            topen = datetime.now()   # Record start record time
            logger.console("\n\n"+str(topen))  # logger.console start time in monitor
            STARTTIME="START : ->"+str(topen)
            logger.console(STARTTIME)  # logger.console start time in monitor
            fo1.write(STARTTIME)
            fo2.write(STARTTIME)

        elif 'Linux' or 'Darwin' in os_platform:
            #--------------------------------------- --------------
            filename=curDir+"/"+"TCP-Client.log"
            filelatest=curDir+"/"+"TCP-Client-latest.log"   #Save latest log
            #File name replace role as below:
            #filename=re.sub(r'\\', r'/', filename) # if have d:/xxx/xxx
            #filename=re.sub(r'//', r'\\', filename) # if d:/ or c:/ only
            #logger.console filename
            fo1=open(filename,"ab+")
            fo2=open(filelatest,"ab+")
            topen = datetime.now()   # Record start record time
            STARTTIME="START : ->"+str(topen)
            logger.console(STARTTIME)  # logger.console start time in monitor
            fo1.write(STARTTIME)
            fo2.write(STARTTIME)
            #-----------------------------------------------------"START : ->"+str(topen)--------------
            #------------------------------------------------------------------------------------


        for port in range(cstartport,cendport):            
            
            try:
                #for port in range(cstartport,cendport):  
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((remoteServerIP, port))
                address=(remoteServerIP,port)
                sock.sendto(cmd,address) 
                if result == 0:

                   if 'Windows' in os_platform:
                       #--------------------------------------- --------------

                       fo2=open(filelatest,"ab+")
                       RESULT ="\n# "+str(remoteServerIP)+"          Port  {}    True  ".format(port)+" "+str(localtime)
                       fo1.write(RESULT)
                       fo2.write(RESULT)                    
                       RESULT="" 
                       logger.console(str(remoteServerIP)+"          Port  {}    True  ".format(port)+" "+str(localtime))


                   elif 'Linux' or 'Darwin' in os_platform: 
                       #--------------------------------------- --------------

                       RESULT ="\n# "+str(remoteServerIP)+"          Port  {}    True  ".format(port)+" "+str(localtime)
                       fo1.write(RESULT)
                       fo2.write(RESULT)                    
                       RESULT="" 
                       logger.console(str(remoteServerIP)+"          Port  {}    True  ".format(port)+" "+str(localtime))
                
                c_sessions=c_sessions+1 
                sock.close()   # Close Socket

     
            except KeyboardInterrupt:
                logger.console("You pressed Ctrl+C")
                sys.exit()

            except socket.gaierror:
                logger.console('Hostname could not be resolved. Exiting')
                sys.exit()

            except socket.error:
                # need include socket error timeout and retrun socket error / and coutinue run loop
                if 'Windows' in os_platform:

                     RESULT ="\n# "+str(remoteServerIP)+"          Port  {}    False  ".format(port)+" "+str(localtime)
                     fo1.write(RESULT)
                     fo2.write(RESULT)                    
                     RESULT="" 
                     logger.console(str(remoteServerIP)+"          Port  {}    False  ".format(port)+" "+str(localtime))


                elif 'Linux' or 'Darwin' in os_platform:
                      #--------------------------------------- --------------
                     RESULT ="\n# "+str(remoteServerIP)+"          Port  {}    False  ".format(port)+" "+str(localtime)
                     fo1.write(RESULT)
                     fo2.write(RESULT)                    
                     RESULT="" 
                     logger.console(str(remoteServerIP)+"          Port  {}    False  ".format(port)+" "+str(localtime))
             
        #------------------------------------------------------------------------------------
        fo1.close()    # Close File 1 - History
        fo2.close()    # Close File 2 - Latest log    -------------------------------------      
            
  


        # Checking the time again
        t2 = datetime.now()


        # Calculates the difference of time, to see how long it took to run the script
        total =  t2 - t1
  
        if 'Windows' in os_platform:
                #--------------------------------------- --------------
            filename=curDir+"/"+"TCP-Client.log"
            filelatest=curDir+"/"+"TCP-Client-latest.log"   #Save latest log
            #File name replace role as below:
            #filename=re.sub(r"\\", r"\'", filename) # if have d:/xxx/xxx
            #filename=re.sub(r'//', r"\'", filename) 
            #logger.console filename
            fo1=open(filename,"ab+")
            fo2=open(filelatest,"ab+") 
            #------------------------------------------------
            tclose = datetime.now()   # Record start record time
            ENDTIME="\nEND : ->"+str(tclose)
            logger.console(ENDTIME)  # logger.console start time in monitor
            fo1.write(ENDTIME)
            fo2.write(ENDTIME)

            #--------------------------------------------------

            RESULT ='\nScanning Completed,Current sessions:  '+str(c_sessions)+",toal execute time: "+str(total)
            fo1.write(RESULT)  
            fo2.write(RESULT)                   
            RESULT=""
            fo1.close() 
            fo2.close()

            #---------------------------------------------
            # logger.consoleing the information to screen
            logger.console('\nScanning Completed,Current sessions:  '+str(c_sessions)+",toal execute time: "+str(total)+"\n")

            #--------------------------------------------- 

            #log event as below:
            n=0
            fo2=open(filelatest,"r")

            IP1=""   #Get log ipaddress
            PORT1="" #Get Log Port
            PASS1="" #Get PASS
            TIME1="" #Get Time

            while n <= count:
              n=n+1   
              for line in fo2:
                if '#' in line:
                  IP1=line[1:18]
                  PORT1=line[28:33]
                  PASS1=line[36:42]
                  TIME1=line[43:68]

                  if 'True' in PASS1:
                      TestResult='True'
                      logger.console(TestResult)                      
                      logger.console(line)
                      logger.info(line)

                  else:
                      TestResult='False'
                      logger.console(TestResult) 
                      logger.console(line)
                      logger.info(line)

            fo2.close() 
            DELD=self.CheckStatus(filelatest,True)
            logger.console(TestResult) 
            return TestResult 
           

        elif 'Linux' or 'Darwin' in os_platform: 
            Resvalue1=0  #for PASS Value
            Resvalue2=0  #for Fail Value
            #--------------------------------------- --------------
            filename=curDir+"/"+"TCP-Client.log"  # Log all history
            filelatest=curDir+"/"+"TCP-Client-latest.log"   #Save latest log
            #File name replace role as below:
            #filename=re.sub(r'\\', r'/', filename) # if have d:/xxx/xxx
            #filename=re.sub(r'//', r'\\', filename) # if d:/ or c:/ only
            #logger.console filename
            fo1=open(filename,"ab+")
            fo2=open(filelatest,"ab+")
            
            #------------------------------------------------
            tclose = datetime.now()   # Record start record time
            ENDTIME="\nEND : ->"+str(tclose)
            logger.console(ENDTIME)  # logger.console start time in monitor
            fo1.write(ENDTIME)
            fo2.write(ENDTIME)

            #--------------------------------------------------


            RESULT ='\nScanning Completed,Current sessions: '+str(c_sessions)+",toal execute time: "+str(total)
            fo1.write(RESULT)  
            fo2.write(RESULT)                  
            RESULT="" 
            fo1.close() 
            fo2.close()

            #--------------------------------------
            # logger.consoleing the information to screen
            logger.console('\nScanning Completed,Current sessions:  '+str(c_sessions)+",toal execute time: "+str(total))
            #--------------------------------------

            #log event as below:
            n=0
            fo2=open(filelatest,"r")

            IP1=""   #Get log ipaddress
            PORT1="" #Get Log Port
            PASS1="" #Get PASS
            TIME1="" #Get Time

            while n <= count:
              n=n+1   
              for line in fo2:
                if '#' in line:
                  IP1=line[1:18]
                  PORT1=line[28:33]
                  PASS1=line[36:42]
                  TIME1=line[43:68]

     
                  if 'True' in PASS1:
                      #TestResult='True'
                      #logger.console(TestResult)
                      Resvalue1=Resvalue1+1                      
                      logger.console(line)
                      logger.info(line)


                  else:
                      #TestResult='False'
                      #logger.console(TestResult)
                      Resvalue2=Resvalue2+1 
                      logger.console(line)
                      logger.info(line)

            fo2.close()             
            DELD=self.CheckStatus(filelatest,True)
            #--Feng 20170203 for result 
            if Resvalue2 >=1 and Resvalue1 == 0 :
               TestResult ='False'
            elif Resvalue2 == 0 and Resvalue1 >=1 :
               TestResult ='True'
            elif Resvalue1 >=1 and Resvalue2 >=1 :
               TestResult = 'Partial_PASS'       
            logger.console(TestResult) 
            return TestResult 
#------------------------------------------------------------------------------------------------
  
if __name__ == "__main__":
    #main()
    tcpclient=TCP_Client_init("10.10.10.8",3000,3010)
    tcpclient.client_control()

