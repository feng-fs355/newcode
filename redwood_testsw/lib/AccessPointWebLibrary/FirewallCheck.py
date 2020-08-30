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
import unittest
from TCP_Server import TCP_Server_init
from TCP_Client_ALL import TCP_Client_init
from UDP_Client import UDP_Client_init
import sshctrl
import urllib2
#from smb.SMBHandler import SMBHandler
#import PortalWebGUICore  # 12/30 Not include robot frame now,just remark
#from robot.api import logger
#from smb.SMBHandler import SMBHandler
from ftplib import FTP
from ftplib import error_perm
from threading import Timer



from robot.api import logger
from robot.utils.asserts import *

from random import randint


#----TBD--Need reapir at 12/30

class Firewall(object):   

    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

   # def tcpclient(self,interfaceIP,startport,endport,ftpserver):
    def tcpclient(self,interfaceIP,startport,endport):
        self.interfaceIP=interfaceIP
        self.startport=startport
        self.endport=endport
        #self.expect_result=expect_result
        #self.ftpserver=ftpserver
        #test1=TCP_Client_init(self.interfaceIP,self.startport,self.endport,self.ftpserver)
        test1=TCP_Client_init(self.interfaceIP,self.startport,self.endport)
        result=test1.client_control()
        print result
        return result

    #- 20170206 feng remark ,for local TCP Server
    def tcpserver(self,interfaceIP,startport,endport):
        self.interfaceIP=interfaceIP
        self.startport=startport
        self.endport=endport 
        test2=TCP_Server_init(self.interfaceIP,self.startport,self.endport)
        test2.server_control()       
    
    def udpclient(self,interfaceIP,startport,endport):
        self.interfaceIP=interfaceIP
        self.startport=startport
        self.endport=endport 
        test3=UDP_Client_init(self.interfaceIP,self.startport,self.endport)
        test3.udpclient_control()
             

            
#---------------------------------------------------------------------
if __name__ == "__main__":



    v = sys.argv
    #logger.console v
    """
    v[1]: interfaceIP
    v[2]: startport
    v[3]: endport
    v[4]: mode  # define server mode or client mode
    v[5]: FTP Server address
    v[6]: TBD
    """
    try:   
  
      v[1]=str(sys.argv[1])     

      v[2]=str(sys.argv[2])
            
      v[3]=str(sys.argv[3])            

      v[4]=str(sys.argv[4])

      #v[5]=str(sys.argv[5])
    except:
      logger.console("\n Warring !,The argumment 1 is IP-Address, argument 2 is Start-port , argument 3 is End-Port")

      #logger.console "\n argument 4 is Mode Selection , argument 5 is ftp server address"
      logger.console("\n argument 4 is Mode Selection ")
      sys.exit()  
    
    Firtest=Firewall()

    """
    if v[4] == '-C' :
       logger.console "You select Client mode"
       Firtest.tcpclient(v[1],v[2],v[3],v[5]) 
    """   

    if v[4] == '-C' :
       #logger.console("You select Client mode")
       Firtest.tcpclient(v[1],v[2],v[3])    
       


    if v[4] == '-S' :
       #logger.console("You select Sever mode")
       Firtest.tcpserver(v[1],v[2],v[3])   

    if v[4] == '-U' :
       #logger.console("You select UDP Port Scanner")
       Firtest.udpclient(v[1],v[2],v[3])  
       #Client mode has been ready (2017/1/3)

    #Firtest.tcpserver(v[1],v[2],v[3])
    #v = sys.argv
    #logger.console v
    """
    v[1]: UUID
    v[2]: port
    v[3]: bootstrapPort
    v[4]: Portal-ID
    v[5]: customize password
    v[6]: iteration
    """
    #tester = PortalAPPTests(v[1], int(v[2]), int(v[3]), v[4], v[4] + "-auto", v[5])
    #tester.OnBoardStress(int(v[6]))

