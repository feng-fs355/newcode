import paramiko
import os
import sys
import errno
import subprocess
import time
import socket
import traceback

from robot.api import logger
from threading import Timer

class SshControl(object):
    """docstring for UpdateNormal"""
    def __init__(self, ssh_client_host = None, ssh_client_user = None, ssh_client_pwd = None):
        self.ssh_client_host = ssh_client_host
        self.ssh_client_user = ssh_client_user
        self.ssh_client_pwd = ssh_client_pwd

    def command(self, cmd, timeout = 10):
        try:
            return self.ssh_client.exec_command(cmd, timeout = timeout)
        except socket.error, SSHException:
            logger.console("Fuck u error")
            logger.console(traceback.print_stack())
            logger.console(traceback.print_exc())
            logger.console("before connection")
            self.waitForDevice()
            logger.console("after connection")
            self.command(cmd, timeout)
            logger.console("Send command")

    def construct_server(self, protocal, port = None):
        if protocal.lower() == "tcp":
            return self._construct_server_with_tcp(port)
        elif protocal.lower() == "udp":
            return self._construct_server_with_udp(port)

    def _construct_server_with_tcp(self, port):
        if port:
            cmd = 'echo \'%s\'| sudo -S iperf -s -p %s \&' %(self.ssh_client_pwd, str(port))
            check_process = 'iperf -s -p %s' %str(port)
        else:
            cmd = 'echo \'%s\'| sudo -S iperf -s \&' %(self.ssh_client_pwd)
            check_process = 'iperf -s'
        stdin, stdout, stderr = self.command(cmd)
        logger.info(stderr)
        time.sleep(5)
        return self._check_server_costruct_successful(check_process)

    def _construct_server_with_udp(self, port):
        if port:
            cmd = 'echo \'%s\'| sudo -S iperf -s -p %s -u \&' %(self.ssh_client_pwd, str(port))
            check_process = 'iperf -s -p %s -u' %str(port)
        else:
            cmd = 'echo \'%s\'| sudo -S iperf -s -u \&' %(self.ssh_client_pwd)
            check_process = 'iperf -s -u'
        stdin, stdout, stderr = self.command(cmd)
        logger.info(stderr)
        time.sleep(5)
        return self._check_server_costruct_successful(check_process)

    def _check_server_costruct_successful(self, cmd):
        stdin, stdout, stderr = self.command('ps -ef| grep iperf')
        for line in stdout.readlines():
            if cmd in line:
                return True
        return False

    def stop_server(self):
        self.command('echo \'%s\'| sudo -S pkill -9 iperf' %self.ssh_client_pwd)

    def send_mesg_to_server(self, protocal, server_ip, port = None, time_out = 30, trying_times = 5):
        if protocal.lower() == "tcp":
            return self._send_mesg_to_server_through_tcp(server_ip, port, time_out, trying_times)
        elif protocal.lower() == "udp":
            return self._send_mesg_to_server_through_udp(server_ip, port, time_out, trying_times)

    def _send_mesg_to_server_through_tcp(self, server_ip, port, time_out, trying_times):
        for i in range(0, trying_times, 1):
            logger.info("=======")
            try:
                if port:
                    stdin, stdout, stderr = self.command("iperf -c \'%s\' -p %s -i1 -t3" %(server_ip, str(port)), timeout = time_out)
                else:
                    stdin, stdout, stderr = self.command("iperf -c \'%s\' -i1 -t3" %server_ip, timeout = time_out)
                if stdout:
                    for line in stdout.readlines():
                        logger.info(line)
                        if "connected with" in line:
                            logger.info("=======")
                            return True
                time.sleep(1)
                logger.info("Doesn't send messages successful, try again")
                continue
            except socket.timeout:
                time.sleep(1)
                logger.info("Doesn't send messages successful, try again")
                continue
        logger.info("=======")
        return False

    def _send_mesg_to_server_through_udp(self, server_ip, port, time_out, trying_times):
        for i in range(0, trying_times, 1):
            logger.info("=======")
            try:
                if port:
                    stdin, stdout, stderr = self.command("iperf -c \'%s\' -p %s -u -i1 -t3" %(server_ip, str(port)), timeout = time_out)
                else:
                    stdin, stdout, stderr = self.command("iperf -c \'%s\' -u -i1 -t3" %server_ip, timeout = time_out)
                if stdout:
                    for line in stdout.readlines():
                        logger.info(line)
                        if "Server Report" in line:
                            logger.info("=======")
                            return True
                time.sleep(1)
                logger.info("Doesn't send messages successful, try again")
                continue
            except socket.timeout:
                time.sleep(1)
                logger.info("Doesn't send messages successful, try again")
                continue
        logger.info("=======")
        return False

    def check_port_is_open(self, protocal, port, host_ip):
        if protocal.lower() == "tcp":
            stdin, stdout, stderr = self.command("echo %s| sudo -S nmap -p %s -sT %s" %(self.ssh_client_pwd, port, host_ip))
        elif protocal.lower() == "udp":
            stdin, stdout, stderr = self.command("echo %s| sudo -S nmap -p %s -sU %s" %(self.ssh_client_pwd, port, host_ip))
        for line in stdout.readlines():
            if "open" in line:
                return True
        return False

    def createSSHClient(self, server, port, user, password):
        #os.system("ssh-keygen -R %s &> /dev/null"  %server)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        try:
            client.connect(server, port, user, password, timeout = 10)
        except:
            logger.console("SSH failed...")
            return None
        return client

    def CheckConnection(self, host):
        ostype = os.name
        if ostype == "nt":
            response = os.system("ping -n 1 -w 2 %s > /dev/null" %host)
        else:
            response = os.system("ping -c 1 -t 2 %s > /dev/null" %host)
        return response

    def connect(self):
        self.ssh_client = None
        self.client_alive = self.CheckConnection(self.ssh_client_host)
        if (self.client_alive != 0):
            return
        self.ssh_client = self.createSSHClient(self.ssh_client_host, 22, self.ssh_client_user, self.ssh_client_pwd)

    def waitForDevice(self):
        self.client_alive = None
        while True:
            self.connect()
            if self.client_alive == 0 and self.ssh_client:
                break
            time.sleep(5)

    def disconnect_ssh(self):
        self.ssh_client.close()

    def clear_all_ssh_connection(self):
        self.command('echo %s| sudo -S pkill sshd' %self.ssh_client_pwd)
