import atexit
import md5
import sys
import re
import paramiko
from robot.libraries import Telnet
from robot.api import logger
import paramiko
import os
import errno
import subprocess
import time
import socket
import traceback
from threading import Timer

#---Feng modify Telnet to SSH --20170208

class OpenWrtCore(object):

    def __init__(self):
        # logger.console("create new Telnet")
        #self._tc = Telnet.Telnet()

        logger.console("create new ssh / SSH")

   
  
    def _connect(self, host = None, prompt = None, user = None, password = None):

        self.host=host
        self.prompt=prompt
        self.user=user
        self.password=password
        self._check_connection()
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self._ssh.connect(self.host, 22, self.user, self.password)
            logger.console("Successfully ssh to " + self.user)
        except paramiko.AuthenticationException:
            logger.console("Authentication problem. Server: " + self.host + "\tUser: " \
                    + self.user + "\tpassword: " + self.password)
            time.sleep(3)
            self._connect()

        except socket.error:
            logger.debug("SSH connect failed, try again")
            time.sleep(3)
            self._connect()


    def _check_connection(self):
        while 0 != os.system("ping -c 3 %s > /dev/null" % self.host):
            logger.console("Pinging to Remote PC...")
            time.sleep(5)


    #def _connect(self, host = None, prompt = None, user = None, password = None):
    #    try:
    #        self._tc.open_connection(host, prompt=prompt)
    #        if (user is not None):
    #            logger.info("try to login with:"+user+":"+password)
    #            # logger.info("prompt: "+prompt)
    #            self._tc.login(user, password, login_timeout="5 second")
    #        else:
    #            self._tc.read_until_prompt()
    #    except Exception, e:
    #        logger.console(e)
    #        #raise OpenWrtError('Telnet connection failed')

    def _send_cmd(self, cmd, timeout = 10):
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd,timeout = timeout)
            sshresult=stdout.read()
            logger.console(sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)


    #def _send_cmd(self, cmd):
    #    return self._tc.execute_command(cmd).splitlines()[0]

    def _set_ssid(self, ssid):
        cmd = ""
        #self._result = self._tc.execute_command(cmd)
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("set ssid : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)

    def _get_mac_address(self):
        cmd = "ifconfig | grep eth0 | awk '{ print $5 }'"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get mac : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)



        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_ssid(self, iface):
        cmd = "uci get wireless.@wifi-iface["+str(iface)+"].ssid"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get ssid : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)

        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_encryption(self, iface):
        cmd = "uci get wireless.@wifi-iface[" + str(iface) + "].encryption"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get encryption : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_password(self, iface):
        cmd = "uci get wireless.@wifi-iface[" + str(iface) + "].key"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get password : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_ssid_is_broadcast(self, iface):
        cmd = "uci get wireless.@wifi-iface[" + str(iface) + "].hidden"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get ssid is broadcast : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)        
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_ipaddr(self):
        cmd = "uci -P/var/state get network.wan.ipaddr"
        
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan ipaddr : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_gateway(self):
        cmd = "uci -P/var/state get network.wan.gateway"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan gateway : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)        
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_netmask(self):
        cmd = "uci -P/var/state get network.wan.netmask"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan netmask : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd) 
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_cpuinfo(self):
        cmd = "cat /proc/cpuinfo"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get cpuinfo : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)         
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_version(self):
        cmd = "cat /proc/version"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get version : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd) 
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_mode(self):
        cmd = "uci get network.wan.proto"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan mode : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)         
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_username(self):
        cmd = "uci -P/var/state get network.wan.username"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan username : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)         
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_password(self):
        cmd = "uci -P/var/state get network.wan.password"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan password : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)         
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_wan_service(self):
        cmd = "uci -P/var/state get network.wan.service"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get wan service : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)         
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _get_dns(self):
        """ TODO get dns server names <<VERIFY is correct>>
        """
        cmd = "uci -P/var/state get network.wan.dns"
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get dns : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd) 
        #return self._tc.execute_command(cmd).splitlines()[0]

    def _check_file(self, usb_id, filename):
        """ Checks if a file exits in usb slot
        returns true if found
        """
        cmd = "ls /mnt/usb-%s| grep %s" %(usb_id, filename)
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("get check file : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd) 
        #return filename == self._tc.execute_command(cmd).splitlines()[0]

    def _delete_file(self, usb_id, filename):

        cmd = "rm /mnt/usb-%s/%s" %(usb_id, filename)
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            sshresult=stdout.read()
            logger.console("delete file : "+sshresult)  # print execute result
            return stdout.read()

        except socket.error, SSHException:
            pass
            logger.console("SSH exception from executing command " + cmd)         

        #self._tc.execute_command(cmd)

    def compute_default_info(self):
        tmp = self._get_mac_address()
        result = re.search('(([A-Fa-f0-9]{2}):?([A-Fa-f0-9]{2}):?([A-Fa-f0-9]{2}):?([A-Fa-f0-9]{2}):?([A-Fa-f0-9]{2}):?([A-Fa-f0-9]{2}))', tmp)
        if not result:
            print "Wrong MacAddress format"
            sys.exit(1)
        macaddr = (result.group(2)+result.group(3)+result.group(4)+result.group(5)+result.group(6)+result.group(7)).lower()
        ssidpostfix=str.format("%04d" % ((int(macaddr[6:12],16))%10000))
        m=md5.new();
        m.update(macaddr);
        password=m.hexdigest()
        return "PORTAL_"+ssidpostfix, "PORTAL_FASTLANE_"+ssidpostfix, password[:8]

    @atexit.register
    def goodbye():
        print "You are now leaving the Python sector."


if __name__ == '__main__':
    tester = OpenWrtCore()
    tester._connect('192.168.8.1', '~#', 'root', 'CassiniRedwwod42562072Portal')
    print tester._check_file(1, 'local_file_FTP.log')


class OpenWrtError(Exception):
    pass
