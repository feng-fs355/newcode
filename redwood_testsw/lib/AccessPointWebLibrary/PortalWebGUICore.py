import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from robot.api import logger
from sets import Set

class PortalWebGUICore(object):

    ########### Browser control ###########
    def openUrl(self, url, title):
        logger.debug("Opening URL to " + url + " with title: " + title)
        try:
            self.browser.get(url)
            assert title in self.browser.title
            time.sleep(1)
            return True
        except TimeoutException:
            logger.debug("TimeoutException raised from Opening URL")
            self._close()
            return False

    def _inputElement(self, name, text):
        for i in range(0, 10, 1):  # 20170314 feng change to 10 sec


            try:
                elem = self.browser.find_element_by_name(name)
                elem.send_keys(text)
                errmsg ="You entered the wrong password"
                p=assert_equal(errmsg, errmsg_result, "You entered the wrong password")
                logger.info(p)
            except NoSuchElementException:
                time.sleep(2)
                logger.debug("NoSuchElementException raised from inputElement\tname: " + str(name) + ", text: " + str(text))
                continue
            except WebDriverException:
                logger.debug("WebDriverException raised from inputElement\tname: " + str(name) + ", text: " + str(text))
                self.refresh_page()

    def _btnElement(self, name, click = True, by_id = None):
        logger.debug("Button element " + name + ", click: " + str(click) + ", by_id: " + str(by_id))
        for i in range(0, 5, 1):
            try:
                if by_id:
                    btn = self.browser.find_element_by_id(name)
                else:
                    btn = self.browser.find_element_by_name(name)
                if click:
                    btn.click()
                break
            except NoSuchElementException:
                logger.console("\n No object ,-> PortalWebGUICore.py line :40")
                time.sleep(2)
                logger.debug("NoSuchElementException raised from btnElement\tname: " + str(name) + ", click: " + str(click) + ", by_id: " + str(by_id))
                continue
            except WebDriverException:
                logger.console("\n No Web driver object ,-> PortalWebGUICore.py line :40")
                logger.debug("WebDriverException raised from btnElement\tname: " + str(name) + ", click: " + str(click) + ", by_id: " + str(by_id))
                self.refresh_page()

    def _linkElement(self,name):
        #feng add
        logger.console("\n  PortalWebGUICore.py / def _linkElement ")
        logger.console("\nTrying to find element in the web : "+name+" \n")
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_element_by_link_text(name)
                elem.click()
                break
            except NoSuchElementException:
                return False
                time.sleep(2)
                logger.debug("NoSuchElementException raised from linkElement\tname: " + str(name))
                continue
            except WebDriverException:
                logger.debug("WebDriverException raised from linkElement\tname: " + str(name))
                self.refresh_page()

    def _cssSelector(self, css_selector, text = None):
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_element_by_css_selector(css_selector)
                if text:
                    elem.clear()
                    elem.send_keys(text)
                else:
                    elem.click()
                break
            except NoSuchElementException:
                time.sleep(2)
                logger.debug("NoSuchElementException raised from cssSelector\tcss selector: " + str(css_selector) + " text: " + str(text))
                continue
            except WebDriverException:
                logger.debug("WebDriverException raised from cssSelector\tcss selector: " + str(css_selector) + " text: " + str(text))
                self.refresh_page()

    def _xpathElement(self, name, text = None):
        # feng add
        logger.console("\n --> In web find element")
        logger.console("\n"+name)
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_element_by_xpath(name)
                #feng add
                logger.console(elem)
                if text:
                    elem.clear()
                    elem.send_keys(text)
                else:
                    elem.click()
                return True
            except NoSuchElementException:
                #feng
                return False               
                logger.console("\n --> No element Exception , PortalWebGUICore.py def _xpathElement")
                logger.debug("NoSuchElementException raised from xpathElement\tname: " + str(name) + " text: " + str(text))
                time.sleep(2)
            except WebDriverException:
                #feng
                return False
                logger.console("\n --> web driver element Exception, PortalWebGUICore.py def_xpathElement")
                logger.debug("WebDriverException raised from xpathElement\tname: " + str(name) + " text: " + str(text))
                self.refresh_page()
        return False

    def _clickButtonByName(self, name):
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_elements_by_name(name)
                elem.click()
                return True
            except NoSuchElementException:
                logger.debug("NoSuchElementException raised from clickButtonByName\tname: " + str(name))
                time.sleep(2)
            except WebDriverException:
                logger.debug("WebDriverException raised from clickButtonByName\tname: " + str(name))
                self.refresh_page()
        return False

    def _findElementByName(self, name):
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_elements_by_name(name)
                return True
            except NoSuchElementException:
                logger.debug("NoSuchElementException raised from findElementName\tname: " + str(name))
                time.sleep(2)
            except WebDriverException:
                logger.debug("WebDriverException raised from _findElementByName\tname: " + str(name))
                self.refresh_page()
        return False

    def _captureWebInfo(self, pathName):
        for i in range(0, 3, 1):
            try:
                
                #driver.find_element_by_xpath("//p[contains(.,'ip-address-class-type')]")
                elem = self.browser.find_element_by_xpath(pathName)
                #feng
                logger.console("\nTring to find element in the web page is : "+pathName)
                return elem.text
            except NoSuchElementException:
                time.sleep(1)
                logger.debug("NoSuchElementException raised from captureWebInfo\tpathname: " + str(pathName))
                continue
            except WebDriverException:
                logger.debug("WebDriverException raised from captureWebInfo\tpathname:" + str(pathName))
                self.refresh_page()

    def _getUrl(self):
        url = self.browser.current_url
        url = url.split("!")[1]
        return url

    def _isCheckboxChecked(self, elem_name, is_xpath = None):
        try:
            if is_xpath :
                elem = self.browser.find_element_by_xpath(elem_name)
            else :
                elem = self.browser.find_element_by_id(elem_name)
            return elem.is_selected()
        except NoSuchElementException:
            # feng tag
            logger.console("\n No button -> isCheckboxChecked in PortalWebGUICore.py / def _isCheckboxChecked")            
            logger.debug("NoSuchElementException raised from isCheckboxChecked\telem_name: " + str(elem_name) + "is_xpath: " + str(is_xpath))

    def _login(self, url, title, user = None, pwd = None):
        if self.openUrl(url, title):
            """ 
             20170125 ,As computer performance issue, need wait web page on
             delay 5sec
            """
            #-------------------
            #
            #--------------------
            self._inputElement("password", pwd)
            self._btnElement("submit")
            #-----------------------------
            time.sleep(5)
            #-------------------------------
            return True

        return False

    def _logout(self):
        self._linkElement("Logout")

    def if_web_disconnect(self):
        if self._captureWebInfo("//h1[contains(.,'Unable to connect')]"):
            self.refresh_page()

    def open_website(self, url, title, pwd, browser = None):
        #feng 
        logger.console("\n -->PortalWebGUICore.py  / def open_website")
        logger.console("\n"+url)        
        #--------------------------------------------
        logger.debug("Opening website to " + url)
        if not browser:
            self.browser = webdriver.Firefox()
            self.browser.set_page_load_timeout(180)
            isLogin = self._login(url, title, pwd = pwd)
            self.url = url
            time.sleep(2)
            return isLogin

    def _close(self):
        logger.debug("Closing browser")
        self.browser.quit()

    def _apply(self):
 
        try:
            #feng add
            logger.console("Apply -> PortalWebGUICore.py -> def _apply")
            #----------------------------------------------------------- 
            logger.debug("Applying command (sleeps 35 second after apply)")
            current_url = self._getUrl()
            #feng add 20170105
            logger.console("\n current_url = "+current_url )
            self._xpathElement('//button[@type=\'submit\']', None)
            time.sleep(40)  # feng change 35 to 40
            if 'login' in self.browser.current_url:
                self._login('http://192.168.8.1', 'Portal', pwd='password')
                self.go_to_page(current_url)
        except TimeoutException:
            logger.warn("Time out when apply")

    def _fast_apply(self):  # bypass 30 sec wait after apply
        try:
            current_url = self._getUrl()
            self._xpathElement('//button[@type=\'submit\']', None)
            # time.sleep(32)
            time.sleep(8)
            if 'login' in self.browser.current_url:
                self._login('http://192.168.8.1', 'Portal', pwd='password')
                self.go_to_page(current_url)
        except TimeoutException:
            logger.warn("Time out when refreshing")

    def apply_no_reload(self):
        current_url = self._getUrl()
        self._xpathElement('//button[@type=\'submit\']', None)
        time.sleep(2)
        if 'login' in self.browser.current_url:
            self._login('http://192.168.8.1', 'Portal', pwd='password')
            self.go_to_page(current_url)

    def refresh_page(self, current_url = None):
        logger.debug("refreshing page\nCurrent url: " + self.browser.current_url)
        if not current_url:
            current_url = self._getUrl()
        self.browser.refresh();
        if 'login' in self.browser.current_url:
            self._login('http://myportalwifi.com', 'Portal', pwd='password')
            self.go_to_page(current_url)
        time.sleep(5) #feng change 3 to 5 20170127

    def go_to_page(self, link):
        if link not in self.browser.current_url:
            self.browser.get('http://192.168.8.1/#!' + link)
            time.sleep(2)

    ########### Status ###########
    def _check_2g_status(self):
        time.sleep(10) # feng add
        logger.debug("Checking 2g status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("Wireless (2.4G)")
        time.sleep(2)

        ssid = self._captureWebInfo("//td[contains(.,'Name (SSID)')]/following-sibling::td")

        logger.console("find ssid is: "+str(ssid))


        encryption = self._captureWebInfo("//td[contains(.,'Encryption')]/following-sibling::td")
        logger.console("find encryption is: "+str(encryption))
        return (ssid, encryption)

    def _check_5g_status(self):
        logger.debug("Checking 5g status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("Wireless (5G)")
        time.sleep(2)
        ssid = self._captureWebInfo("//td[contains(.,'Name (SSID)')]/following-sibling::td")
        encryption = self._captureWebInfo("//td[contains(.,'Encryption')]/following-sibling::td")
        return (ssid, encryption)

    def _check_attach(self, ip_address, iface, scanning_time = 1, cycle_time = 0):
        logger.debug("Checking attached devices\tip address: " + str(ip_address))
        self.refresh_page()
        for i in range(0, scanning_time, 1):
            time.sleep(2)  
            self._linkElement("Status")            
            time.sleep(2)
            self._linkElement("Attached Devices")            
            time.sleep(10) # feng add 20170125 ,the 1.2.116 attached page response too slow,need include timer.
            msg = self._captureWebInfo("//td[contains(.,'%s')]/following-sibling::td" %ip_address)

            #feng add
            logger.console(msg)
            #-------------------
            if msg:
                break
            time.sleep(cycle_time)
        return msg

    def _check_lan_status(self):
        logger.debug("Checking lan status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("LAN")
        time.sleep(2)
        ip_address = self._captureWebInfo("//td[contains(.,'IP Address')]/following-sibling::td")
        subnet_mask = self._captureWebInfo("//td[contains(.,'Subnet Mask')]/following-sibling::td")
        return (ip_address, subnet_mask)

    ########### Wireless Configuration ###########
    def _broadcast_ssid(self, frequency, enable = None):
        logger.debug("Setting " + frequency + " ssid broadcast to " + str(enable))
        checkUrl = "/wireless/configuration/%sg" %frequency
        currentUrl = self._getUrl()
        if checkUrl != currentUrl:
            self._linkElement("Wireless Configuration")
            time.sleep(2)
            self._linkElement(str(frequency) + "G SSID")
            time.sleep(2)
        if self._isCheckboxChecked("togglecomp") is not enable :
            self._btnElement("togglecomp", by_id = True)

    def _change_ssid(self, frequency, ssid):
        logger.debug("Changing " + frequency + " ssid to " + ssid)
        checkUrl = "/wireless/configuration/%sg" %frequency
        currentUrl = self._getUrl()
        if checkUrl != currentUrl:
            self._linkElement("Wireless Configuration")
            time.sleep(3) #feng change 2 to 3
            self._linkElement(str(frequency) + "G SSID")
            time.sleep(3) #feng change 2 to 3
        self._cssSelector('input[type="text"]', ssid)


    def _change_encryption_mode(self, frequency, encryption):
        logger.debug("Changing " + frequency + " encryption mode to " + encryption)
        checkUrl = "/wireless/configuration/%sg" %frequency
        currentUrl = self._getUrl()
        if checkUrl != currentUrl:
            self._linkElement("Wireless Configuration")
            time.sleep(2)
            self._linkElement(str(frequency) + "G SSID")
            time.sleep(2)
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div' +
                '/div/div[2]/div/div[2]/div', None)
        time.sleep(2)
        if encryption == "none" :
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div/' +
                    'div/div[2]/div/div[2]/div/div[2]/div', None)

        elif encryption == "psk2" :
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div/div/' +
                    'div[2]/div/div[2]/div/div[2]/div[2]', None)

        elif encryption == "psk-mixed+tkip+aes" :
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div/div/' +
                    'div[2]/div/div[2]/div/div[2]/div[3]', None)

    def _change_network_password(self, frequency, pwd):
        logger.debug("Changing " + frequency + " network password to " + pwd)
        checkUrl = "/wireless/configuration/%sg" %frequency
        currentUrl = self._getUrl()
        if checkUrl != currentUrl:
            self._linkElement("Wireless Configuration")
            time.sleep(2)
            self._linkElement(str(frequency) + "G SSID")
            time.sleep(2)
        self._cssSelector('input[type="password"]', pwd)

    ########### WAN IP ###########
    def get_wan_connection_status(self):
        if 'status/wan' != self._getUrl():
            self._linkElement("Status")
            time.sleep(2)
            self._linkElement("WAN")
            time.sleep(2)
        return self._captureWebInfo("//td[contains(.,'Connection')]/following-sibling::td")

    def get_wan_dns(self):
        if 'status/wan' != self._getUrl():
            self._linkElement("Status")
            time.sleep(2)
            self._linkElement("WAN")
            time.sleep(2)
        dns_server = Set()
        ip_address = self._captureWebInfo("//td[contains(.,'Domain Name Server')]/following-sibling::td")
        dns_server.add(str(ip_address))
        while True:
            ip_address = self._captureWebInfo("//td[contains(.,'%s')]/../following-sibling::tr" %ip_address)
            if not ip_address:
                break
            dns_server.add(str(ip_address))
        return dns_server

    def get_wan_ip_and_subnet(self):
        if 'status/wan' != self._getUrl():
            self._linkElement("Status")
            time.sleep(2)
            self._linkElement("WAN")
            time.sleep(2)
        ip_address = self._captureWebInfo("//td[contains(.,'IP Address')]/following-sibling::td")
        subnet_mask = self._captureWebInfo("//td[contains(.,'Subnet Mask')]/following-sibling::td")
        return ip_address, subnet_mask

    def configure_wan_dhcp(self):
        logger.debug("Configuring wan dhcp")
        try:
            self._toggle_dynamic_wan_ip(False)  # prevent case where pppoe not turned off
            self._toggle_dynamic_wan_ip(True)
            self._apply()
        except TimeoutException:
            logger.warn("Webpage timeout from configuring wan dhcp")

    def configure_wan_static(self, ip_address=None, gateway=None, netmask=None):
        #feng add 1228
        logger.console("\nTrriger WAN setting using PortalWebGUICore.py /  def configure_wan_static")        
        logger.debug("configuring with wan static")
        try:
            self._toggle_dynamic_wan_ip(False)
            time.sleep(2)
            self._enter_static_wan_ip(ip_address, gateway, netmask)
            self._apply()
        except TimeoutException:
            logger.warn("Webpage timeout from configuring wan static")

    def configure_wan_pppoe(self, username=None, password=None, service_name=None):
        logger.debug("configuring with wan pppoe")
        try:
            self._toggle_dynamic_wan_ip(True)
            self._toggle_pppoe_require_username(True)
            time.sleep(2)
            self._enter_pppoe_username_password(username, password, service_name)
            self._fast_apply()
        except TimeoutException:
            logger.warn("Webpage timeout from configuring wan pppoe")

    def _configure_dns(self, primary, backup=None):
        logger.debug("Configuring DNS")
        checkUrl = "/wan/domain-name-server-address"
        currentUrl = self._getUrl()
        if checkUrl != currentUrl:
            self._linkElement("WAN IP")
            time.sleep(2)
            self._linkElement("Domain Name Server Address")
            time.sleep(2)
        self._cssSelector('input[type="text"]', primary)
        if backup: self._xpathElement('(//input[@type=\'text\'])[2]', backup)

    def _toggle_dynamic_wan_ip(self, enable):
        #feng add 2017/1/5
        logger.console("\nTrue = Enable / False = Disable\n")
        logger.console(enable)
        self._linkElement("WAN IP")
        time.sleep(2)
        self._linkElement("Connection Accessibility")
        time.sleep(2)
        if self._isCheckboxChecked("togglecomp") is not enable :
            self._btnElement("togglecomp", by_id = True)

    def _enter_static_wan_ip(self, ip_address=None, gateway=None, netmask=None):
        self._linkElement("WAN IP")
        time.sleep(2)
        self._linkElement("Connection Accessibility")
        time.sleep(2)

        if ip_address:
            self._cssSelector('input[type="text"]', ip_address)
        if netmask:
            self._xpathElement('(//input[@type=\'text\'])[2]', netmask)
        if gateway:
            self._xpathElement('(//input[@type=\'text\'])[3]', gateway)

    def _toggle_pppoe_require_username(self, enable):
        self._linkElement("WAN IP")
        time.sleep(2)
        self._linkElement("Connection Accessibility")
        time.sleep(2)
        if self._isCheckboxChecked('(//input[@id=\'togglecomp\'])[2]', is_xpath = True) is not enable :
            self._xpathElement('(//input[@id=\'togglecomp\'])[2]', None)

    def _enter_pppoe_username_password(self, username=None, password=None, service_name=None):
        self._linkElement("WAN IP")
        time.sleep(2)
        self._linkElement("Connection Accessibility")
        time.sleep(2)
        if username:
            self._xpathElement('(//input[@type=\'text\'])[4]', username)
        if password:
            self._cssSelector('input[type="password"]', password)
        if service_name:
            self._xpathElement('(//input[@type=\'text\'])[5]', service_name)

    def _toggle_isp(self, enable = None):
        checkUrl = "/wan/domain-name-server-address"
        currentUrl = self._getUrl()
        if checkUrl != currentUrl:
            self._linkElement("WAN IP")
            time.sleep(2)
            self._linkElement("Domain Name Server Address")
            time.sleep(2)
        if self._isCheckboxChecked("togglecomp") is not enable:
            self._btnElement("togglecomp", by_id = True)

    ########### LAN IP ###########
    def configure_lan_static(self, ip_address = None, subnet_mask = None):
        """
        20170124
        Remark as below:
        self._toggle_dynamic_lan_ip(False)
        self._toggle_dynamic_lan_ip(False)
        self.apply_no_reload() 
        """ 
        #self._toggle_dynamic_lan_ip(False)
        time.sleep(2)
        # feng add 
        logger.console("\n -> Go to PortalWebGUICore.py / def configure_lan_static")
        self._enter_static_lan_ip(ip_address, subnet_mask)
        if subnet_mask:
         #feng add
            logger.console("\n --> Go to PortalWebGUICore.py / def _toggle_dynamic_lan_ip")
            #self._toggle_dynamic_lan_ip(False)  #20170124
            self._apply()
        else:
            logger.console("\n --> Go to PortalWebGUICore.py / def apply_no_reload -> change to self.apply")
            self._apply()            #20170124
            #self.apply_no_reload()  #20170124

    def _try_classd_and_e(self, ip_address):
        self.configure_lan_static(ip_address)
        time.sleep(2)
        #print "ddddd"+self._captureWebInfo("//div[contains(@class,'message expand-error-transition')]")
        #logger.console(self.browser.page_source)
        #return self._captureWebInfo("//div[contains(@class,'message expand-error-transition')]")
        #return self._captureWebInfo("//div[contains(@class,'message')]")
        #driver.find_element_by_xpath("//p[contains(.,'ip-address-class-type')]")
        #20170124 modify as below:
        return self._captureWebInfo("//p[contains(.,'ip-address-class-type')]")

    def _toggle_bridge_mode(self, enable = None):
        #feng add
        logger.console("\n For Toggle Bridge mode--> use selenium PortalWebGUICore.py :line 494\n")
        self._linkElement("LAN IP")
        time.sleep(2)
        if self._isCheckboxChecked("togglecomp") is not enable :
            self._btnElement("togglecomp", by_id = True)

    def _toggle_dynamic_lan_ip(self, enable = None):
        # feng add 
        logger.console("\n -> PortalWebGUICore.py / def _linkElement")
        self._linkElement("LAN IP")
        time.sleep(2)
        if self._isCheckboxChecked("(//input[@id=\'togglecomp\'])[2]", is_xpath =True) is not enable :
            self._xpathElement("(//input[@id=\'togglecomp\'])[2]", None)

    def _enter_static_lan_ip(self, ip_address = None, subnet_mask = None):
        #feng
        print ("\nTO SETTING up LAN Static IP Address")

        self._linkElement("LAN IP")
        time.sleep(2)
        if ip_address:
            self._cssSelector('input[type="text"]', ip_address)
        if subnet_mask:
            self._xpathElement('(//input[@type=\'text\'])[2]', subnet_mask)

    def _toggle_dhcp_server(self, enable = None):
        #feng add
        logger.console("toggile dhcp server , in the PortalWebGUICore.py - lin 542\n")
        self._linkElement("LAN IP")
        time.sleep(2)
        #feng ----modify 
        if self._isCheckboxChecked('(//input[@id=\'togglecomp\'])[3]', is_xpath = True) is not enable :
            self._xpathElement('(//input[@id=\'togglecomp\'])[3]', None)
        #-----------------
    def _enter_start_server_ip_range(self, start_ip = None, end_ip = None):
        self._linkElement("LAN IP")
        time.sleep(2)
        if start_ip:
            self._xpathElement('(//input[@type=\'text\'])[3]', start_ip)
        if end_ip:
            self._xpathElement('(//input[@type=\'text\'])[4]', end_ip)

    ########### Firewall ###########
    def delete_inbound_firewall_rule(self):
        self.goto_inbound_page()
        rule_num = self._captureWebInfo("//tr[contains(@class,'headers')]/following-sibling::tr[last()]/td")
        if rule_num:
            for i in range (0, int(rule_num), 1):
                self._cssSelector('a.delete')
                time.sleep(2)
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/div/div[2]/div[2]')
                time.sleep(2)

    def delete_outbound_firewall_rule(self):
        self.goto_outbound_page()
        rule_num = self._captureWebInfo("//tr[contains(@class,'headers')]/following-sibling::tr[last()]/td")
        if rule_num:
            for i in range (0, int(rule_num), 1):
                self._cssSelector('a.delete')
                time.sleep(2)
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/div/div[2]/div[2]')
                time.sleep(2)

    def goto_inbound_page(self):
        if "firewall" not in self.browser.current_url:
            self._linkElement("Firewall")
            time.sleep(2)
        if "inbound" not in self.browser.current_url:
            self._linkElement("Inbound Rules")
            time.sleep(2)

    def goto_outbound_page(self):
        if "firewall" not in self.browser.current_url:
            self._linkElement("Firewall")
            time.sleep(2)
        if "outbound" not in self.browser.current_url:
            self._linkElement("Outbound Rules")
            time.sleep(2)

    def goto_mac_filter_page(self):
        if "firewall" not in self.browser.current_url:
            self._linkElement("Firewall")
            time.sleep(2)
        if "mac-filtering" not in self.browser.current_url:
            self._linkElement("MAC Filtering")
            time.sleep(2)

    def block_all_devices(self):
        self.goto_mac_filter_page()
        time.sleep(2)
        self._btnElement("togglecomp", by_id = True)
        self._xpathElement("//span[@id='app']/div/div/section/div[2]/form/button")

    def block_specific_device(self, devices_ip):
        self.goto_mac_filter_page()
        time.sleep(2)
        self._xpathElement("//td[contains(.,'%s')]/following-sibling::td[contains(@class,'toggle')]/div/div/input[@id='togglecomp']" %(devices_ip))
        self._xpathElement("//span[@id='app']/div/div/section/div[2]/form/button")

    def check_service_name(self):
        return "" == self._captureWebInfo("//label[contains(.,'Service Name')]/following-sibling::div")

    def check_port(self):
        return "" == self._captureWebInfo("//label[contains(.,'Port')]/following-sibling::div")

    def check_inbound_lan_ip(self):
        return "" == self._captureWebInfo("//label[contains(.,'LAN Destination IP')]/following-sibling::div")

    def check_inbound_wan_ip(self):
        return not self._captureWebInfo("//div[contains(@class,'ip-dropdown has_error')]/following-sibling::div")

    def check_outbound_lan_ip(self):
        return "" == self._captureWebInfo("//div[contains(@class,'lan')]/child::div[contains(@class,'message expand-error-transition')]")

    def check_outbound_wan_ip(self):
        return "" == self._captureWebInfo("//div[contains(@class,'wan')]/child::div[contains(@class,'message expand-error-transition')]")

    def set_service_name(self, service_name):
        self._cssSelector('input[type="text"]', service_name)

    def set_port(self, port):
        self._xpathElement('(//input[@type=\'text\'])[2]', port)

    def set_protocal(self, protocal):
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div[2]/div[3]/div', None)
        time.sleep(2)
        if protocal.lower() == "tcp" :
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[3]/div/div[2]/div')
        elif protocal.lower() == "udp" :
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[3]/div/div[2]/div[2]')

        elif protocal.lower() == "tcp/udp" :
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[3]/div/div[2]/div[3]')

    def edit_inbound(self, service_name = None, port = None, protocal = None, lan_ip = None,
            wan_source = None, wan_start_ip = None, wan_end_ip = None):
        self.goto_inbound_page()
        self._cssSelector("a.edit")
        time.sleep(2)
        #Servic Name
        if service_name:
            self._xpathElement("(//input[@type=\'text\'])[7]", service_name)
        #Port
        if port:
            self._xpathElement("(//input[@type=\'text\'])[8]", port)
        #Protocal
        if protocal:
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/div[2]/div/form/div/div[3]/div')
            time.sleep(2)
            if protocal.lower() == "tcp":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[3]/div/div[2]/div')
            elif protocal.lower() == "udp":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[3]/div/div[2]/div[2]')
            elif protocal.lower() == "tcp/udp":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[3]/div/div[2]/div[3]')
                #LAN IP
        if lan_ip:
            self._xpathElement('(//input[@type=\'text\'])[9]', lan_ip)
        #WAN IP
        if wan_source:
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/div[2]/div/form/div/div[6]/div/div')
            time.sleep(2)
            if wan_source.lower() == "any":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[6]/div/div/div[2]/div')
            elif wan_source.lower() == "single":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[6]/div/div/div[2]/div[2]')
                time.sleep(2)
                self._xpathElement('(//input[@type=\'text\'])[10]', wan_start_ip)
            elif wan_source.lower() == "range":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[6]/div/div/div[2]/div[3]')
                time.sleep(2)
                self._xpathElement('(//input[@type=\'text\'])[11]', wan_start_ip)
                self._xpathElement('(//input[@type=\'text\'])[12]', wan_end_ip)

        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/div[2]/div[2]/div[2]')
        time.sleep(2)

    def configure_inbound(self, service_name, port, protocal, lan_ip,
            wan_source, wan_start_ip = None, wan_end_ip = None):
        self.goto_inbound_page()
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/button', None)
        time.sleep(2)
        #Service Name
        self.set_service_name(service_name)
        #Port
        self.set_port(port)
        #Protocol
        self.set_protocal(protocal)
        #LAN IP
        self._xpathElement('(//input[@type=\'text\'])[3]', lan_ip)
        #WAN IP
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                '/form/div[2]/div[6]/div/div/div')
        time.sleep(2)
        if wan_source.lower() == "any":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[6]/div/div//div[2]/div')
        elif wan_source.lower() == "single":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[6]/div/div/div[2]/div[2]')
            time.sleep(2)
            self._cssSelector('div.singleIp > div.inline.field > input[type="text"', wan_start_ip)
        elif wan_source.lower() == "range":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[6]/div/div/div[2]/div[3]')
            time.sleep(2)
            self._cssSelector('div.rangeIp > div.inline.field > input[type="text"]', wan_start_ip)
            self._xpathElement('(//input[@type=\'text\'])[6]', wan_end_ip)

        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div[2]/div[9]/button')
        time.sleep(2)

    def edit_outbound(self, service_name = None, port = None, protocal = None, lan_source = None, wan_source = None,
            lan_start_ip = None, lan_end_ip = None, wan_start_ip = None, wan_end_ip = None):
        self.goto_outbound_page()
        self._cssSelector('a.edit')
        time.sleep(2)
        #Service Name
        if service_name:
            self._xpathElement('(//input[@type=\'text\'])[9]', service_name)
        #Port
        if port:
            self._xpathElement('(//input[@type=\'text\'])[10]', port)
        #Protocal
        if protocal:
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/div[2]/div/form/div/div[3]/div')
            time.sleep(2)
            if protocal.lower() == "tcp":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[3]/div/div[2]/div')
            elif protocal.lower() == "udp":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[3]/div/div[2]/div[2]')
            elif protocal.lower() == "tcp/udp":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[3]/div/div[2]/div[3]')
        #LAN IP
        if lan_source:
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/div[2]/div/form/div/div[5]/div/div/div')
            time.sleep(2)
            if lan_source.lower() == "any":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[5]/div/div/div/div[2]/div')
            elif lan_source.lower() == "single":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[5]/div/div/div/div[2]/div[2]')
                time.sleep(2)
                self._xpathElement('(//input[@type=\'text\'])[11]', lan_start_ip)
            elif lan_source.lower() == "range":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[5]/div/div/div/div[2]/div[3]')
                time.sleep(2)
                self._xpathElement('(//input[@type=\'text\'])[12]', lan_start_ip)
                self._xpathElement('(//input[@type=\'text\'])[13]', lan_end_ip)
        #WAN IP
        if wan_source:
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/div[2]/div/form/div/div[6]/div/div/div')
            time.sleep(2)
            if wan_source.lower() == "any":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[6]/div/div/div/div[2]/div')
            elif wan_source.lower() == "single":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[6]/div/div/div/div[2]/div[2]')
                time.sleep(2)
                self._xpathElement('(//input[@type=\'text\'])[14]', wan_start_ip)
            elif wan_source.lower() == "range":
                self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                        '/div[2]/div/form/div/div[6]/div/div/div/div[2]/div[3]')
                time.sleep(2)
                self._xpathElement('(//input[@type=\'text\'])[15]', wan_start_ip)
                self._xpathElement('(//input[@type=\'text\'])[16]', wan_end_ip)

        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/div[2]/div[2]/div[2]')
        time.sleep(2)

    def configure_outbound(self, service_name, port, protocal, lan_source, wan_source,
            lan_start_ip = None, lan_end_ip = None, wan_start_ip = None, wan_end_ip = None):
        self.goto_outbound_page()
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/button', None)
        time.sleep(2)
        #Service Name
        self.set_service_name(service_name)
        #Port
        self.set_port(port)
        #Protocol
        self.set_protocal(protocal)
        #LAN IP
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                '/form/div[2]/div[5]/div/div/div', None)
        time.sleep(2)
        if lan_source.lower() == "any":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[5]/div/div/div/div[2]/div', None)
        elif lan_source.lower() == "single":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[5]/div/div/div/div[2]/div[2]', None)
            time.sleep(2)
            self._cssSelector('div.singleIp > div.inline.field > input[type="text"]', lan_start_ip)
        elif lan_source.lower() == "range":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[5]/div/div/div/div[2]/div[3]', None)
            time.sleep(2)
            self._cssSelector('div.rangeIp > div.inline.field > input[type="text"]', lan_start_ip)
            self._xpathElement('(//input[@type=\'text\'])[5]', lan_end_ip)
        time.sleep(2)
        #WAN IP
        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                '/form/div[2]/div[6]/div/div/div', None)
        time.sleep(2)
        if wan_source.lower() == "any":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[6]/div/div/div/div[2]/div', None)
        elif wan_source.lower() == "single":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[6]/div/div/div/div[2]/div[2]', None)
            time.sleep(2)
            self._cssSelector('div.wan > div.ip-dropdown > div.singleIp > div.inline.field > input[type="text"]', wan_start_ip)
        elif wan_source.lower() == "range":
            self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]' +
                    '/form/div[2]/div[6]/div/div/div/div[2]/div[3]', None)
            time.sleep(2)
            self._cssSelector('div.wan > div.ip-dropdown > div.rangeIp > div.inline.field > input[type="text"]', wan_start_ip)
            self._xpathElement('(//input[@type=\'text\'])[8]', wan_end_ip)

        self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/div[2]/div[7]/button', None)
        time.sleep(2)

    def configure_dmz(self, ip_address):
        self._linkElement("Firewall")
        time.sleep(2)
        self._linkElement("DMZ")
        time.sleep(2)
        self._cssSelector('input[type="text"]', ip_address)
        self._xpathElement("//span[@id='app']/div/div/section/div[2]/form/button", None)
        time.sleep(2)

    def delete_dmz(self):
        self._linkElement("Firewall")
        time.sleep(2)
        self._linkElement("DMZ")
        time.sleep(2)
        self._xpathElement("//span[@id='app']/div/div/section/div[2]/form/button[2]", None)
        time.sleep(2)

    ########### Storage ###########
    def _goto_usb_page_slot(self, usb_id):
        if "storage" not in self.browser.current_url:
            self._linkElement("Storage")
            #feng add 20170126 delay 10
            #------------------------
            time.sleep(10)
            #------------------------
            #time.sleep(2)
        if "usb-" + str(usb_id) not in self.browser.current_url:
            self._linkElement("USB " + str(usb_id))
            time.sleep(2)

    def check_usb_status(self, usb_id):

        self._goto_usb_page_slot(usb_id)
        return self._xpathElement("//button[@type='submit']")

    def check_usb_controller(self, usb_id):
        self._goto_usb_page_slot(usb_id)
        #feng add delay(1)
        #-----------------
        time.sleep(1)
        #------------------
        return self._captureWebInfo("//button[contains(@class,'ui right floated button small dark')]")

    def check_usb_format(self, usb_id):
        self._goto_usb_page_slot(usb_id)
        return self._captureWebInfo("//td[contains(.,'File System Type')]/following-sibling::td")

    def check_usb_is_ejected(self, usb_id):
        self._goto_usb_page_slot(usb_id)
        if not self._findElementByName('Storage'):
            self.refresh_page()
            #feng add 20170126
            #driver.find_element_by_xpath("//button[contains(.,'Detect')]")
        AAA=self._captureWebInfo("//button[contains(@class,'ui right floated button small dark')]/preceding-sibling::div")
        AAA=str(AAA)
        logger.console("Capture data is :  "+AAA)
        return self._captureWebInfo("//button[contains(@class,'ui right floated button small dark')]/preceding-sibling::div")

    def eject_usb(self, usb_id):
        self._goto_usb_page_slot(usb_id)
        # return if the eject button is clicked
        time.sleep(6)
        if not self._findElementByName('Storage'):
            self.refresh_page()
        return self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/button', None)

    def detect_usb(self, usb_id):
        self._goto_usb_page_slot(usb_id)
        time.sleep(6)
        if not self._findElementByName('Storage'):
            self.refresh_page()
        return self._xpathElement('//span[@id=\'app\']/div/div/section/div[2]/form/button', None)

    def toggle_samba(self, usb_id, enable=None):
        self._goto_usb_page_slot(usb_id)
        # 20170202 change enable to True
        if self.samba_status(usb_id) is not True :
            self._btnElement("togglecomp", by_id=True)

    def toggle_ftp(self, usb_id, enable=None):
        self._goto_usb_page_slot(usb_id)
        # 20170202 change enable to True
        if self.ftp_status(usb_id) is not True :
            self._xpathElement('(//input[@id=\'togglecomp\'])[2]', None)

    def toggle_dlna(self, usb_id, enable=None):  # 20170202

        self._goto_usb_page_slot(usb_id)
        logger.console("\ndlan status is : "+str(self.dlna_status(usb_id)))
        # 20170202 change enable to True
        if self.dlna_status(usb_id) is not True : 
            logger.console("Trigger dlna feature.....")
            self._xpathElement('(//input[@id=\'togglecomp\'])[3]', None)

    def samba_status(self, usb_id):
        return self._isCheckboxChecked("togglecomp")

    def ftp_status(self, usb_id):
        return self._isCheckboxChecked('(//input[@id=\'togglecomp\'])[2]', is_xpath=True)

    def dlna_status(self, usb_id):
        #feng add
        #-----------------
        #tme.sleep(20)
        #-----------------
        return self._isCheckboxChecked('(//input[@id=\'togglecomp\'])[3]', is_xpath=True)

    def can_connect_dlna(self):
        self.browser.get(self.url + ':8200')
        return self._findElementByName('MiniDLNA status')


    ########## Router password ############
    def change_router_password(self, pwd):
        self._linkElement("Admin Password")
        time.sleep(2)
        self._cssSelector('input[type="password"]', pwd)
        self._xpathElement('(//input[@type=\'password\'])[2]', pwd)

if __name__ == '__main__':
    tester = PortalWebGUICore()
    tester.open_website("http://192.168.8.1", "Portal", "password")
    print tester._try_classd_and_e("244.1.1.1")
