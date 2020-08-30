"""
    This module should cover all redwood manager API.
"""
import os
import sys
sys.path.append(os.getcwd() + "/lib/redwood/rwm/imp/cli/")
import ast
import re

from robot.api import logger

import RWMCliCore

class RWMLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'
    """
        RWMLibrary is for connect to ``redwood manager`` and performe actions(mainly method calls)
        It's currently supporting CLI via ip socket, see RWMCliCore.py for more details.
        Bluetooth scoket will be supported later.
    """

    def __init__(self):
        self._rwm = RWMCliCore.RWMCliCore(None)
        self._manamger_id = ""

    def send_raw_command(self, method, parameter):
        """
        This method is used to send raw command to RWM.

        Examples:
        | Send Raw Command | wlan.intf.get | none |
        | Send Raw Command | wlan.ap.statecontrol | {'action':'restart','BSSID':'123'} |
        """
        if parameter is "" or "none" in parameter:
            parameter = {}
        else:
            parameter = ast.literal_eval(parameter)
        return self._rwm.send_command(method, parameter)

    def manager_status(self):
        method = "manager.status"
        param = none
        self.send_raw_command(method, param)
        
    def wlan_ap_test_forcedfs(self, channel = 0):
        """
        [ Not yet done ] Calls wlan.ap.test.forcedfs

        Examples:
        | wlan Ap Test Forcedfs | 1 |
        """
        method = "wlan.ap.test.forcedfs"
        self._rwm._send_api_command(method,channel)

    def connect_to_socket(self, host = "127.0.0.1", port = 9000):
        """
        Connect to host socket.
        Default:
            127.0.0.1:9000
        Examples:
        | Connect To Socket | 192.168.1.100 | 58888 |
        """
        self._rwm.connect_socket(host,int(port))

    def close_socket(self):
        """
        Close socket
        Would be save to call it at the end of test
        """
        self._rwm.colse_socket()

    def status_check(self, actual_status, expected_status = 0):
        """
        Verify the status return by RWM
        Raise error if status not expected.
        """
        if int(actual_status) != int(expected_status):
            raise AssertionError('Unexpected result status %s' % (actual_status))

    def wait_for_notification(self, method, expected_key = None, expected_value = None, timeout = 10):
        """
            Waiting for given notification ``method`` for ``timeout`` seconds.

            Notification method name is required. Expected_key and expected_value are optional.

        """
        msg_list = []

        msg_list = self._rwm.wait_for_notification(method, timeout)
        if not msg_list:
            raise AssertionError("No notification for method: %s" % (method))

        if expected_key:
            expected_key = str(expected_key)
            if expected_key in str(msg_list):
                for msg in msg_list:
                    re_pattern = re.compile(r'("'+ re.escape(expected_key) + r'": \[\{{1}.*\}\]{1})')
                    results = re.findall(re_pattern, msg)
                    if not results:
                        re_pattern = re.compile(r'("'+ re.escape(expected_key) + r'": "{0,1}[0-9A-Za-z_ :-]*"{0,1}),')
                        results = re.findall(re_pattern, msg)
                    print results
            else:
                raise AssertionError("Key %s not found" % (expected_key))

        return 0
