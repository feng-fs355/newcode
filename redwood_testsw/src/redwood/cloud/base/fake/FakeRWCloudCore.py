import os
import socket
import ssl
import json
import select
import thread
import threading
import time
import sys
sys.path.append(os.getcwd() + "/lib/redwood/rwm/imp/cli/")
sys.path.append(os.getcwd() + "/lib/redwood/utils/")

import RWMCliCore
import RWCloudSocketAutoHandlerLibrary

class FakeRWCloudCore(object):

    __initialized = False
    def __init__(self):
        working_dir = os.getcwd()
        if self.__initialized:
            return
        self.certfile = working_dir + '/lib/redwood/rwm/cli.cer'
        self.keyfile = working_dir + '/lib/redwood/rwm/cli.key'
        self.backlog = 1

        self.__initialized = True
        self.manager_registered = False
        self.__wait_timeup = True
        print("Cloud initialize.")

    def start(self, port = 62300):
        self.port = int(port)
        self.__openSocket()
        self.manager_registered = False
        while not self.manager_registered:
            readable,writable,exceptional = select.select([self.server_sock], [], [], 1)

            for server_sock in readable:
                if server_sock is self.server_sock:
                    try:
                        client_sock, address = server_sock.accept()
                        client_sock = ssl.wrap_socket(sock = client_sock,
                                                  server_side = True,
                                                  certfile = self.certfile,
                                                  keyfile = self.keyfile)
                        print("Server accepted client connection, address " + str(address))
                        self.client_socket = RWMCliCore.RWMCliCore(client_sock)
                        self.client_socket_listener = RWCloudSocketAutoHandlerLibrary.RWCloudSocketAutoHandler(client_sock, True)
                        self.client_socket_listener_thread = thread.start_new_thread(self.client_socket_listener.listener, (client_sock,))

                        while self.client_socket_listener.is_listener_started() is not True:
                            time.sleep(1)
                            pass
                        self.manager_registered = True

                    except:
                        print sys.exc_info()
                        continue

    def close(self):
        self.manager_registered = False
        self.client_socket.colse_socket()
        self.__closeSocket()

    def send_command(self, methodName, params, srcEpid = 255, destEpid = 1):
        msg_id = self.client_socket.write(methodName, params, int(srcEpid), int(destEpid))
        return self.client_socket_listener.get_socket_response(msg_id)

    def is_manager_registerd(self):
        return self.manager_registered

    def wait_for_notification(self, methodName, timeout):

        timeout = int(timeout)
        self.__wait_timeup = False
        timer = threading.Timer(timeout, self.__times_up)
        timer.start()

        mesg = []
        while not self.__wait_timeup:
            resp = self.client_socket_listener.get_socket_response(methodName)
            if not resp:
                break
            mesg.append(resp)
        return mesg

    def subscribe_notification(self, method, destEpid):
        self.client_socket_listener.subscribe_notification(method, destEpid)


    def __openSocket(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server.setblocking(0)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_sock.bind(("", self.port))
        print("Socket bind on Port = {0}".format(self.port))

        self.server_sock.listen(self.backlog)
        print("Socket server start listening")

    def __closeSocket(self):
        self.server_sock.close()
        print("Socket server closed")

    def __times_up(self):
        self.__wait_timeup = True