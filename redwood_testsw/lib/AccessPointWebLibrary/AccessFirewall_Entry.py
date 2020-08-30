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
from smb.SMBHandler import SMBHandler
from ftplib import FTP
from ftplib import error_perm
from threading import Timer
from robot.api import logger
from robot.utils.asserts import *
from random import randint
import FirewallCheck
from sshctrl import NetworkControl



parentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parentdir + "/..")
from AccessPointWebLibrary import AccessPointWebLibrary


#class Firewall_Entry(AccessPointWebLibrary):
class AccessFirewall_Entry(object):

    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

    #def __init__(self,interfaceIP,startport,endport):
    #    self.interfaceIP = interfaceIP
    #    self.startport = startport
    #    self.endport = endport   


    def check_tcpclient(self,interfaceIP,startport,endport,remote_local=None,user=None,password=None,target=None):
        """
         only for local TCP_Client used.
        """
        self.interfaceIP = interfaceIP
        self.startport = startport
        self.endport = endport
        self.remote_local=remote_local
        self.target=target
        self.user=user
        self.password=password

        if self.remote_local == 'L' : 
            """
            If local then get result at local TCP Client
            """
            logger.console("\nStart Local TCP Client\n")
            logger.info("\nStart Local TCP Client\n")
            t2=FirewallCheck.Firewall() 
            result=t2.tcpclient(interfaceIP,startport,endport)  #-> To FirewallCheck.py  
            logger.info("\n get result is : "+result)  # Get test result from TCP_Client_All.py
            logger.console(result)
            return result
        if self.remote_local == 'R' :
            """
            If remote then get result at remote TCP Client
            """
            logger.console("\nStart Remote TCP Client\n")
            logger.info("\nStart Remote TCP Client\n")
            
            #--Entry to sshctrl service as below:
            t3=sshctrl.NetworkControl(interfaceIP,user,password,startport,endport,target)  
            t3.connect()
            result=t3.run_client()
            logger.info(result)
            logger.console("\nTest remote client result is : "+result)
            return result  # return result


        #def check_firewall_udp(self):
    def check_udp(self,interfaceIP,startport,endport):
        """
         only for local TCP_Client used.
        """
        logger.info("\nStart UDP Port Scanner")
        t1=FirewallCheck.Firewall()
        t1.udpclient(interfaceIP,startport,endport)  # -> To FirewallCheck.py     


    
    def run_tcpserver(self,interfaceIP,user,password,startport,endport,remote_local=None):
        #feng add
        """
         For Local TCP_Server == 'L'
         For Remote TCP Server == 'R'
        """

        self.interfaceIP = interfaceIP
        self.user=user
        self.password=password
        self.startport=startport
        self.endport=endport
        self.remote_local=remote_local

        if self.remote_local == 'R':
            
            logger.console("\n--> Select Remote TCP Server\n")
            logger.info("\nTrying to Call ssh function")
            #--Entry to sshctrl service as below:
            time.sleep(3)
            t3=sshctrl.NetworkControl(interfaceIP,user,password,startport,endport)  
            t3.connect()
            res=t3.run_tcpserver()
            logger.info(res)
            logger.console(res)

        if self.remote_local == 'L':
            logger.console("\n\n--> Select Locate TCP Server\n") 
            process=os.system("killall python")            
            logger.info(process)
            time.sleep(3)
            cmd= "python FirewallCheck.py "+str(self.interfaceIP)+" "+str(self.startport)+" "+str(self.endport)+" -S &"
            os.system(cmd)
            logger.info("TCP_Server has been execute.")
            logger.console("TCP_Server has been execute.")
            
       
if __name__ == "__main__":

    Firetest=AccessFirewall_Entry()
    #Firetest.run_tcpserver("127.0.0.1","pap1","12345678","3000","3010","L")
    #Firetest.check_tcpclient("127.0.0.1","3000","3010")


