import os
import sys
sys.path.append(os.getcwd() + "/lib/ap/imp/openwrt")

from OpenWrtCore import OpenWrtCore, OpenWrtError

from robot.api import logger

class AccessPointLibrary(object):
    """Test library for testing *OpenWrt* commands.

    Interacts with the access point via telnet, and using OpenWrt api method.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

    def __init__(self):
        logger.console("create new OpenWrtCore")
        self._openwrtcore = OpenWrtCore()
        self._result = ''

    def create_telnet_connection(self, host = '127.0.0.1', prompt = '~$', user = None, password = None):
        """Create telnet connection to access point. ``mandotory``

        connect to given host using robot telnet library

        Examples:
        | Create Telnet Connection | 192.168.1.1 | /# |
        | Create Telnet Connection | 192.168.1.1 | /# | root | root |
        """
        self._openwrtcore._connect(host, prompt, user, password)

    def send_cmd(self, cmd):
        return self._openwrtcore._send_cmd(cmd)

    def set_ssid(self, ssid):
        return self._openwrtcore._set_ssid(ssid)

    def get_ssid(self, iface = "2G"):

        if "2G" == iface:
            iface = 0
        elif "5G" == iface:
            iface = 1

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
