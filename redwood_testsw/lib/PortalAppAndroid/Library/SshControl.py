import os
import sys
import time
import urllib2
import re
import paramiko
from paramiko import client
from paramiko import SSHClient
from scp import SCPClient
import getpass
import telnetlib

class SshControl(object):
    def __init__(self, ssh_client_host = None, ssh_client_user = None, ssh_client_pwd = None):
        self.ssh_client_host = ssh_client_host
        self.ssh_client_user = ssh_client_user
        self.ssh_client_pwd = ssh_client_pwd
    
    def command(self, cmd, timeout = 10):
        try:
            return self.ssh_client.exec_command(cmd, timeout = timeout)
        except Exception, e:
            print (e)
            time.sleep(5)
            self.waitForDevice()
            self.command(cmd, timeout)
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(self.ssh_client_host, 22,  self.ssh_client_user, self.ssh_client_pwd)
    def send_command(self,cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        print stdout.readlines()
        print stderr.readlines()
        
if __name__ == '__main__':
    ssh = SshControl("192.168.8.1", "root", "CassiniRedwwod42562072Portal")
    print "connect 192.168.8.1"
    ssh.connect()
    ssh.send_command("ls")
    ssh.send_command("firstboot")
    ssh.send_command("y")