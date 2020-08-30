import os
import thread
import ast
import json
import re
import sys
sys.path.append(os.getcwd() + "/lib/redwood/cloud/imp/fake/")

import FakeRWCloudCore

class RWCloudLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'
    """
        RWCloudLibrary provides the interfaces that are needed when testing ``portal``.
        It will do the following:
            1. Create socket on local machine to simulate redwood cloud.
               Only support one RWM client connection for now.
            2. Manage the client socket (RWM) to receive client packets and to send packets to client.

        All wireless agility commands can be sent via send_raw_command with given
        source endpoint(255 by default) and destination endpoint.
    """
    def __init__(self):
        #init fake server socket
        print "init fake cloud"
        self._server = FakeRWCloudCore.FakeRWCloudCore()

    def start_cloud_socket(self, port):
        """
            Start a socket as cloud socket that waiting RWM to connect.
            Internally, it will start handlers to handle clients requests
            and sending heartbeats periodically.

            It's mandatory for this library to work. Must call this function before use socket related commands.

            Example:
            | Start Cloud Socket | 168168 |
        """
        self.__cloud_socket_handler(port)

    def send_command(self):
        return self._server.send_command()

    def is_manager_registerd(self):
        """
            Use this function to check if the RWM client socket is ready
            This check should be done before sending any commands to RWM.

            Example:
            Use it with robot framework built-in key word: Wait until keyword succeeds.
            | Wait Until Keyword Succeeds | 20 s | 1 s | Is manager registerd |
        """
        if self._server.is_manager_registerd():
            return True
        else:
            raise ValueError('socket not connected yet...')

    def send_raw_command(self, method, parameter, srcEpid = 255, destEpid = None):
        """
            Send raw json packet with given ``method`` and ``parameter`` from given ``srcEpid`` to ``destEpid``.

            ``destEpid`` will be agent or manager.

            Example:
            | Send raw command | ${method} | ${parameter} |
            | Send raw command | ${method} | ${parameter} | ${srcEpid} | ${destEpid} |
        """
        if parameter is "" or "none" in parameter:
            parameter = {}
        else:
            parameter = ast.literal_eval(parameter)

        destEpid = destEpid.replace("\"", "")
        if "agent" == destEpid:
            destEpid = 2
        elif "manager" == destEpid:
            destEpid = 1
        statuscode = self._server.send_command(method, parameter, srcEpid, destEpid)

        return '{"status": ' + str(statuscode) + '}'

    def status_check(self, respsrt, expected_status, expected_key_value = {}):
        """
            Compare the given responsed string to the given status and expected_key_value.

            Will raise AssertionError for unexpected response.
        """
        respsrt = str(respsrt)
        if "None" in respsrt:
            raise AssertionError('Unexpected response %s' % (respsrt))
        elif "Method not found" in respsrt:
            raise AssertionError("Method not found: %s" % (respsrt))
        resp = json.loads(respsrt)
        if "result" in resp:
            if str(expected_status) !=  str(resp['result']['status']):
                raise AssertionError("Status Error(%s != %s)" % (expected_status, resp['result']['status']))

    def wait_for_notification(self, method, expected_key = None, expected_value = None, timeout = 10):
        """
            Waiting for given notification ``method`` for ``timeout`` seconds.

            Notification method name is required. Expected_key and expected_value are optional.

        """
        msg_list = []

        msg_list = self._server.wait_for_notification(method, timeout)
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

    def subscribe_notification(self, method, destEpid):
        self._server.subscribe_notification(method, destEpid)

    def close_cloud(self):
        self._server.close()


    def __cloud_socket_handler(self,port):
        self._server._listener = thread.start_new_thread(self._server.start, (port,))