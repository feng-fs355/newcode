"""
    This module is used to create connection socket to Redwood manager
    and handle the sending/revecing json format packet
"""
import os
import socket
import ssl
import pyjsonrpc
import struct
import json
import ast
import thread
import threading
import sys
sys.path.append(os.getcwd() + "/lib/redwood/utils/")

import RWCloudSocketAutoHandlerLibrary

class RWMCliCore(object):

    def __init__(self, socket_obj):
        #set socket
        working_dir = os.getcwd()
        self.certfile = working_dir + '/lib/redwood/rwm/cli.cer'
        self.keyfile = working_dir + '/lib/redwood/rwm/cli.key'
        self.ca_certs = working_dir + '/lib/redwood/rwm/caroot.crt'
        self.__wait_timeup = True
        if socket_obj:
            print "cloud got socket request"
            self._socket = socket_obj

        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket = ssl.wrap_socket(sock = self._socket,
                                           keyfile = self.keyfile,
                                           certfile = self.certfile,
                                           cert_reqs = ssl.CERT_REQUIRED,
                                           ca_certs = self.ca_certs)
            self._client_socket_listener = None

    def connect_socket(self, host = "127.0.0.1", port = 9000):
        print host + ":" + str(port)
        self._socket.connect((host, port))

        self._client_socket_listener = RWCloudSocketAutoHandlerLibrary.RWCloudSocketAutoHandler(self._socket)
        self._client_socket_listener_thread = thread.start_new_thread(self._client_socket_listener.listener, (self._socket,))

    def colse_socket(self):
        self._socket.close

    def send_command(self, methodName, params,srcEpid = 255,destEpid = 1):
        cmd_id = self.write(methodName, params, srcEpid, destEpid)
        try:
            resp = self._client_socket_listener.get_socket_response(cmd_id)
            if resp:
                result = self.__json_result_parser(resp)
            else:
                result = None
        except:
            print " check: %s " % cmd_id
            return -1
        return result

    def write(self, methodName, params,srcEpid = 255,destEpid = 1):
        json_obj = pyjsonrpc.create_request_json(methodName,**params)
        ascii_gs = 29
        plen = socket.htons(len(json_obj));
        reserved = 0
        json_stream = struct.pack('=BHBBHB', ascii_gs, plen, destEpid, srcEpid, reserved, ascii_gs)
        json_stream += json_obj
        print('--> ' + json_obj)
        self._socket.send(json_stream)
        json_obj = ast.literal_eval(json_obj)
        return json_obj['id']

    def wait_for_notification(self, methodName, timeout):

        timeout = int(timeout)
        self.__wait_timeup = False
        timer = threading.Timer(timeout, self.__times_up)
        timer.start()

        mesg = []
        while not self.__wait_timeup:
            resp = self._client_socket_listener.get_socket_response(methodName)
            if not resp:
                break
            mesg.append(resp)
        return mesg

    def __json_result_parser(self, respStr = None):
        jsonData = json.loads(respStr)
        type_str = ""

        if 'result' in jsonData :
            response = jsonData['result']
            status = jsonData['result']['status']
            print response
        elif 'error' in jsonData :
            response =  jsonData['error']
            status = jsonData['error']['code']
        else :
            print 'Response is missing fields'
            return -1
        response_str = json.dumps(response,sort_keys=False,indent=4)

        return status

    def __times_up(self):
        self.__wait_timeup = True

