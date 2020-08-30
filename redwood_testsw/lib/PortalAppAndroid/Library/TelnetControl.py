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

class TelnetControl(object):
    def __init__(self,host):
        self.host = host
        self.User = "root"
        self.Password = "CassiniRedwwod42562072Portal"
    def connect(self):
        tn = telnetlib.Telnet(self.host)
        tn.read_until("login: ")
        tn.write(self.User  + "\n")
        if self.Password:
            tn.read_until("Password: ")
            tn.write(self.Password + "\n")
        tn.read_until("root@OpenWrt:~# ")
        tn.write("ifconfig\n")
        print tn.read_until("root")
        tn.close()
        
    def get_meshap_ip(self,meshapmac):
        tn = telnetlib.Telnet(self.host)
        tn.read_until("login: ")
        tn.write(self.User  + "\n")
        meshap_ip=[]
        if self.Password:
            tn.read_until("Password: ")
            tn.write(self.Password + "\n")
        tn.read_until("root@OpenWrt:~# ")
        tn.write("cat /proc/net/arp | grep "+ meshapmac +" | awk '{print $1}'\n")
        meshap_ip = tn.read_until("root")
        #print meshap_ip[51:64]
        return meshap_ip[51:64]
    
    def disable_lan_port(self,port_num):
        tn = telnetlib.Telnet(self.host)
        tn.read_until("login: ")
        tn.write(self.User  + "\n")
        if self.Password:
            tn.read_until("Password: ")
            tn.write(self.Password + "\n")
        tn.read_until("root@OpenWrt:~# ")
        tn.write("ssdk_sh debug phy set "+port_num+" 0 0x800\n")
        print tn.read_until("root")
        tn.close()   
    
    def enable_lan_port(self,port_num):
        tn = telnetlib.Telnet(self.host)
        tn.read_until("login: ")
        tn.write(self.User  + "\n")
        if self.Password:
            tn.read_until("Password: ")
            tn.write(self.Password + "\n")
        tn.read_until("root@OpenWrt:~# ")
        tn.write("ssdk_sh debug phy set "+port_num+" 0 0x9000\n")
        print tn.read_until("root")
        tn.close()  

    def factory_reset(self):
        tn = telnetlib.Telnet(self.host)
        tn.read_until("login: ")
        tn.write(self.User  + "\n")
        if self.Password:
            tn.read_until("Password: ")
            tn.write(self.Password + "\n")
        tn.read_until("root@OpenWrt:~# ")
        tn.write("firstboot\n")
        print tn.read_until("y]")
        tn.write("y\n")
        print tn.read_until("~#")
        tn.write("reboot\n")
        print tn.read_until("~#")
        tn.close()
        
        
    def disconnect(self):
        tn = telnetlib.Telnet(self.host)
        tn.close()
        
if __name__ == '__main__':
    meship = ""
    telnet = TelnetControl("192.168.8.1")
    #telnet.get_meshap_ip("14:00")
    meship = telnet.get_meshap_ip("1a:a0")
    print meship
    telnetmesh = TelnetControl(meship)
    telnetmesh.connect()
    #telnet.factory_rest()
