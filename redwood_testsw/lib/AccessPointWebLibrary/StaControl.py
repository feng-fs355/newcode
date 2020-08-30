import os
import subprocess
import time
import sys
import platform
#feng add ---201612/27
import re
#from netaddr import *  # the machine need pip install netaddr
#import pprint         
#------------------------------
import urllib2
from smb.SMBHandler import SMBHandler
import PortalWebGUICore
from robot.api import logger
from smb.SMBHandler import SMBHandler
from ftplib import FTP
from ftplib import error_perm
from threading import Timer

class StaControl(object):
    
    def __init__(self, wlan, eth, user_pwd, host_ip):
    #--------------------------------------------------------------
    #--default script    
    #def __init__(self, wlan, eth, user_pwd, host_ip):
    #-------------------------------------------------
        self.wlan = wlan
        self.eth = eth
        self.user_pwd = user_pwd
        self.host_ip = host_ip

    def get_terminal_output(self, cmd, timeout_sec = 30, exit_code_flag = False):
        #feng add
        logger.console("\n -->StaControl.py : def get_terminal_output")
        proc = subprocess.Popen("exec " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kill_proc = lambda p: p.kill()
        timer = Timer(timeout_sec, kill_proc, [proc])
        try:
            timer.start()
            stdout,stderr = proc.communicate()

        finally:
            timer.cancel()
            if stdout: logger.info("Standard output: " + stdout)
            if stderr: logger.info("Error output: " + stderr)
            if exit_code_flag:
                exit_code = proc.wait()
                return stdout,stderr, exit_code
            return stdout, stderr

    def get_interface_mac_addr(self, interface):
        mac, err = self.get_terminal_output("ifconfig| grep %s| awk '{ print $5 }'" %interface )
        return mac.split("\n")[0]

    def get_interface_ip_addr(self, interface, expect_status = True, scanning_times = 30, cycle_time = 1):
        #feng add
        logger.console("\n --> PortalWebGUICore.py -> Line 46")
        #---------------------------------------------------------
        for i in range(0, scanning_times, 1):
            ip_address, err = self.get_terminal_output("ifconfig %s| grep \"inet addr\"| awk '{print $2}' " %interface)
            if ip_address != "":
                if expect_status:
                    ip_address = ip_address.split(":")[1]
                    #feng add
                    logger.console(ip_address)
                    break
                else:
                    continue
            if i == scanning_times-1:
                return ip_address, not expect_status                
            time.sleep(cycle_time)
        return ip_address.split("\n")[0], expect_status
        #feng add
        aaa=ip_address.split("\n")[0]
        logger.console ("\n"+"Get PC ip info is : "+aaa)

        #logger.console("\nTo "ip_address)

    def _get_route_ip(self):
        #feng add
        #-----------------------------------------------
        logger.console("\nTring to get router IP from PC")
        return self.get_route_info(2)

    #-----default as below 
    """
    def _get_route_subnet_mask(self):
        #feng add
        logger.console("\nTring to get Router mask from PC")
        #-------------------------------------------------
        return self.get_route_info(3)

    """ 
    #feng add as below:
    def _get_route_subnet_mask(self):
        #feng add
        logger.console("\nTring to get Router mask from PC")
        #-------------------------------------------------
        return self.get_route_info(3)
        #feng add
        
        #domainaddress=""
        #domainmask="" 
        #logger.console("\n line 91 "+ip_address)
       
        #logger.console("\nTring to get Router mask from PC")
        #domain=IPNetwork(ip_address)
        #b=b.netmask
        #b=str(b)
                
        #domainaddress = re.sub("\d{1,3}$","0",ip_address)
        #logger.console("\n The Route Domain address is : "+domainaddress)
        #feng modify as below:
        #will direct transfer ip_address to _get_route_subnet_mask (ex:192.168.0.0)
        
        #-------------------------------------------------
        #return self.get_route_info(3)

    def get_route_info(self, select):


        for i in range(0, 30, 1):

            if select == 2:
               ip_address, err = self.get_terminal_output("netstat -rn| grep %s| awk '{print $%s}'" %(self.eth, select))
               if ip_address != "":
                 ip_address = ip_address.splitlines()[select-2] 
                 logger.console(type(ip_address))               
                 logger.console("The Router IP address is :"+ip_address)
                 if "0.0.0.0" not in ip_address:
                    break
               time.sleep(1)   
            if select == 3:
               ip_address, err =self.get_terminal_output("ifconfig %s | grep Mask | cut -d ':' -f4" %(self.eth))
               logger.console("get router mask")
               logger.console(type(ip_address)) 
             
               if ip_address != "":
                 ip_address = ip_address.strip()        
                 logger.console("\n"+ip_address)
                 if "0.0.0.0" not in ip_address:
                    break
               time.sleep(1)
            

        return ip_address

    #--------------------------------------------------------
    
    # The default script as below:
    #-------------------------------------------------------------------------
    """
    def get_route_info(self, select):
        for i in range(0, 30, 1):
            ip_address, err = self.get_terminal_output("netstat -rn| grep %s| awk '{print $%s}'" %(self.eth, select))
            if ip_address != "":
                #ip_address = ip_address.splitlines()[select-2]
                
                #feng add as below
                # pending for ip 192.192.192.1 issue / 
                ip_address = ip_address.splitlines()[select-2]
                #feng add
                print "\n"
                logger.console(ip_address)
                if "0.0.0.0" not in ip_address:
                    break
            time.sleep(1)
        return ip_address
    """    
    #-------------------------------------------------------------------------------
    def _assign_eth_ip_address(self, ip_address, subnet_mask):
        #feng add
        logger.console("\n -> StaControl.py line 78 / Assign ip address")
        print "\n"
        #logger.console(self.eth)
        print "\n"
        #----------------------------------------------------------------------------------------------------    
        #feng add 2016/12/28
        # Interface eth restart as below:
        #--------------------------------------------------
        logger.console("\nRestart Network manager first,please wait for 20 sec")
        os.system("echo %s| sudo service network-manager restart" %(self.user_pwd))
        time.sleep(20) #restart eth as 20sec
        # no need -> restart network manager
        #-------------------------------------------------
        #----------------------------------------------------------------------
        #feng
        
        #-----default assign ip address as below:
        os.system("echo %s| sudo -S ip a add %s/%s dev %s" %(self.user_pwd, ip_address, subnet_mask, self.eth))

    def _remove_eth_ip_address(self, ip_address, subnet_mask):
        #feng add
        logger.console("\nRemove_eth_ip_address -> line 119 -> StaControl.py")
        #need add action in robot file (20161226),will talk to ivan
        #----------------------------------------------------------------------------------

        os.system("echo %s| sudo -S ip a delete %s/%s dev %s" %(self.user_pwd, ip_address, subnet_mask, self.eth))

    def remove_file(self):
        os.system('rm large_file')
        os.system('rm small_file')

    def create_large_file(self):
        if str(platform.system()) == 'Linux':
            os.system('fallocate -l 1G large_file')
        elif str(platform.system()) == 'Darwin':
            os.system('mkfile -n 1g large_file')

    def create_small_file(self):
        if str(platform.system()) == 'Linux':
            os.system('fallocate -l 10M small_file')
        elif str(platform.system()) == 'Darwin':
            os.system('mkfile -n 10m small_file')

    def block_until_cable_connect(self):
        #feng Add
        logger.console("\n -->In StaControl.py line 102")
        
        while True:
            stdout, stderr = self.get_terminal_output("echo %s| sudo -S ethtool %s| grep Link| awk '{print $3}'" %(self.user_pwd, self.eth))
            if "yes" in stdout:
                break
            logger.info("Block until cable connect")
            time.sleep(1)

    def enable_wifi(self):
        if 'darwin' == sys.platform:
            os.system("networksetup -setairportpower en0 on")
        else:
            os.system("nmcli radio wifi on")

    def disable_wifi(self):
        if 'darwin' == sys.platform:
            os.system("networksetup -setairportpower en0 off")
        else:
            os.system("nmcli radio wifi off")

    def _enable_interface(self, interface):
        os.system("echo \'%s\'| sudo -S ifconfig %s up" %(self.user_pwd, interface))

    def _disable_interface(self, interface):
        #feng add
        logger.console("\n --> Sta Controll.py : def _disable_interface")
        os.system("echo \'%s\'| sudo -S ifconfig %s down" %(self.user_pwd, interface))

    def _scan_ssid(self, ssid, is_scan, scanning_times = 1, cycle_time = 0):
        logger.info("Trying to scan %s" %ssid)
        for i in range(0, scanning_times, 1):
            logger.info("Sannning %sth times" %str(i))
            out, err = self.get_terminal_output("echo \'%s\' |sudo -S iw %s scan |grep -F \'%s\'"
                %(self.user_pwd, self.wlan, ssid))
            if err !="":
                time.sleep(5)
                logger.info("Try again..")
                i = i - 1
            elif out != "":
                if is_scan:
                    break
                else:
                    continue
            if i == scanning_times-1:
                return not is_scan
            time.sleep(cycle_time)
            logger.info("Can't find the ssid, try again")
        return is_scan

    '''
    def _scan_mode(self, encryption, ssid, scanning_times = 1, cycle_time = 0):
        logger.console("\nScanning SSID: " + ssid + "...")
        for i in range(1, scanning_times + 1, 1):
            logger.console("---Scanninng %dth times---" %i)
            self.disable_wifi()
            time.sleep(5)
            self.enable_wifi()

            out, err = self.get_terminal_output("nmcli -f all dev wifi | grep %s | awk '{ print $9 }'"
                %(ssid))
            if out == encryption:
                break
            if i == scanning_times:
                raise Exception("Wrong mode!")
            time.sleep(cycle_time)
        logger.console("Successful!\n")
    '''

    def _connect_wifi(self, ssid, pwd = None):
        logger.info("Trying to connect SSID:" + ssid)
        if pwd :
            isConnect = os.system("nmcli d wifi connect \'%s\' password \'%s\' iface %s " %(ssid, pwd, self.wlan))
        else :
            isConnect = os.system("nmcli d wifi connect \'%s\' iface \'%s\' " %(ssid, self.wlan))
        logger.console(isConnect)
        if isConnect != 0:
            os.system("echo %s| sudo -S service network-manager restart > /dev/null" %self.user_pwd)
            time.sleep(10)
            self._disconnect_wifi(ssid)
            self._delete_wifi_record(ssid)
            return False
        return True

    def _disconnect_wifi(self, ssid):
        os.system("nmcli d disconnect iface %s" %self.wlan)
        time.sleep(2)

    def _delete_wifi_record(self, ssid):
        os.system("nmcli c delete id \'%s\'" %ssid)
        time.sleep(5)  # 20170127 Feng change 2 to 5

    def ping_check(self, address):
        # feng add
        logger.console("\n ping check "+address+" -->StaControl.py  line 193")
        logger.info("Trying to ping %s ..." %address)
        #feng
        print "ping_check\n"
        #logger.console(address)
        if 'darwin' == sys.platform:
            #output, err = self.get_terminal_output("ping -c 5 -t 5 %s  | grep 'received' | cut -d ' ' -f 4" %(address))
            #--feng add 20170127 test via pppoe and modiify
            output, err = self.get_terminal_output("ping -c 5 -t 20 %s  | grep 'received' | cut -d ' ' -f 4" %(address))
        else:
            #output, err = self.get_terminal_output("ping -c 5 -w 5 %s  | grep 'received' | cut -d ' ' -f 4" %(address))
            #--feng add 20170127 test via pppoe and modiify
            output, err = self.get_terminal_output("ping -c 5 -w 20 %s  | grep 'received' | cut -d ' ' -f 4" %(address))
        logger.info("Ping result: " + output)
        output = output.split("\n")[0]
        if output == "" or int(output) < 2:  # Error control: Allow to fail 1/5 times
            return False
        return True

    def samba_upload(self, usb_id, upload_file, username, password):
        #feng add 20170202
        logger.console(upload_file)
        #----------------------------
        local_file = open(upload_file)
        director = urllib2.build_opener(SMBHandler)
        fh = local_file  # init to prevent 'reference before assignment'
        try:
            logger.console("\nhost ip : "+self.host_ip)
            # have issue as below 20170202
            #fh = director.open('smb://%s:%s@%s/usb-%s/%s' %(username, password, self.host_ip, str(usb_id), upload_file), data=local_file)
            #------------------------------------------------------------------------------------------------------------------------------
            fh = director.open('smb://admin:password@192.168.8.1/portal/usb-'+str(usb_id)+'/'+upload_file, data=local_file)
            logger.console("\nHas been upload file to samba server") 
        except urllib2.URLError:
            logger.error("URLError in samba upload, usb id: " + str(usb_id) + ", upload file: " + str(upload_file) + ". USB probably not detected correctly")
        

        fh.close()

    def samba_download(self, usb_id, download_file):
        director = urllib2.build_opener(SMBHandler)
        fh = None # prevent reference before assignment
        try:
            fh = director.open('smb://admin:password@192.168.8.1/usb-' + str(usb_id) + '/' + download_file)
            #feng add 20170126
            time.sleep(10) 
        except urllib2.URLError:
            logger.error("URLError in samba download, usb id: " + str(usb_id) + ", download file: " + str(download_file) + ". USB probably not detected correctly")
        if fh:
            print type(fh)
            save_file = open(download_file, 'w')
            save_file.write(fh)
            fh.close()

    def upload_file_ftp(self, usb_id, filename, username, password):
        local_f = open(filename, 'rb')
        try:
            ftp = FTP(self.host_ip, username, password)
            ftp.cwd('usb-' + str(usb_id))
            ftp.storbinary('STOR %s' %filename, local_f)
        except ftplib.error_perm:
            logger.error("550 Failed to change directory, usb id: " + str(usb_id) + " filename: " + str(filename) + " usr:pass: " + username + ":" + password + ". USB probably not detected correctly")
            #--feng add 20170202
            logger.console("550 Failed to change directory, usb id: " + str(usb_id) + " filename: " + str(filename) + " usr:pass: " + username + ":" + password + ". USB probably not detected correctly")
        ftp.close()

    def _download_file_ftp(self, usb_id, filename, username, password):
        local_f = open(filename, 'wb')
        ftp = FTP(self.host_ip, username, password)
        ftp.cwd('usb-' + str(usb_id))
        ftp.retrbinary('RETR %s' %filename, local_f)
        ftp.close()

    def construct_server(self, protocal, port = None):
        if protocal.lower() == "tcp":
            return self._construct_server_with_tcp(port)
        elif protocal.lower() == "udp":
            return self._construct_server_with_udp(port)

    def _construct_server_with_tcp(self, port):
        if port:
            cmd = 'echo \'%s\'| sudo -S iperf -s -p %s > /dev/null &' %(self.user_pwd, str(port))
            check_process = 'iperf -s -p %s' %port
        else:
            cmd = 'echo \'%s\'| sudo -S iperf -s > /dev/null &' %(self.user_pwd)
            check_process = 'iperf -s'
        return_code = os.system(cmd)
        time.sleep(5)
        if return_code != 0:
            logger.console("Construct TCP server failed, try again")
            self.stop_server()
            self._construct_server_with_tcp(port)
        return self._check_server_costruct_successful(check_process)

    def _construct_server_with_udp(self, port):
        if port:
            cmd = 'echo \'%s\'| sudo -S iperf -s -p %s -u > /dev/null &' %(self.user_pwd, str(port))
            check_process = 'iperf -s -p %s -u' %port
        else:
            cmd = 'echo \'%s\'| sudo -S iperf -s -u > /dev/null &' %(self.user_pwd)
            check_process = 'iperf -s -u'
        return_code = os.system(cmd)
        time.sleep(5)
        if return_code != 0:
            logger.console("Construct UDP server failed, try again")
            self.stop_server()
            self._construct_server_with_udp(port)
        return self._check_server_costruct_successful(check_process)

    def _check_server_costruct_successful(self, cmd):
        stdout, stderr = self.get_terminal_output('ps -ef| grep iperf')
        if cmd in stdout:
            return True
        return False

    def stop_server(self):
        os.system('echo \'%s\'| sudo -S pkill -9 iperf' %self.user_pwd)

    def send_mesg_to_server(self, protocal, server_ip, port = None, time_out = 30, trying_times = 5):
        if protocal.lower() == "tcp":
            return self._send_mesg_to_server_through_tcp(server_ip, port, time_out, trying_times)
        elif protocal.lower() == "udp":
            return self._send_mesg_to_server_through_udp(server_ip, port, time_out, trying_times)

    def _send_mesg_to_server_through_tcp(self, server_ip, port, time_out, trying_times):
        for i in range(0, trying_times, 1):
            logger.info("=======")
            if port:
                outs, errs = self.get_terminal_output("iperf -c \'%s\' -p %s -i1 -t3" %(server_ip, str(port)), time_out)
            else:
                outs, errs = self.get_terminal_output("iperf -c \'%s\' -i1 -t3" %server_ip, time_out)
            logger.info(outs)
            if outs:
                if "connected with" in outs:
                    logger.info("=======")
                    return True
            time.sleep(1)
            logger.info("Doesn't send messages successful, try again")
            continue
        logger.info("=======")
        return False

    def _send_mesg_to_server_through_udp(self, server_ip, port, time_out, trying_times):
        for i in range(0, trying_times, 1):
            logger.info("=======")
            if port:
                outs, errs = self.get_terminal_output("iperf -c \'%s\' -p %s -u -i1 -t3" %(server_ip, str(port)), time_out)
            else:
                outs, errs = self.get_terminal_output("iperf -c \'%s\' -u -i1 -t3" %server_ip, time_out)
            logger.info(outs)
            if outs:
                if "Server Report" in outs:
                    logger.info("=======")
                    return True
            time.sleep(1)
            logger.info("Doesn't send messages successful, try again")
            continue
        logger.info("=======")
        return False

    def check_port_is_open(self, protocal, port, host_ip):
        if protocal.lower() == "tcp":
            outs, errs = self.get_terminal_output("echo %s| sudo -S nmap -p %s -sT %s" %(self.user_pwd, port, host_ip))
        elif protocal.lower() == "udp":
            outs, errs = self.get_terminal_output("echo %s| sudo -S nmap -p %s -sU %s" %(self.user_pwd, port, host_ip))
        if "open" in outs:
            return True
        return False

    def create_virtual_interface(self, name, mac_address):
        #print "\ncreate"
        os.system('echo %s| sudo -S ip link add name %s address %s link %s type macvlan' %(self.user_pwd, name, mac_address, self.eth))
        #os.system('echo %s| sudo -S ip link set %s up' %(self.user_pwd, name))

    def remove_virtual_interface(self, name):
        #print "\nremove"
        os.system('echo %s| sudo -S sudo ip link delete dev %s' %(self.user_pwd, name))

    def dhcp_lease(self, name):
        #print "\nlease"
        print os.system('echo %s| sudo -S dhclient %s' %(self.user_pwd, name))
        time.sleep(5)

    def dhcp_release(self, name):
        #print "\nrelease"
        os.system('echo %s| sudo -S dhclient -r %s' %(self.user_pwd, name))

    def check_dhcp_lease(self, name):
        print "\ncheck"
        out, err = self.get_interface_ip_addr(name, True, 5, 1)
        if "192.168.8" not in out :
            return False
        return True

    def configure_virtual_lease(self, start, end):
        interface_list = []
        interface_str = ""

        for i in range(start, end):
            print "\n==== " + str(i) + " ===="
            mac_address = "00:01:02:03:04:%x" %i
            tmp_str = "v" + str(i)
            interface_str = interface_str + " " + tmp_str
            interface_list.append(tmp_str)
            tester.create_virtual_interface(tmp_str, mac_address)
            tester._enable_interface(tmp_str)

        print "Lease IP"
        print interface_str
        tester.dhcp_lease(interface_str)

    def reset_virtual_interface(self, name):
        mac_address = self.get_interface_mac_addr(name)
        tester.dhcp_release(tmp_str)
        tester.remove_virtual_interface(tmp_str)
        tester.create_virtual_interface(tmp_str, mac_address)
        tester._enable_interface(tmp_str)

if __name__ == '__main__':
    #feng add as below 1227
    tester = StaControl("wlan0", "eth0", "idltest", "192.168.8.1")
    #------------------------------------------------------------
    #--default 
    #tester = StaControl("wlan0", "eth0", "idltest", "192.168.8.1")
    #----------
    """
    tester.configure_virtual_lease(1, 50)
    tester.configure_virtual_lease(50, 100)
    tester.configure_virtual_lease(100, 150)
    tester.configure_virtual_lease(150, 200)
    tester.configure_virtual_lease(200, 250)
    """

    file = open('test_lease.log', 'w')
    file.write('')
    '''

    lease_count = 250
    lease_pair = 30
    a = 1
    b = lease_pair
    for i in range(1, lease_count/lease_pair + 2, 1):
        tester.configure_virtual_lease(a, b)
        a = b
        b = a + lease_pair
        if b >=lease_count:
            b = lease_count + 1

    for i in range(1, 250):
        tmp_str = "v" + str(i)
        print "\n==== " + str(i) + " ===="
        if not tester.check_dhcp_lease(tmp_str):
            print "Try to lease IP again"
            tester.reset_virtual_interface(tmp_str)
            tester.dhcp_lease(tmp_str)
            if not tester.check_dhcp_lease(tmp_str):
                file.write("\n" + str(i))
                file.write("\nCan't lease IP successful")
                print "Can't lease IP successful"
    file.close()
    '''
    interface_str = " v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 v11 v12 v13 v14 v15 v16 v17 v18 v19 v20 v21 v22 v23 v24 v25 v26 v27 v28 v29 v30 v31 v32 v33 v34 v35 v36 v37 v38 v39 v40 v41 v42 v43 v44 v45 v46 v47 v48 v49 v50 v51 v52 v53 v54 v55 v56 v57 v58 v59 v60 v61 v62 v63 v64 v65 v66 v67 v68 v69 v70 v71 v72 v73 v74 v75 v76 v77 v78 v79 v80 v81 v82 v83 v84 v85 v86 v87 v88 v89 v90 v91 v92 v93 v94 v95 v96 v97 v98 v99 v100 v101 v102 v103 v104 v105 v106 v107 v108 v109 v110 v111 v112 v113 v114 v115 v116 v117 v118 v119 v120 v121 v122 v123 v124 v125 v126 v127 v128 v129 v130 v131 v132 v133 v134 v135 v136 v137 v138 v139 v140 v141 v142 v143 v144 v145 v146 v147 v148 v149 v150 v151 v152 v153 v154 v155 v156 v157 v158 v159 v160 v161 v162 v163 v164 v165 v166 v167 v168 v169 v170 v171 v172 v173 v174 v175 v176 v177 v178 v179 v180 v181 v182 v183 v184 v185 v186 v187 v188 v189 v190 v191 v192 v193 v194 v195 v196 v197 v198 v199"
    print "Release IP"
    tester.dhcp_release(interface_str)
    for i in range(0, 252):
        print "\n==== " + str(i) + " ===="
        #tmp_str = interface_list[i]
        tmp_str = "v" + str(i)
        #tester.dhcp_release(tmp_str)
        tester.remove_virtual_interface(tmp_str)

    #tester._remove_eth_ip_address("192.168.8.125", "255.255.255.0")
