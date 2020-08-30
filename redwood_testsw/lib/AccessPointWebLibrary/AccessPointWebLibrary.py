import os
import sys
import unittest
import time


from OpenWrtCore import OpenWrtCore, OpenWrtError
from PortalWebGUICore import PortalWebGUICore
from StaControl import StaControl
from SshControl import SshControl
from robot.api import logger
from robot.utils.asserts import *

from random import randint



class AccessPointWebLibrary(object):
    """Test library for testing *PortalWebCore* commands.

    Interacts with the access point via ssh, and using OpenWrt api method.
    20170208 Feng modify to ssh
    """

    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

    def init_variable(self, eth, wlan, user_pwd, router_ip, ssh_client_host = None, ssh_client_user = None, ssh_client_pwd = None):
        self._eth = eth
        self._wlan = wlan
        self._user_pwd = user_pwd
        self._router_ip = router_ip
        self._ssh_client_host = ssh_client_host
        self._ssh_client_user = ssh_client_user
        self._ssh_client_pwd = ssh_client_pwd
        self._openwrtcore = OpenWrtCore()
        self._portalwebguicore = PortalWebGUICore()
        self._stacontrol = StaControl(self._wlan, self._eth, self._user_pwd, self._router_ip,)
        self._sshcontrol = SshControl(self._ssh_client_host, self._ssh_client_user, self._ssh_client_pwd)
        self._result = ''

    
    def create_ssh_connection(self, host="127.0.0.1", prompt='~$', user=None, password=None):

    #def create_ssh_connection(self, host='127.0.0.1', prompt='~$', user=None, password=None):
        """Create ssh connection to access point. ``mandotory``

        connect to given host using robot ssh library

        Examples:
        | Create ssh Connection | 192.168.1.1 | /# |
        | Create ssh Connection | 192.168.1.1 | /# | root | root |
        """
        logger.info("\nCreating ssh connection to " + user + ":" + password)
        self._openwrtcore._connect(host, prompt, user, password)

    def open_website(self, url, title, pwd):
        #feng
        logger.console("\n --/AccessPointWebLibrary.py / def open_website")
        logger.console(url)
        logger.info("Opening website to" + url + ":" + title + ":" + pwd)
        return self._portalwebguicore.open_website("http://" + url, title, pwd)

    def close_website(self):
        #feng add
        logger.console("\n --> AccessPointWebLibrary.py  /  def close_website")
        self._portalwebguicore._close()

    def apply(self):
        logger.console("Apply , in the AccessPointWebLibrary  /  def apply\n")
        self._portalwebguicore._apply();

    def send_cmd(self, cmd):
        return self._openwrtcore._send_cmd(cmd)

    def set_ssid(self, iface, ssid):
        self._openwrtcore._set_ssid(iface, ssid)

    def get_ssid(self, iface="2G"):
        iface = self._get_iface_code(iface)
        self._result = self._openwrtcore._get_ssid(iface)
        return self._result

    def check_system_info(self):
        """Get system info ``version`` and ``cpuinfo``.

        The given value is passed to the calculator directly. Valid buttons
        are everything that the calculator accepts.

        Examples:
        | Check System Info |
        """
        self._result = self._openwrtcore._get_version()
        self._result += "\n" + self._openwrtcore._get_cpuinfo()
        return self._result

    def change_ssid(self, iface, ssid):
        self._portalwebguicore._change_ssid(iface, ssid)

    def change_encryption_mode(self, iface, encryption):
        encryption = self._get_encryption_code(encryption)
        self._portalwebguicore._change_encryption_mode(iface, encryption)

    def change_network_password(self, iface, pwd=None):
        if pwd: self._portalwebguicore._change_network_password(iface, pwd)

    def change_router_password(self, pwd=None):
        if pwd: self._portalwebguicore.change_router_password(pwd)

    def toggle_ssid_broadcast(self, iface, enable=True):
        self._portalwebguicore._broadcast_ssid(iface, enable)

    def toggle_bridge_mode(self, enable=None):
        #feng add
        logger.console("--> toggle bridge mode : line 107")
        self._portalwebguicore._toggle_bridge_mode(enable)

    def toggle_dhcp_server(self, enable=None):
        #feng add
        logger.console("\ntoggle dhcp server , in the AccessPointWebLibrary.py / def toggle_dhcp_server")
        self._portalwebguicore._toggle_dhcp_server(enable)

    def connect_wifi(self, ssid, pwd = None):
        return self._stacontrol._connect_wifi(ssid, pwd)

    def disconnect_wifi(self, ssid):
        self._stacontrol._disconnect_wifi(ssid)

    def delete_wifi_record(self, ssid):
        self._stacontrol._delete_wifi_record(ssid)

    def scan_ssid(self, ssid, expect_status):
        return self._stacontrol._scan_ssid(ssid, expect_status, 16, 5)

    def renew_pc_ip_address(self):
        #feng Add
        logger.console("\n --> AccessPointWebLibrary.py : line 123")
        #---------------------------------------------------
        logger.console("\nRenew PC ip address")
        #feng add
        # the PC Ethernet card interface as below:
        logger.console(self._eth)
        #------------------------------------------
        self._stacontrol._disable_interface(self._eth)
        time.sleep(5)
        self._stacontrol._enable_interface(self._eth)
        time.sleep(5)
        self._stacontrol.block_until_cable_connect()

    def disable_wifi(self):
        self._stacontrol.disable_wifi()

    def enable_wifi(self):
        self._stacontrol.enable_wifi()

    def disable_interface(self, interface):
        self._stacontrol._disable_interface(interface)

    def enalble_interface(self, interface):
        self._stacontrol._enable_interface(interface)

    def go_to_page(self, link):
        self._portalwebguicore.go_to_page(link)

    def refresh_page(self):
        #feng add
        logger.console("\n refresh page , AccessPointWebLibrary.py : def refresh")
        self._portalwebguicore.refresh_page()

    def ssh_connect(self):
        self._sshcontrol.waitForDevice()

    def ssh_disconnect(self):
        self._sshcontrol.disconnect_ssh()

    def clear_all_ssh_connection(self):
        self._sshcontrol.clear_all_ssh_connection()

    def wifi_connection(self, ssid, password = None):
        wifi_connect_flag = False
        for i in range(0, 10, 1):
            logger.info("Try to connect wifi %sth times" %str(i))
            if self.scan_ssid(ssid, True):
                wifi_connect_flag = self.connect_wifi(ssid, password)
                if wifi_connect_flag:
                    break
                logger.info("Connecting wifi failed, try again.")
            else:
                assert_true(False, "Scanning ssid failed, could not find ssid")
        assert_true(wifi_connect_flag, "Cannot connect to ssid's wifi")

    def create_large_file(self):
        logger.info("creating large file")
        self._stacontrol.create_large_file()

    def create_small_file(self):
        self._stacontrol.create_small_file()
    def remove_file(self):
        self._stacontrol.remove_file()

########## CHECK FUNCTIONS ###########
    def check_portal_wireless(self, iface=None, ssid=None, encryption=None, password=None):
        """Checks ssid, encryption, and password with info from ssh'ing into portal itself
        Verifies that the params passed in is the same with the info inside portal
        Error is thrown if any info is different
        User can specify which param to check, omit a check by passing in None to variable
        """
        logger.console("\nChecking portal wireless configurations")
        self._portalwebguicore.if_web_disconnect()
        iface = self._get_iface_code(iface)
        encryption = self._get_encryption_code(encryption)

        if ssid: assert_equal(ssid, self._openwrtcore._get_ssid(iface), "ssid is diff")
        if encryption: assert_equal(encryption, self._openwrtcore._get_encryption(iface), "encryption is diff")
        if password: assert_equal(password, self._openwrtcore._get_password(iface), "passwod is diff")

    def check_portal_wireless_default(self, iface=None, encryption=None):
        """Checks default generated ssid, password, and encryption type
        Verifies that info inside default portal is correctly generated
        Error is throw if any info is different
        User can specify the type of encryption to check
        """
        logger.console("\nChecking portal wireless default configurations")
        self._portalwebguicore.if_web_disconnect()
        iface = self._get_iface_code(iface)
        encryption = self._get_encryption_code(encryption)
        ssid_2g, ssid_5g, password = self._get_default_info()
        if 0 == iface:
            ssid = ssid_2g
        elif 1 == iface:
            ssid = ssid_5g
        assert_equal(ssid, self._openwrtcore._get_ssid(iface), "ssid is diff")
        assert_equal(encryption, self._openwrtcore._get_encryption(iface), "encryption is diff")
        assert_equal(password, self._openwrtcore._get_password(iface), "password is diff")

    def check_web_status_wireless(self, iface=None, ssid=None, encryption=None):
        """Check ssid ssid and encryption type on the web
        """
        logger.console("\nChecking web status configurations")
        self._portalwebguicore.if_web_disconnect()
        encryption = self._get_encryption_code(encryption)

        if "2.4" == iface:
            (ssid_result, encryption_result) = self._portalwebguicore._check_2g_status()
        elif "5" == iface:
            (ssid_result, encryption_result) = self._portalwebguicore._check_5g_status()

        assert_equal(ssid, ssid_result, "ssid is diff")
        assert_equal(encryption, encryption_result, "encryption is diff")

    def check_web_status_attached_device(self, iface=None):
        """FIXME only scans entire page for mac address, does not differentiate
        between 2G and 5G connections
        """
        """
            2017/01/26 

        Because can't run eth0 / wlan0 as the same time. needs disble eth0 first
        After checked attached device, enable eth0
        """
        #---------------------------------------------
        logger.info("disable ethernet first : "+str(self._eth))
        logger.console("disable ethernet first : "+str(self._eth))
        self._stacontrol._disable_interface(self._eth)
        time.sleep(10)
        #--------------------------------------------- 
        logger.console("\nChecking web status attached devices")
        self._portalwebguicore.if_web_disconnect()

        this_device_ip, expect_status = self._stacontrol.get_interface_ip_addr(self._wlan, True)
        if expect_status:
            device_mac = self._portalwebguicore._check_attach(this_device_ip, iface, 10, 3)
            assert_equal(device_mac, self._stacontrol.get_interface_mac_addr(self._wlan), "This device not on web status attached device page")
        else:
            assert_true(False, "Can't receive the IP address")
        #---------------------------------------------------------
        logger.info("enable ethernet first : "+str(self._eth))
        logger.console("enable ethernet first : "+str(self._eth))
        self._stacontrol._enable_interface(self._eth)
        time.sleep(10)
        #---------------------------------------------------------

    def check_web_default_ssid(self, iface=None):
        """Verify default ssid is caluclated and shown correctly on the web
        """
        logger.console("\nChecking web status default ssid")
        self._portalwebguicore.if_web_disconnect()
        ssid_2g, ssid_5g, pwd = self._get_default_info()
        if "2.4" == iface:
            default_ssid = ssid_2g
        elif "5" == iface:
            default_ssid = ssid_5g
        self.check_web_status_wireless(iface, default_ssid, "WPA2")

    def check_ssid(self, iface, ssid):
        logger.console("\nChecking ssid via portal")
        self._portalwebguicore.if_web_disconnect()
        iface = self._get_iface_code(iface)
        assert_equal(ssid, self._openwrtcore._get_ssid(iface), "ssid not set correctly")

    def check_encryption(self, iface, encryption):
        logger.console("\nChecking encryption via portal")
        self._portalwebguicore.if_web_disconnect()
        iface = self._get_iface_code(iface)
        encryption = self._get_encryption_code(encryption)
        assert_equal(encryption, self._openwrtcore._get_encryption(iface), "Security mode not set correctly")

    def check_password(self, iface, password):
        logger.console("\nChecking password via portal")
        self._portalwebguicore.if_web_disconnect()
        iface = self._get_iface_code(iface)
        assert_equal(password, self._openwrtcore._get_password(iface), "Network password not set correctly")

    def check_wifi_connection(self, iface, ssid=None, encryption=None, password=None):
        """Check connection to portal
        tries to scan given ssid, connect to that given ssid
        and pings to router and outside ip to test valid connection
        """
        logger.console("\nChecking connection")
        self._portalwebguicore.if_web_disconnect()
        all_success = True

        self.wifi_connection(ssid, password)

        outgoing_ip = "8.8.8.8"
        self._stacontrol._disable_interface(self._eth)
        time.sleep(5)
        if not self._stacontrol.ping_check(self._router_ip):
            logger.console("Cannot ping to router")
            all_success = False
        if not self._stacontrol.ping_check(outgoing_ip):
            logger.console("Cannot ping to outside network")
            all_success = False
        self._stacontrol._enable_interface(self._eth)
        time.sleep(5)
        assert_true(all_success, "Check connection failed")

    def check_broadcast(self, freq, ssid):
        """Checks if ssid broadcast
        turns off broadcast, attempt to scan for given ssid, expects to fail
        turns on broadcast, attempt to scan for given ssid, expects to succeed
        """
        logger.console("\nChecking broadcast")
        self._portalwebguicore.if_web_disconnect()
        self.toggle_ssid_broadcast(freq, False)
        self.apply()
        self.delete_wifi_record(ssid)
        assert_true(self._stacontrol._scan_ssid(ssid, False, 4, 5), "ssid should be hidden, but is found")

        self.toggle_ssid_broadcast(freq, True)
        self.apply()
        assert_true(self.scan_ssid(ssid, True), "ssid should be broadcasted, but not found")

########## WAN Test Functions ###########
    def check_internet_connection(self, url, expect_status):
        """Check for internet connection
        Pings to router, google dns, and domain name address
        """
                
        #-------------
        logger.info("\nChecking internet connection")
        # self._log_wan_info()

        if expect_status:
            assert_true(self._stacontrol.ping_check(url), "Ping to %s failed" %url)
        else :
            assert_false(self._stacontrol.ping_check(url), "Shouldn't be able to ping to %s " %url)

    def configure_wan_with_dhcp(self):
        logger.info("Configuring DHCP connection")
        self._portalwebguicore.configure_wan_dhcp()

    def configure_wan_with_pppoe(self, username=None, password=None, service=None):
        logger.info("Configuring PPPoE connection")
        #feng add
        logger.console("\nconfigure_wan_with_pppoe -> AccessPointWeblibrary.py : def configure_wan_with_pppoe\n")
        self._portalwebguicore.configure_wan_pppoe(username, password, service)

    def configure_wan_with_static(self, ip_address=None, gateway=None, netmask=None):
        logger.info("Configure wan with static")
        self._portalwebguicore.configure_wan_static(ip_address, gateway, netmask)
        #feng add
        logger.console("\nConfigure wan with static -> AccessPointWebLibrary.py  / def configure_wan_with_static \n")

    def verify_wan_portal_info(self, connection_type, param1=None, param2=None, param3=None):
        """Verifies that info in portal is correct
        Checks ip address/gateway/netmask, username/password/service based on type of connection
        """

        # 20170125 feng bypass this function
        #logger.info("Verifying portal info")
        # self._log_wan_info() 
        
        connection_type = connection_type.lower()
        wan_mode = self._openwrtcore._get_wan_mode()

        if "dhcp" == connection_type:
            assert_equal(connection_type, wan_mode, "WAN is not in DHCP mode")
        elif "static" == connection_type:
            ip_address = param1
            gateway = param2
            netmask = param3

            assert_equal(connection_type, wan_mode, "WAN is not in Static mode")
            assert_equal(ip_address, self._openwrtcore._get_wan_ipaddr(), "Static ip address is diff")
            assert_equal(netmask, self._openwrtcore._get_wan_netmask(), "Static netmask is diff")
            if gateway: assert_equal(gateway, self._openwrtcore._get_wan_gateway(), "Static gateway is diff")

        elif "pppoe" == connection_type:
            username = param1
            password = param2
            service = param3

            assert_equal(connection_type, wan_mode, "WAN is not in PPPoE mode")
            assert_equal(username, self._openwrtcore._get_wan_username(), "PPPoE username is diff")
            assert_equal(password, self._openwrtcore._get_wan_password(), "PPPoE password is diff")
            if service: assert_equal(service, self._openwrtcore._get_wan_service(), "PPPoE service is diff")
         
    def verify_wan_web_info(self, connection_type, param2=None, param3=None, param4=None):
        """Verifies that info on the web is correct
        Checks connection status, and ip address based on type of connection
        """
        logger.info("Verifying web info")
        # Get portal web status
        web_connection_status = self._portalwebguicore.get_wan_connection_status().lower()
        web_ip_address, web_subnet = self._portalwebguicore.get_wan_ip_and_subnet()

        # Check WAN connection status
       
        expect_connection_status = param2.lower()
        assert_equal(expect_connection_status, web_connection_status, "Web connection status is diff")

        if "static" == connection_type.lower():
            ip_address = param3
            subnet = param4
            assert_equal(ip_address, web_ip_address, "Web ip address is diff")
            if subnet: assert_equal(subnet, web_subnet, "Web subnet mask address is diff")

    def verify_wan_web_dns_info(self, dns1=None, dns2=None, dns3=None, dns4=None):
        """Verifies that dns info on the web is correct
        Checks the addresses on the dns server status is the same as the dns addresses
        passed in from the arguments
        """
        logger.info("Verifying web DNS info")
        dns_list = self._portalwebguicore.get_wan_dns()

        if dns1: self._assert_in_dns_list(dns_list, dns1)
        if dns2: self._assert_in_dns_list(dns_list, dns2)
        if dns3: self._assert_in_dns_list(dns_list, dns3)
        if dns4: self._assert_in_dns_list(dns_list, dns4)

    def check_cannot_connect_domain_name(self):
        """Check that a connection to a domain name address cannot be established
        Fails if this test device is able to ping to the domain names below
        Make sure that the only internet connection to outside is thru the testing portal
        """
        logger.info("\nChecking internet connection")
        time.sleep(10)
        # self._log_wan_info()
        fast_com = "www.fast.com"
        amazon_com = "www.amazon.com"
        assert_false(self._stacontrol.ping_check(fast_com), "Can ping to fast.com, should fail")
        assert_false(self._stacontrol.ping_check(amazon_com), "Can ping to amazon.com, should fail")

    def configure_auto_dns(self):
        """Automatically get two dns servers from ISP
        This is usually 172.16.10.22 and 8.8.8.8 (though not guarenteed)
        """
        logger.info("Configuring to get dns automatically from ISP")
        self._portalwebguicore._toggle_isp(True)
        self.apply()

    def configure_manual_dns(self, primary_dns, backup_dns=None):
        """Manually configure two sets of dns servers, instead of using the automatic ones from ISP
        """
        logger.info("Configuring dns manually")
        self._portalwebguicore._toggle_isp(False)
        self._portalwebguicore._configure_dns(primary_dns, backup_dns)
        self.apply()

########## LAN Test Functions ###########
    def check_lan_default(self, ip_address, subnet_mask):
        """ Check WEB GUI /status/LAN default
            The info should be IP: 192.168.8.1  Subnet mask: 255.255.255.0
        """   
        logger.console("\nCheck lan default")
        ip_address_result, subnet_mask_result = self._portalwebguicore._check_lan_status()
        assert_equal(ip_address, ip_address_result, "Default IP Address is diff")
        assert_equal(subnet_mask, subnet_mask_result, "Default Subnet Mask is diff")

    def configure_lan_with_static(self, ip_address = None, subnet_mask = None):
        # feng add 
        logger.console("\n --> AccessPointWeLibrary.py line 451")
        """ Set LAN IP and Subnet_mask """
        logger.console("\nConfigure lan with static")
                # feng add 
        logger.console("\n --> Go to PortalWebGUICore.py Line 482")
        self._portalwebguicore.configure_lan_static(ip_address, subnet_mask)

    #--default script as below:
    """
    def check_route_ip(self, ip_address, subnet_mask):
        " Check the PC should get the new router ip ""
        ip_address_result = self._stacontrol._get_route_ip()
        assert_equal(ip_address, ip_address_result, "Route IP address is diff")
        subnet_mask_result = self._stacontrol._get_route_subnet_mask()
        logger.console(subnet_mask_result)
        assert_equal(subnet_mask, subnet_mask_result, "Route subnet mask is diff")

    """
    #feng add 12/27
    def check_route_ip(self, ip_address, subnet_mask):
        " Check the PC should get the new router ip "
        #feng 
        logger.console("\n the Robot system default IP address / subnet_make as below : ")
        logger.console("\n"+ip_address+" / "+ subnet_mask) 
        ip_address_result = self._stacontrol._get_route_ip()
        #feng add
        logger.console("\nRoute table ip address result : ")
        logger.console(ip_address_result)
        #----------------------------------------------------------
        #--------------------------------------------------------------------- 
        assert_equal(ip_address, ip_address_result, "Route IP address is diff")

        #----------------------------------------------------------------
        subnet_mask_result = self._stacontrol._get_route_subnet_mask()
        #feng add
        logger.console("\n the Robot system default IP address / subnet_make as below : ")
        logger.console("\n"+ip_address+" / "+subnet_mask)
        logger.console("\nRoute table ip subnet mask result : ")
        logger.console(subnet_mask_result)
        assert_equal(subnet_mask, subnet_mask_result, "Route subnet mask is diff")

    


    def check_connect_web(self, ip_address, title, password):
        #eng
        logger.console("\n\nCall check_connect_web function -> AccessPintWebLibrary.py line 469\n")
        """ Trying to login WEB GUI """
        for i in range (0, 5, 1):
            logger.console("\nCheck if connect to WEB GUI")
            if self._stacontrol.ping_check(ip_address):

                assert_true(self.open_website(ip_address, title, password), "Times out, Can't open web GUI successful")
                break
            else:
                self._stacontrol.block_until_cable_connect()
                self.set_eth_manually(self.assign_ip_address, self.assign_subnet_mask)
                continue
            if i == 4:
                assert_true(False, "ping to router failed")

    def check_connect_wan(self):
        ip_address, subnet_mask = self._portalwebguicore.get_wan_ip_and_subnet()
        if ip_address:
            assert_true(self._stacontrol.ping_check(ip_address), "Coundn't ping to WAN port")
            #feng add
            logger.console("\nCheck wan IP address: ")
            logger.console(ip_address)
        else:
            assert_true(False, "Can't get WAN ip")

    def try_classd_and_e(self, ip_address):
        # --Feng 20161221 tag
        """ Check the WEB if refuse the ClassD(224-239) and E(240-255) """
        logger.console("\nTrying classD and E")
        #errmsg_result = self._portalwebguicore._try_classd_and_e(ip_address)
        logger.console("The IP addtess from the robot script is : "+ip_address)

        errmsg_result = self._portalwebguicore._try_classd_and_e(ip_address)
        #errmsg = "IP address needs to be A, B or C class type."
        errmsg ="ip-address-class-type"
        assert_equal(errmsg, errmsg_result, "ip-address-class-type")
        #feng add
        logger.console("\nThe message is : ip-address-type , catch from the Web")
        #assert_equal(errmsg, errmsg_result, "Can use ClassD and E")
        #ip-address-class-type



    def disable_dynamic_server(self):
        # feng add
        logger.console("\n--> in AccessPointWebLibrary.py / def disable_dynamic_server")        
        logger.console("\nDisable the DHCP server")
        self.toggle_dhcp_server(False)
        self.apply()

    def enable_dynamic_server(self):

        logger.console("\n--> in AccessPointWebLibrary.py / line 497")
        logger.console("\nEnable the DHCP server")
        self.toggle_dhcp_server(True)
        self.apply()

    def check_pc_ip_address(self, expect_status):

        """ Check the PC if get the IP broadcast from Portal"""
        logger.console("\nCheck if receive IP address")
        if not expect_status:
            ip_address, status_result = self._stacontrol.get_interface_ip_addr(self._eth, expect_status, 10, 1)
            #feng add as below
            logger.console("\nCheck PC IP address is : "+ip_address)
            logger.console(status_result)
        else:
            ip_address, status_result = self._stacontrol.get_interface_ip_addr(self._eth, expect_status)
        assert_true(status_result, "The expect status is different from the result")
        #feng
        logger.console ("\n--> in AccessPointWebLibrary.py line 568")


    def set_eth_manually(self, ip_address, subnet_mask):
        #feng
        logger.console("\nSetting up PC ethernet interface IP by manual-> Line 584 in AccessPointWebLibrary")
        """ Set IP address and subnet mask to the interface """
        logger.console("\nSet eth IP address")
        self.assign_ip_address = ip_address
        self.assign_subnet_mask = subnet_mask
        self._stacontrol._assign_eth_ip_address(ip_address, subnet_mask)
        time.sleep(5)

    def discard_eth_manually(self, ip_address, subnet_mask):
        logger.console("\nRemove eth IP address")
        self._stacontrol._remove_eth_ip_address(ip_address, subnet_mask)

########## Firewall ##########
    def configure_dmz(self, ip_address = None):
        logger.console("\nSet DMZ")
        if not ip_address:
            ip_address, result = self._stacontrol.get_interface_ip_addr(self._eth, True)
        self._portalwebguicore.configure_dmz(ip_address)

    def delete_dmz(self):
        self._portalwebguicore.delete_dmz()

    def delete_inbound_all_firewall_rule(self):
        pass

    def delete_inbound_firewall_rule(self):
        self._portalwebguicore.delete_inbound_firewall_rule()

    def delete_outbound_firewall_rule(self):
        self._portalwebguicore.delete_outbound_firewall_rule()

    def the_all_packets_should_be_received(self, protocal):
        logger.console("\nThe all packets should be received")
        for i in range(1001,1011):
            self.inbound_receive_mesg(i, protocal, True)

    def block_all_devices(self):
        self._portalwebguicore.block_all_devices()

    def block_specific_device(self, devices_ip):
        self._portalwebguicore.block_specific_device(devices_ip)

    def check_does_not_has_internet_connection(self):
        logger.console("\nCheck doesn't connect to the internet")
        assert_false(self._stacontrol.ping_check("8.8.8.8"), "Shouldn't access internet")

# Test Inbound rule
    # Base funcion
    def set_firewall_inbound_rule(self, service_name, port, protocal, lan_ip,
            wan_source, wan_start_ip = None, wan_end_ip = None):

        logger.console("\nSet inbound rule")
        lan_ip, result = self._stacontrol.get_interface_ip_addr(self._eth, True)

        self._portalwebguicore.configure_inbound(service_name, port, protocal, lan_ip, wan_source, wan_start_ip, wan_end_ip)
        assert_true(self._portalwebguicore.check_service_name(), "Set service name failed")
        assert_true(self._portalwebguicore.check_port(), "Set port number failed")
        assert_true(self._portalwebguicore.check_inbound_lan_ip(), "Set LAN IP failed")
        assert_true(self._portalwebguicore.check_inbound_wan_ip(), "Set WAN IP failed")

    def edit_firewall_inbound_rule(self, service_name = None, port = None, protocal = None, lan_ip = None,
            wan_source = None, wan_start_ip = None, wan_end_ip = None):

        logger.console("\nEdit inbound rule")
        self._portalwebguicore.edit_inbound(service_name, port, protocal, lan_ip, wan_source, wan_start_ip, wan_end_ip)
        assert_true(self._portalwebguicore.check_service_name(), "Edit service name failed")
        assert_true(self._portalwebguicore.check_port(), "Edit port number failed")
        assert_true(self._portalwebguicore.check_inbound_lan_ip(), "Edit LAN IP failed")
        assert_true(self._portalwebguicore.check_inbound_wan_ip(), "Edit WAN IP failed")

    def inbound_receive_mesg(self, port, protocal, expect_receive = True):
        # Check if the messages from the WAN port PC can be received by the LAN port PC
        # Step.1 Costruct the local server with "TCP" or "UDP"
        # Step.2 Remote PC as client and send message to the pself.ssh_client_pwdortal's WAN IP
        # Step.3 Close the local server
        # "expect_receive" control if you want to receive the message or not

        logger.console("\nTest inbound receive message with \"%s\" port: %s" %(protocal, str(port)))

        host_ip = self._openwrtcore._get_wan_ipaddr()
        self._construct_local_server(protocal, port)

        if expect_receive:
            logger.console("It should be received successful")
            result = self._sshcontrol.send_mesg_to_server(protocal, host_ip, port, time_out = 30, trying_times = 5)
            assert_true(result, "Doesn't receive the message from WAN")
        else:
            logger.console("It shouldn't be received successful")
            result = self._sshcontrol.send_mesg_to_server(protocal, host_ip, port, time_out = 30, trying_times = 1)
            assert_false(result, "Shouldn't receive the message from WAN")
        self._stop_local_server()

    def _construct_local_server(self, protocal, port):
        # Construct the local server, should set the protocal and the port you want
        for i in range(0, 15, 1):
            logger.console("\nConstruct local server")
            self._stop_local_server()
            if self._stacontrol.construct_server(protocal, port):
                return True
            logger.console("Construct server failed, try again..")

        assert_true(False, "Construct server failed")

    def _stop_local_server(self):
        self._stacontrol.stop_server()

    # Utility function
    def test_inbound_receive(self, port, protocal):
        """ Only the port and protocal is the same as the rule you set can be received"""
        while True:
            ran_port = randint(1000, 5000)
            if ran_port != port:
                break
        if protocal.lower() == "tcp/udp":
            self.inbound_receive_mesg(port, "TCP", True)
            self.inbound_receive_mesg(ran_port, "TCP", False)
            self.inbound_receive_mesg(port, "UDP", True)
            self.inbound_receive_mesg(ran_port, "UDP", False)
        else:
            self.inbound_receive_mesg(port, protocal, True)
            self.inbound_receive_mesg(ran_port, protocal, False)
            if protocal.lower() == "tcp":
                self.inbound_receive_mesg(port, "UDP", False)
            elif protocal.lower() == "udp":
                self.inbound_receive_mesg(port, "TCP", False)

    def test_inbound_connection_from_all(self, port, protocal):
        logger.console("\nTest inbound connection from all with \"%s\" port: %s" %(protocal, str(port)))
        self.test_inbound_receive(port, protocal)

    def test_inbound_connection_from_single_ip(self, port, protocal):
        logger.console("\nTest inbound connection from single ip with \"%s\" port: %s" %(protocal, str(port)))
        self.test_inbound_receive(port, protocal)
        self.edit_firewall_inbound_rule(wan_source = "single", wan_start_ip = "10.10.10.10")
        if protocal.lower() == "tcp/udp":
            self.inbound_receive_mesg(port, "TCP", False)
            self.inbound_receive_mesg(port, "UDP", False)
        else:
            self.inbound_receive_mesg(port, protocal, False)

    def test_inbound_connection_from_range_ip(self, port, protocal):
        logger.console("\nTest inbound connection from range ip with %s port: %s" %(protocal, str(port)))
        self.test_inbound_receive(port, protocal)
        self.edit_firewall_inbound_rule(wan_source = "range", wan_start_ip = "10.10.10.50", wan_end_ip = "10.10.10.100")
        if protocal.lower() == "tcp/udp":
            self.inbound_receive_mesg(port, "TCP", False)
            self.inbound_receive_mesg(port, "UDP", False)
        else:
            self.inbound_receive_mesg(port, protocal, False)

# Test Outbound rule
    # Base function
    def set_firewall_outbound_rule(self, service_name, port, protocal, lan_source, wan_source,
            lan_start_ip = None, lan_end_ip = None, wan_start_ip = None, wan_end_ip = None):

        logger.console("\nSet outbound rule")
        lan_start_ip, result = self._stacontrol.get_interface_ip_addr(self._eth, True)
        lan_end_ip = "192.168.8.140"

        self._portalwebguicore.configure_outbound(service_name, port, protocal, lan_source, wan_source,
            lan_start_ip, lan_end_ip, wan_start_ip, wan_end_ip)
        assert_true(self._portalwebguicore.check_service_name(), "Configure service name failed")
        assert_true(self._portalwebguicore.check_port(), "Configure port number failed")
        assert_true(self._portalwebguicore.check_outbound_lan_ip(), "Configure LAN IP failed")
        assert_true(self._portalwebguicore.check_outbound_wan_ip(), "Configure WAN IP failed")

    def edit_firewall_outbound_rule(self, service_name = None, port = None, protocal = None, lan_source = None, wan_source = None,
            lan_start_ip = None, lan_end_ip = None, wan_start_ip = None, wan_end_ip = None):

        logger.console("\nEdit outbound rule")
        self._portalwebguicore.edit_outbound(service_name, port, protocal, lan_source, wan_source,
             lan_start_ip, lan_end_ip, wan_start_ip, wan_end_ip)
        assert_true(self._portalwebguicore.check_service_name(), "Edit service name failed")
        assert_true(self._portalwebguicore.check_port(), "Edit port number failed")
        assert_true(self._portalwebguicore.check_outbound_lan_ip(), "Edit LAN IP failed")
        assert_true(self._portalwebguicore.check_outbound_wan_ip(), "Edit WAN IP failed")

    def outbound_send_mesg(self, port, protocal, expect_transfer = True):
        # Step.1 Costruct the remote server with "TCP" or "UDP"
        # Step.2 Local PC as client and send message to the remote PC
        # Step.3 Close the remote server
        # "expect_receive" control if you want to receive the message or not

        logger.console("\nOutbound send message with \"%s\", port: %s"  %(protocal, str(port)))

        host_ip = self._ssh_client_host
        self._construct_remote_server(port, protocal)

        if expect_transfer:
            logger.console("It should be sended successful")
            result = self._stacontrol.send_mesg_to_server(protocal, host_ip, port, time_out = 30, trying_times = 5)
            assert_true(result, "Doesn't send message to WAN port successful(Server)")
        else:
            logger.console("It shouldn't be sended successful")
            result = self._stacontrol.send_mesg_to_server(protocal, host_ip, port, time_out = 30, trying_times = 1)
            assert_false(result, "Shouldn't send message to WAN por successful(Server)")

        self._stop_remote_server()

    def _construct_remote_server(self, port, protocal):
        # Construct the remote server, should set the protocal and the port you want
        host_ip = self._ssh_client_host
        for i in range(0, 15, 1):
            logger.console("\nConstruct remote server")
            self._stop_remote_server()
            if self._sshcontrol.construct_server(protocal, port):
                return True
            logger.console("Construct server failed, try again..")

        assert_true(False, "Construct server failed")

    def _stop_remote_server(self):
        self._sshcontrol.stop_server()

    # Utility funciton
    def test_outbund_transfer(self, port, protocal):
        while True:
            ran_port = randint(1000, 5000)
            if ran_port != port:
                break
        if protocal.lower() == "tcp/udp":
            self.outbound_send_mesg(port, "TCP", False)
            self.outbound_send_mesg(ran_port, "TCP", True)
            self.outbound_send_mesg(port, "UDP", False)
            self.outbound_send_mesg(ran_port, "UDP", True)
        else:
            self.outbound_send_mesg(port, protocal, False)
            self.outbound_send_mesg(ran_port, protocal, True)
            if protocal.lower() == "tcp":
                self.outbound_send_mesg(port, "UDP", True)
            elif protocal.lower() == "udp":
                self.outbound_send_mesg(port, "TCP", True)

    def test_outbound_connection_to_all(self, port, protocal):
        logger.console("\nTest outbound connection to all with \"%s\", port: %s" %(protocal, str(port)))
        self.test_outbund_transfer(port, protocal)

    def test_outbound_connection_to_single_ip(self, port, protocal):
        logger.console("\nTest outbound connection to single ip with \"%s\", port: %s" %(protocal, str(port)))
        self.test_outbund_transfer(port, protocal)
        self.edit_firewall_outbound_rule(wan_source = "single", wan_start_ip = "10.10.10.10")
        if protocal.lower() == "tcp/udp":
            self.outbound_send_mesg(port, "TCP", True)
            self.outbound_send_mesg(port, "UDP", True)
        else:
            self.outbound_send_mesg(port, protocal, True)

    def test_outbound_connection_to_range_ip(self, port, protocal):
        logger.console("\nTest outbound connection to range ip with \"%s\", port: %s" %(protocal, str(port)))
        self.test_outbund_transfer(port, protocal)
        self.edit_firewall_outbound_rule(wan_source = "range", wan_start_ip = "10.10.10.10",  wan_end_ip = "10.10.10.50")
        if protocal.lower() == "tcp/udp":
            self.outbound_send_mesg(port, "TCP", True)
            self.outbound_send_mesg(port, "UDP", True)
        else:
            self.outbound_send_mesg(port, protocal, True)

########## USB ##########
    def go_to_usb_page(self, usb_id):
        self._portalwebguicore._goto_usb_page_slot(usb_id)

    def eject_usb_slot(self, usb_id):
        if self._portalwebguicore.check_usb_controller(usb_id).lower() == "eject":
            self._portalwebguicore.eject_usb(usb_id)
            time.sleep(6) #loading time
        else:
            assert_true(False, "USB button status is incorrect")

    def detect_usb_slot(self, usb_id):
        if self._portalwebguicore.check_usb_controller(usb_id).lower() == "detect":
            self._portalwebguicore.detect_usb(usb_id)
            #feng add 20170126
            #-----------------------
            time.sleep(10)
            #------------------------
        else:
            assert_true(False, "USB button status is incorrect")

    def toggle_usb_samba(self, usb_id, enable=None):
        if 'disable' == enable.lower():
            enable = False
        else:
            enable = True
        self._portalwebguicore.toggle_samba(usb_id, enable)
        self._portalwebguicore.apply_no_reload()

    def check_usb_format(self, usb_id, expected_usb_format):
        assert_equal(self._portalwebguicore.check_usb_format(usb_id).lower(), expected_usb_format.lower(), "USB on slot " + usb_id + " format is different from expected")

    def check_usb_is_ejected(self, usb_id):
        #feng add 20170126 
        #--------------------
        self.refresh_page()
        time.sleep(2)
        # message is "USB device not detected.""
        #--------------------
        #change to assert_equal(self._portalwebguicore.check_usb_is_ejected(usb_id), "USB device successfully removed.", "USB on slot " + usb_id + " failed to eject")
        assert_equal(self._portalwebguicore.check_usb_is_ejected(usb_id), "USB device not detected.", "USB on slot " + usb_id + " failed to eject")
    def check_usb_is_mounted(self, usb_id):
        #feng add 20170126 
        #--------------------
        self.refresh_page()
        time.sleep(2)
        #--------------------
        assert_true(self._portalwebguicore.check_usb_status(usb_id), "USB is unmounted on slot " + usb_id)

    def check_samba_works(self, usb_id, username, password):
        """Checks samba function by uploading a test file to portal and
        ssh'ing into portal to check its existance
        """
        upload_f = 'sambaupload.file'
        os.system("echo 'samba upload dummy file' >> " + upload_f)
        #feng add 20170202 
        #---------------------------------------------------------------------
        logger.console("\nprepare to upload to samba server")
        logger.console("\nthe username : "+username)
        logger.console("\nthe password :"+password)
        logger.console("\nthe usbid : "+usb_id)
        #----------------------------------------------------------------------       
        self._stacontrol.samba_upload(usb_id, upload_f, username, password)

        has_file = self._openwrtcore._check_file(usb_id, upload_f)
        self.delete_usb_file(usb_id, upload_f)
        os.system("rm -f " + upload_f)

        assert_true(has_file, "Samba failed: "+ upload_f + " not found in usb slot: " + usb_id)

    def upload_samba_file(self, usb_id, filename, username, password):
        """Upload a file to usb on portal via samba """
        self._stacontrol.samba_upload(usb_id, filename, username, password)

    def check_upload_successful(self, usb_id, filename):
        logger.info("Check if upload file: " + filename + " successful on slot " + str(usb_id))
        assert_true(self._openwrtcore._check_file(usb_id, filename), "Upload file failed")

    def delete_usb_file(self, usb_id, filename):
        logger.info("Trying to delete file " + filename + " on slot " + str(usb_id))
        self._openwrtcore._delete_file(usb_id, filename)

    def toggle_usb_ftp(self, usb_id, enable = None):
        self._portalwebguicore.toggle_ftp(usb_id, enable)
        self._portalwebguicore.apply_no_reload()

    def upload_file_ftp(self, usb_id, filename, username, password):
        logger.info("Trying to upload file thru ftp to slot " + str(usb_id) + " with file: " + filename + " and usr:pwd: " + username + ":" + password)
        #-feng add 20170202
              
        logger.console("Trying to upload file thru ftp to slot " + str(usb_id) + " with file: " + filename + " and usr:pwd: " + username + ":" + password)
        
        #----------------------------------------------------------------------------
        self._stacontrol.upload_file_ftp(usb_id, filename, username, password)

    def toggle_usb_dlna(self, usb_id, enable=None):
        self._portalwebguicore.toggle_dlna(usb_id, enable)
        self._portalwebguicore.apply_no_reload()

    def check_dlna_works(self, usb_id):
        assert_true(self._portalwebguicore.can_connect_dlna(), "DLNA is not working, cannot connect to port 8200")

    def download_file_ftp(self, usb_id, filename, username, password):
        logger.console("\nTrying to download file")
        self._stacontrol._download_file_ftp(usb_id,filename,username,password)

    def check_samba_status(self, usb_id, expect_status = True):
        if expect_status:
            assert_true(self._portalwebguicore.samba_status(usb_id), "Samba should be toggled")
        else:
            assert_false(self._portalwebguicore.samba_status(usb_id), "Samba shouldn't be toggled")

    def check_ftp_status(self, usb_id, expect_status = True):
        if expect_status:
            assert_true(self._portalwebguicore.ftp_status(usb_id), "FTP should be toggled")
        else:
            assert_false(self._portalwebguicore.ftp_status(usb_id), "FTP shouldn't be toggled")

    def check_dlna_status(self, usb_id, expect_status = True):
        if expect_status:
            assert_true(self._portalwebguicore.dlna_status(usb_id), "DLNA should be toggled")
        else:
            assert_false(self._portalwebguicore.dlna_status(usb_id), "DLNA shouldn't be toggled")

    def test_eject_feature(self, usb_id, trying_times, expected_usb_format):
        for i in range(0, int(trying_times), 1):
            logger.info("Check usb eject and detect feature %sth times" %str(i))
            self.eject_usb_slot(usb_id)
            #feng add time.delay
            #-----------------------
            time.sleep(3)
            #------------------------
            self.check_usb_is_ejected(usb_id)
            self.detect_usb_slot(usb_id)
            self.check_usb_is_mounted(usb_id)
            self.check_usb_format(usb_id, expected_usb_format)
            if i == 0:
                self._portalwebguicore.toggle_samba(usb_id, True)
                self._portalwebguicore.toggle_ftp(usb_id, True)
                self._portalwebguicore.toggle_dlna(usb_id, True)
                self._portalwebguicore.apply_no_reload()
            self.check_samba_status(usb_id, True)
            self.check_ftp_status(usb_id, True)
            self.check_dlna_status(usb_id, True)

########## UTIL #########
    def _get_iface_code(self, iface):
        if "2.4" == iface:
            return 0
        elif "5" == iface:
            return 1

    def _get_encryption_code(self, encryption):
        if "WPA2" == encryption:
            return "psk2"
        elif "WPA/WPA2" == encryption:
            return "psk-mixed+tkip+aes"
        else:
            return "none"

    def _get_default_info(self):
        return self._openwrtcore.compute_default_info()

    def _log_wan_info(self):
        logger.debug("WAN mode: " + self._openwrtcore._get_wan_mode(), True)
        logger.debug("IP address: " + self._openwrtcore._get_wan_ipaddr(), True)
        logger.debug("Gateway: " + self._openwrtcore._get_wan_gateway(), True)
        logger.debug("Netmask: " + self._openwrtcore._get_wan_netmask(), True)
        logger.debug("DNS server: " + self._openwrtcore._get_dns(), True)

    def _log_portal_wireless_info(self):
        iface = 0
        logger.debug("2G", True)
        logger.debug("SSID: " + self._openwrtcore._get_ssid(iface), True)
        logger.debug("Password: " + self._openwrtcore._get_password(iface), True)
        logger.debug("Encryption mode: " + self._openwrtcore._get_encryption(iface), True)
        iface = 1
        logger.debug("5G", True)
        logger.debug("SSID: " + self._openwrtcore._get_ssid(iface), True)
        logger.debug("Password: " + self._openwrtcore._get_password(iface), True)
        logger.debug("Encryption mode: " + self._openwrtcore._get_encryption(iface), True)

    def _assert_in_dns_list(self, dns_list, dns_address):
        assert_true(dns_address in dns_list, dns_address + " not shown in web status DNS server list")

if __name__ == '__main__':
    tester = AccessPointWebLibrary()
    tester.init_variable("eth0", "wlan0", "idltest", "192.168.8.1")
