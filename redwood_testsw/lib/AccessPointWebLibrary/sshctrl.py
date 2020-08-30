import os
import time
import paramiko
import socket

from robot.api import logger
from robot.libraries import Telnet


class NetworkControl(object):
    """Controls Remote TCP Server / TCP Client"""

    def __init__(self, interfaceIP, host_name, host_password,startport=None,endport=None,target=None):
        self.interfaceIP = interfaceIP
        self.host_name = host_name
        self.host_password = host_password
        self.startport=startport
        self.endport=endport
        self.target=target
        logger.console("\n"+str(self.interfaceIP)+" "+str(self.host_name)+" "+str(self.host_password)+" "+str(self.startport)+" "+str(self.endport))



    def connect(self):
        self._check_connection()
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self._ssh.connect(self.interfaceIP, 22, self.host_name, self.host_password)
            logger.console("Successfully ssh to " + self.host_name)
        except paramiko.AuthenticationException:
            logger.console("Authentication problem. Server: " + self.interfaceIP + "\tUser: " \
                    + self.host_name + "\tpassword: " + self.host_password)
            time.sleep(3)
            self.connect()

        except socket.error:
            logger.debug("SSH connect failed, try again")
            time.sleep(3)
            self.connect()


    def sshconnection(self):
        self._check_connection()
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self._ssh.connect(self.interfaceIP, 22, self.host_name, self.host_password)
            logger.console("Successfully ssh to " + self.host_name)
        except paramiko.AuthenticationException:
            logger.console("Authentication problem. Server: " + self.interfaceIP + "\tUser: " \
                           + self.host_name + "\tpassword: " + self.host_password)
            time.sleep(3)
            self.connect()

        except socket.error:
            logger.debug("SSH connect failed, try again")
            time.sleep(3)
            #self.telnetconnection()
            self.connect()
    def close(self):
        self._ssh.close()

    def command(self, cmd, timeout = 120):
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd,timeout = timeout)
            #stdin, stdout, stderr = self._ssh.exec_command(cmd)
            #return stdout.read()
            sshresult=stdout.read()
            logger.console(sshresult)  # print execute result

            if 'True' in sshresult :
                logger.info("You got True !")
                return "True"
            if 'False' in sshresult :
                logger.info("You got False")    
                return "False"
            #return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)

    """
    def send_cmd(self, cmd,timeout = 10):
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd,timeout = timeout)
            #return stdout.read().rstrip()
            sshresult=stdout.read().rstrip()
            logger.console(sshresult)  # print execute result

            if 'True' in sshresult :
                logger.info("You got True !")
                return "True"
            if 'False' in sshresult :
                logger.info("You got False")    
                return "False"
            
        except paramiko.SSHException:
            logger.console("SSH exception from executing command " + cmd)
    """
    
    def run_tcpserver(self):  #feng add
        
        logger.console("\nPrepare run TCP Server")
        #--
        cmd1= "killall python"
        cmd2= "python FirewallCheck.py "+str(self.interfaceIP)+" "+str(self.startport)+" "+str(self.endport)+" -S &"
        logger.info(cmd2)
        logger.console("\nStep1. killall python first") 
        self.command(cmd1)
        time.sleep(1)
        logger.console("\nStep2. killall python again")
        self.command(cmd1)
        time.sleep(1)                 
        logger.console("\nStart Remote TCP Server")
        time.sleep(1)
        return self.command(cmd2)

    def run_client(self):  #feng add 20170206 TBD
        time.sleep(3)
        logger.console("You want to run TCP Client")
        #--
        #-- Tcpclient no need killall ,just for server only.
        #-- Run target use self.target
        cmd2= "python FirewallCheck.py "+str(self.target)+" "+str(self.startport)+" "+str(self.endport)+" -C"
        logger.console("Start Remote TCP Client : / sshctrl.py")
        Res1=self.command(cmd2)
        return Res1   


    def _check_connection(self):
        while 0 != os.system("ping -c 3 %s > /dev/null" % self.interfaceIP):
            logger.console("Pinging to Remote PC...")
            time.sleep(5)



if __name__ == '__main__':
    tester=NetworkControl('10.10.10.8','pap1','12345678')
    tester.connect()
