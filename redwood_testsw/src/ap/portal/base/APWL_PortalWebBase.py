import os
import sys
import time
from robot.api import logger

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from robot.api import logger
from sets import Set

parentdir = os.path.dirname(os.path.realpath(__file__))
# TODO: clean up the path
sys.path.append(parentdir + "/../../../../lib/ap")
from AccessPointWebLibrary import AccessPointWebLibrary
# TODO: clean up the path
sys.path.append(parentdir + "/../../../../lib/log")
from LogCaptureLibrary import LogCaptureLibrary

class APWL_PortalWebBase(AccessPointWebLibrary, LogCaptureLibrary):

    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

    HTML_TITLE = "Portal"
    BROWSER = None

    def __init__(self):
        self.pwc = _PortalWebController()

    ### AccessPointWebLibrary ###
    def set_web_driver(self, web_driver):
        logger.info("\nCreating web driver: " + web_driver)
        self.BROWSER = web_driver
        return

    def login(self, host_ip, user_name = None, pwd = None):
        logger.info("\nlogin web with: " + user_name + ":" + pwd)
        return self.pwc.open_and_login("http://" + host_ip, self.HTML_TITLE, pwd, self.BROWSER)

    def logout(self):
        return self.pwc.logout()

    def get_net_settings(self, port):
        if port.upper() == "LAN":
            s = self.pwc.get_lan_status()
        elif port.upper() == "WAN":
            s = self.pwc.get_wan_status()
        else:
            logger.error("port: %s not defined." % (port))
            raise ValueError
        settings = super(APWL_PortalWebBase, self)._DS_Net_Settings(connection_status = s['connection_status'],
            ip_address = s['ip_address'], subnet_mask = s['subnet_mask'],
            mac_address = s['mac_address'], dns_server = s['dns_server'])
        return settings

    def get_wlan_settings(self, band, iface):
        if band.upper() == "2G" or band.upper() == "2.4G":
            s = self.pwc.get_2g_status(iface)
        elif band.upper() == "5G":
            s = self.pwc.get_5g_status(iface)
        else:
            logger.error("band: %s not defined." % (band))
            raise ValueError
        settings = super(APWL_PortalWebBase, self)._DS_Wlan_Settings(ssid = s['ssid'],
            channel = s['channel'], mode = s['mode'],
            mac_address = s['mac_address'], encryption = s['encryption'])
        return settings

    def get_version_info(self):
        s = self.pwc.get_router_info()
        info = super(APWL_PortalWebBase, self)._DS_Router_Info(hw_ver = s['hw_ver'],
            sw_ver = s['sw_ver'], time_zone = s['time_zone'])
        return info

    def get_attached_devices(self, band, iface_type = None):
        sl = self.pwc.get_attached_devices(band, iface_type)
        if not sl:
            logger.info("No connected devices on %s %s." %(band, iface_type))
            return None
        dev = []
        for s in sl:
            logger.debug("device: %s" % s)
            dev.append(super(APWL_PortalWebBase, self)._DS_Attached_Device(ip_address = s['ip'],
                mac_address = s['mac'], device_name = s['name'], alias_name = s['alias']))
        return dev

    def close_browser(self):
        return self.pwc.close()

    ### LogCaptureLibrary ###
    def start_log_capture(self, path = None, file_name = None):
        self.outpath = path + "/"
        if not file_name.endswith(".png"):
            file_name += ".png"
        fn = "start_" + file_name
        self.pwc.save_screenshot(self.outpath + fn)
        print('*HTML* <img src="' + fn + '" alt="' + fn + '">')
        return file_name

    def stop_log_capture(self, log_id):
        fn = "stop_" + log_id
        self.pwc.save_screenshot(self.outpath + fn)
        print('*HTML* <img src="' + fn + '" alt="' + fn + '">')
        return True

### Private Class ###
"""
This class implements web controller for Portal, it's using selenium web driver to control web page.
"""
class _PortalWebController(object):
    def open_url(self, url = None, title = None):
        logger.debug("Opening URL to " + url + " with title: " + title)
        if url is not None:
            self.url = url
        if title is not None:
            self.title = title
        try:
            self.browser.get(self.url)
            assert self.title in self.browser.title
            time.sleep(1)
            return True
        except TimeoutException:
            logger.debug("TimeoutException raised from Opening URL")
            self.close()
            return False

    def login(self, url = None, title = None, user = None, pwd = None):
        if self.open_url(url, title):
            if pwd is not None:
                self.pwd = pwd
            self._inputElement("password", self.pwd)
            self._btnElement("submit")
            return True
        return False

    def logout(self):
        self._linkElement("Logout")

    def if_web_disconnect(self):
        if self._captureWebInfo("//h1[contains(.,'Unable to connect')]"):
            self.refresh_page()

    def open_and_login(self, url, title, pwd, browser = None):
        logger.debug("Opening website to " + url)
        if not browser or browser.lower() == "firefox":
            self.browser = webdriver.Firefox()
            self.browser.set_page_load_timeout(180)
            isLogin = self.login(url, title, pwd = pwd)
            self.url = url
            time.sleep(2)
            return isLogin
        else:
            logger.error("webdriver %s not support." % (browser))
            return False

    def apply_no_reload(self):
        current_url = self._getUrl()
        self._xpathElement('//button[@type=\'submit\']', None)
        time.sleep(2)
        if 'login' in self.browser.current_url:
            self.login()
            self.go_to_page(current_url)

    def refresh_page(self, current_url = None):
        logger.debug("refreshing page\nCurrent url: " + self.browser.current_url)
        if not current_url:
            current_url = self._getUrl()
        self.browser.refresh();
        if 'login' in self.browser.current_url:
            self.login()
            self.go_to_page(current_url)
        time.sleep(3)

    def go_to_page(self, link):
        if link not in self.browser.current_url:
            self.browser.get('http://' + self.url + '/#!' + link)
            time.sleep(2)

    def save_screenshot(self,filepath):
        self.browser.save_screenshot(filepath)

    def close(self):
        logger.debug("Closing browser")
        self.browser.quit()

    ### Status ###
    def get_lan_status(self):
        logger.debug("Checking lan status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("LAN")
        time.sleep(2)

        lan_settings = {
            'connection_status': self._captureWebInfo("//td[contains(.,'Connection')]/following-sibling::td"),
            'ip_address': self._captureWebInfo("//td[contains(.,'IP Address')]/following-sibling::td"),
            'subnet_mask': self._captureWebInfo("//td[contains(.,'Subnet Mask')]/following-sibling::td"),
            'mac_address': self._captureWebInfo("//td[contains(.,'MAC Address')]/following-sibling::td"),
            'dns_server': self._captureWebInfo("//td[contains(.,'Domain Name Server')]/following-sibling::td")
        }
        return lan_settings

    def get_wan_status(self):
        logger.debug("Checking wan status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("WAN")
        time.sleep(2)

        wan_settings = {
            'connection_status': self._captureWebInfo("//td[contains(.,'Connection')]/following-sibling::td"),
            'ip_address': self._captureWebInfo("//td[contains(.,'IP Address')]/following-sibling::td"),
            'subnet_mask': self._captureWebInfo("//td[contains(.,'Subnet Mask')]/following-sibling::td"),
            'mac_address': self._captureWebInfo("//td[contains(.,'MAC Address')]/following-sibling::td"),
            'dns_server': self._captureWebInfo("//td[contains(.,'Domain Name Server')]/following-sibling::td")
        }
        return wan_settings

    def get_2g_status(self, iface):
        logger.debug("Checking 2.4G status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("Wireless (2.4G)")
        time.sleep(2)
        settings = {
            'ssid': self._captureWebInfo("//td[contains(.,'Name (SSID)')]/following-sibling::td"),
            'channel': self._captureWebInfo("//td[contains(.,'Channel')]/following-sibling::td"),
            'mode': self._captureWebInfo("//td[contains(.,'Mode')]/following-sibling::td"),
            'mac_address': self._captureWebInfo("//td[contains(.,'MAC')]/following-sibling::td"),
            'encryption': self._captureWebInfo("//td[contains(.,'Encryption')]/following-sibling::td")
        }
        return settings

    def get_5g_status(self, iface):
        logger.debug("Checking 5g status")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("Wireless (5G)")
        time.sleep(2)
        settings = {
            'ssid': self._captureWebInfo("//td[contains(.,'Name (SSID)')]/following-sibling::td"),
            'channel': self._captureWebInfo("//td[contains(.,'Channel')]/following-sibling::td"),
            'mode': self._captureWebInfo("//td[contains(.,'Mode')]/following-sibling::td"),
            'mac_address': self._captureWebInfo("//td[contains(.,'MAC')]/following-sibling::td"),
            'encryption': self._captureWebInfo("//td[contains(.,'Encryption')]/following-sibling::td")
        }
        return settings

    def get_router_info(self):
        logger.debug("Checking router informaiton")
        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("Router Information")
        time.sleep(2)
        info = {
            'hw_ver': self._captureWebInfo("//td[contains(.,'Hardware Version')]/following-sibling::td"),
            'sw_ver': self._captureWebInfo("//td[contains(.,'Firmware Version')]/following-sibling::td"),
            'time_zone': self._captureWebInfo("//p[contains(.,'timezone')]").split('timezone: ')[1]
        }
        return info

    def get_attached_devices(self, band, iface_type):
        s = ""
        xpath = "table"
        if band == "wired":
            s = "Wired Devices"
            xpath = "div/" + xpath
        elif "2.4" in band:
            if iface_type == "guest":
                s = "2.4 GHz Guest Wireless Devices"
            else:
                s = "2.4 GHz Wireless Devices"
        elif "5" in band:
            if iface_type == "guest":
                s = "5 GHz Guest Wireless Devices"
            else:
                s = "5 GHz Wireless Devices"
        else:
            logger.error("Attached device for %s %s not exist" %(band, iface_type))
            raise ValueError

        logger.debug("Checking attached devices\t on: %s" % (s))

        self._linkElement("Status")
        time.sleep(2)
        self._linkElement("Attached Devices")
        time.sleep(15)
        msg = self._captureWebInfo("//h4[contains(.,'%s')]/following-sibling::%s/tbody" % (s, xpath))
        dl = msg.split("\n")
        list_info = []
        if len(dl) <= 1:
            return None
        else:
            del dl[0]
            for d in dl:
                logger.debug("device:%s." % d)
                di = d.split(" ")
                info = {
                    'ip': str(di[1]),
                    'mac': str(di[2]),
                    'name': str(di[3]),
                    'alias': str(di[4])
                }
                list_info.append(info)

        return list_info

    ### elements ###
    def _inputElement(self, name, text):
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_element_by_name(name)
                elem.send_keys(text)
                break
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
                time.sleep(2)
                logger.debug("NoSuchElementException raised from btnElement\tname: " + str(name) + ", click: " + str(click) + ", by_id: " + str(by_id))
                continue
            except WebDriverException:
                logger.debug("WebDriverException raised from btnElement\tname: " + str(name) + ", click: " + str(click) + ", by_id: " + str(by_id))
                self.refresh_page()

    def _linkElement(self,name):
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_element_by_link_text(name)
                elem.click()
                break
            except NoSuchElementException:
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
        for i in range(0, 5, 1):
            try:
                elem = self.browser.find_element_by_xpath(name)
                if text:
                    elem.clear()
                    elem.send_keys(text)
                else:
                    elem.click()
                return True
            except NoSuchElementException:
                logger.debug("NoSuchElementException raised from xpathElement\tname: " + str(name) + " text: " + str(text))
                time.sleep(2)
            except WebDriverException:
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
                elem = self.browser.find_element_by_xpath(pathName)
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
            logger.debug("NoSuchElementException raised from isCheckboxChecked\telem_name: " + str(elem_name) + "is_xpath: " + str(is_xpath))

    def _apply(self):
        try:
            logger.debug("Applying command (sleeps 35 second after apply)")
            current_url = self._getUrl()
            self._xpathElement('//button[@type=\'submit\']', None)
            time.sleep(35)
            if 'login' in self.browser.current_url:
                self.login()
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
                self.login()
                self.go_to_page(current_url)
        except TimeoutException:
            logger.warn("Time out when refreshing")

if __name__ == '__main__':
    print 'Subclass:', issubclass(APWL_PortalWebBase, AccessPointWebLibrary)
    print 'Instance:', isinstance(APWL_PortalWebBase(), AccessPointWebLibrary)
    print 'Subclass:', issubclass(APWL_PortalWebBase, LogCaptureLibrary)
    print 'Instance:', isinstance(APWL_PortalWebBase(), LogCaptureLibrary)