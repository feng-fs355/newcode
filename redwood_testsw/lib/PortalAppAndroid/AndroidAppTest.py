import time
import sys
import os
import atexit
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Library")
from AndroidControl import Android
from TelnetControl import TelnetControl
from Color import Color
from AppiumControl import AppiumControl

class PortalAPPTests(object):
    
    def __init__(self, UUID, port, bootstrapPort, portalID, customizeSSID, customizePWD, version = "6.0", deviceName = "MyPhone"):
        logging.basicConfig(format='[%(asctime)s][%(levelname)s]%(message)s', level=logging.INFO)
        atexit.register(self.exit_handler)
        self.portalID = portalID
        self.customizeSSID = customizeSSID
        self.customizePWD = customizePWD
        self.appiumServer = AppiumControl(port, bootstrapPort, UUID)
        self.appiumServer.start()
        self.appiumController = Android(port = port, platform_version= version, device_name = deviceName)

    def OnBoardStress(self, iteration = 50):    
        logging.info ("Start %s" % sys._getframe().f_code.co_name)
        loop = 0
        
        while True and loop < iteration:
            loop += 1
            try:
                logging.info ("\tTry to Onborad %s" % self.portalID)
		st = time.time()
                self.appiumController.onboard_portal(self.portalID, self.customizeSSID + str(loop), self.customizePWD)
                et = time.time() - st
                self.appiumController.check_internet()
                self.appiumController.delete_network()
                time.sleep(20)
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                logging.error("%s Run %s %sFail%s" % (__name__, loop, Color.FAIL,Color.ENDC))
                logging.debug(sys.exc_info())
                print e
                sys.exit()

            logging.info("Run %s %sPass%s with onboarding time: %d seconds" % (loop, Color.PASS, Color.ENDC, et))
            et = None
	self.appiumController.close_appium_session()
    def exit_handler(self):
        self.appiumServer.stop()

if __name__ == "__main__":
    v = sys.argv
    print v
    """
    v[1]: UUID
    v[2]: port
    v[3]: bootstrapPort
    v[4]: Portal-ID
    v[5]: customize password
    v[6]: iteration
    """
    tester = PortalAPPTests(v[1], int(v[2]), int(v[3]), v[4], v[4] + "-auto", v[5])
    tester.OnBoardStress(int(v[6]))
