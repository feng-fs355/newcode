import os
import random
import time
import urllib2
import unittest
import appium
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

class FailedActionError(Exception):
    """A specified phone action failed to execute properly"""
    pass

class Android(object):
    def __init__(self, port, unicode_keyboard = None,
            platform_version = None, device_name = None, apk_file = None):

        #appImageName    = apk_file

        #curDir = os.path.dirname(os.path.abspath(__file__))
        #apk = curDir + "/" + appImageName

        desired_caps = {}
        desired_caps['newCommandTimeout'] = '300'
        desired_caps['platformName'] = "Android"
        desired_caps['platformVersion'] = platform_version
        desired_caps['deviceName'] = device_name
        #desired_caps['app'] = apk
        desired_caps['appPackage'] = 'com.portalwifi.portal.ppe'
        desired_caps['appActivity'] = 'com.ignitiondl.portal.MainActivity'
        self.driver = webdriver.Remote(('http://127.0.0.1:%d/wd/hub' % port), desired_caps)
	self.permission = False
        self.port = port
    
    def launch_app():
        desired_caps = {}
    
    ###start up page###
    def click_buy(self):
        """Click buy button at the portal app start up page."""
        buy_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/buy_button")
        buy_btn.click()
    
    def click_setup(self):
        """Click setup button at the portal app start up page."""
        setup_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/setup_button")
        setup_btn.click()
    
    ###On-boarding###
    def click_next(self, count = 1):
        """Click next button at the on-bording page."""
        for i in range(0, count, 1):
	    next_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/button_next")
	    next_btn.click()
	    time.sleep(1)

    def click_next_to_find_portal(self):
        """Click next button at the Locating-your-portal page."""
        next_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/button_1")
        next_btn.click()
     
    def click_for_allow(self):
        """Click allow button at the portal ask for device to allow to get location info"""
        try:
	    allow_btn = self.find_element_by_id("com.android.packageinstaller:id/permission_allow_button")
	except:
	    return	    
        allow_btn.click()
        self.permission = True
        
    def scrollToPortal(self, name, maxswipes=10):
        """Scroll until finds name element.
        Times out after 15 seconds.
        """
        count = 0
        page_last_portal = []
        prev_search_last_portal = ""
        #print prev_search_last_portal
        while True:
            portal_list = self.driver.find_elements_by_id("com.portalwifi.portal.ppe:id/portal_name")
            # Check if hit end of list
            page_last_portal += portal_list[-1].text
            if prev_search_last_portal == portal_list[-1].text:
                #print "end"
                raise FailedActionError("Portal %s not found." %name)
            prev_search_last_portal = portal_list[-1]
            for elem in portal_list:
                if name in elem.text:
                    #logger.console("Element %s is found" %elem.text)
                    target_portal = elem
                    target_portal.click()
                    return elem
            self.driver.swipe(start_x=360, start_y=900, end_x=360, end_y=300, duration=2000)
            if count == maxswipes:
                #logger.console("Cannot find Portal %s after %s swipes" % (name, maxswipes))
                raise FailedActionError("Portal ID: %s not found in list. Exiting." %name)
            count += 1
            time.sleep(1)

    def click_pair(self):
        """Click setup button at the portal app start up page."""
        pair_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/button_1")
        pair_btn.click()
         
    ### Page "Setup your network" #####
    def set_name_pw(self, ssid, pwd):
        # Network Name
        """Click name button at the Setup your network page."""
        network_name = self.find_element_by_id("com.portalwifi.portal.ppe:id/ssid_edit", 90)
        network_name.click()
        network_name.send_keys(ssid)
        print("        ssid ok.")
        # Password
        """Click password button at the Setup your network page."""
        network_pwd = self.find_element_by_id("com.portalwifi.portal.ppe:id/password_edit",90)
        network_pwd.click()
        network_pwd.send_keys(pwd)
        print("        pwd ok.")

    def click_apply_for_network_customize(self):
        """Click apply button at the Setup your network page."""
        apply_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/button_apply")
        apply_btn.click()
    
    def click_home(self):
        """Click home button at the "All done!" page."""
        home_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/button_home",90)
        home_btn.click()
        
    ### Page "Internet" ###
    def show_wan_ip(self):
        wan_ip = self.find_element_by_id("com.portalwifi.portal.ppe:id/wan_ip")
        print ("            Wan IP Address = " + wan_ip.text)
    ### Page "Portal Home" ###
    def click_net_setting(self):
        """Click setting button at the Portal Home page."""
        setting_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/network_settings")
        setting_btn.click()
        
    def click_internet_btn(self):
        internet_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/internet_button")
        internet_btn.click()
        
    def click_portal_btn(self):
        portal_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/portal_button")
        portal_btn.click()
        
    def click_add_portal_btn(self):
        add_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/add_new_portal")
        add_btn.click()
        
    def click_guest_btn(self):
        guest_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/guests_button")
        guest_btn.click()
        
    def click_device_btn(self):
        device_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/devices_button")
        device_btn.click()
        
    def click_toolbar_back(self):
        back_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/toolbar_back")
        back_btn.click()
        
    ### Page "Basic Device Setting" ###
    def click_show_advance_switch(self):
        switch_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/show_advance_switch")
        switch_btn.click()
        
    def click_bridge_mode(self):
        bridge_mode_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/bridge_mode_enabled_switch")
        bridge_mode_btn.click()
    
    def click_apply_setting(self):
        apply_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/apply_settings")
        apply_btn.click()
    
    ### Page "Add new Portal to my network"
    def click_continue_to_add_portal(self):
        continue_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/button_2")
        continue_btn.click()
    
    ### Page "User and Guests" ###
    def click_add_guest_network(self):
        add_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/add_new_guest_network")
        add_btn.click()
    
    ### Page "Network Setting"
    def click_check_update(self):
        check_update_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/network_settings")
        check_update_btn.click()
        
    def click_delete_network(self):
        delete_network_btn = self.find_element_by_id("com.portalwifi.portal.ppe:id/delete_network_button")
        delete_network_btn.click()
        
    def click_apply_for_delete_network(self):
        time.sleep(3) # TODO remove this, use wait_for
        apply_btn = self.driver.find_element_by_xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.Button[2]')
        apply_btn.click()
        
    ### Function ###
    def check_internet(self):
        print("        Check Internet IP Address")
        self.click_internet_btn()
        self.show_wan_ip()
        self.click_toolbar_back()
        
    def onboard_portal(self, potalid, ssid, password):
        print("        On borading Portal")
        time.sleep(10)
        self.click_setup()
        self.click_next(4)
        if not self.permission and self.port == 5000:
	    self.click_next_to_find_portal()
            self.click_for_allow()
            print("        Allow Location Done." )
        time.sleep(20)
        self.scrollToPortal(potalid)
        self.click_pair()
        time.sleep(20)
        self.set_name_pw(ssid, password)
        self.click_apply_for_network_customize()
        time.sleep(20)
        self.click_home()
        time.sleep(10)  
    
    def enable_bridge_mode(self):
        print("        Enter Portal Device Enable bridge mode")   
        self.click_portal_btn()
        self.click_show_advance_switch()
        time.sleep(20)
        self.click_bridge_mode()
        self.click_apply_setting()
        time.sleep(60)
        self.click_toolbar_back()
    
    def set_guest_network(self, ssid, pwd):
        print("        Add Guest Network")
        self.click_guest_btn()
        self.click_add_guest_network()
        self.set_name_pw(ssid, pwd)
        self.click_apply_setting()
        time.sleep(120)
        self.click_toolbar_back()
    
    def add_new_portal(self, potalid):
        print("        Add Mesh AP into network")
        self.click_add_portal_btn()
        self.click_continue_to_add_portal()
        self.scrollToPortal(potalid)
        self.click_pair()
        time.sleep(240)
        print("        Mesh has been created!!!")
        
    def delete_network(self):
        print ("        Delete Network ")
        self.click_net_setting()
        self.click_delete_network()
        self.click_apply_for_delete_network()
 
    def close_appium_session(self):
        self.driver.quit()
        time.sleep(10)
        print ("        Session terminated")
 
    ### Tool###
    def find_element_by_id(self, _id, timeout=10):
        """Custom find element by id with a 10 sec wait for item to show up"""
        self.wait_for_id(_id, timeout)
        return self.driver.find_element_by_id(_id)
 
    def wait_for_id(self, _id, timeout=20):
        """Wait for id element to show up
        Has a default 10 sec timeout.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, _id))
                    )
            return True
        except TimeoutException:
            print ("Can not find button")
            self.close_appium_session()
            return False
        
if __name__ == '__main__':
    apptest = Android()
    #apptest.click_home()
    apptest.close_appium_session()
    #apptest.onboard_portal("1AA1", "IDLtest", "12345678")
