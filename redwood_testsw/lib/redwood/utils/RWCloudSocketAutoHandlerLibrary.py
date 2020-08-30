import select
import struct
import pyjsonrpc
import json
import thread
import socket
import time
import Queue

HEADER_SEPERATOR = 29
HEADER_RESERVERD = 0
HEADER_MANAGER   = 1
HEADER_CLOUD     = 255

HEARTBEAT_INTERVAL = 15

JSONPRC_REQUEST  = 0
JSONRPC_RESPONSE = 1
JSONRPC_NOTIFICATION = 2

SOCET_RESPONSE_TIMEOUT = 10
MAX_RESPONSE_QUEUE_SIZE = 30

class RWCloudSocketAutoHandler(object):

    def __init__(self, rw_socket, heart_beat_enable = False):
        print "RWCloudSocketAutoHandler init"
        self.running = True
        #RPC methods
        methods = {
                "cloud.register"   : self.__cloudRegister,
                "cloud.unregister" : self.__cloudUnregister,

                "manager.agent.announce" : self.__managerAgentAnnounce,
                "manager.agent.attach": self.__managerAgentAttach,
                "manager.agent.detach": self.__dummpyEventHandler,

                "wlan.event.scanresult": self.__wlanEventScanresult,
                "wlan.ap.event.dfslist": self.__dummpyEventHandler,
                "wlan.ap.event.radar": self.__dummpyEventHandler,
                "wlan.ap.event.statechange": self.__dummpyEventHandler,
                "wlan.event.scanresult": self.__dummpyEventHandler,
                "wlan.event.spectralreport": self.__dummpyEventHandler
        }
        self.rpc = pyjsonrpc.JsonRpc(methods)
        self.__client_sock = rw_socket
        self.__heartbeat_started = False
        self.__listener_started = False
        self.__heartbeat_enable = heart_beat_enable
        self.__socket_response_queue = Queue.Queue(maxsize = MAX_RESPONSE_QUEUE_SIZE)
        #self.__listener(rw_socket)
        self.subscribe_notification_list = ["manager.agent.announce", "manager.agent.attach", "manager.agent.detach",
                                       "wlan.event.scanresult", "wlan.ap.event.dfslist", "wlan.ap.event.radar",
                                       "wlan.ap.event.statechange", "wlan.event.spectralreport"]

    def get_socket_response(self, msg_id = None):
        counter = 0
        while SOCET_RESPONSE_TIMEOUT > counter:
            if self.__socket_response_queue.empty():
                pass
            else:
                resp = self.__socket_response_queue.get()
                if msg_id in resp or "error" in resp:
                    return resp
            counter += 1
            time.sleep(1)
        return None

    def is_listener_started(self):
        return self.__listener_started

    def subscribe_notification(self, method, destEpid):
        request_json = self.__subscribeEvent(method)
        self.__client_sock.send(self.__createHeader(HEADER_CLOUD, int(destEpid), len(request_json)) + request_json)
        self.get_socket_response("subscr_id")
        return None


    def listener(self, rw_socket):
        while self.running:
            readable,writable,exceptional = select.select([rw_socket], [], [], 1)
            for sock in readable:
                if sock is rw_socket:
                    data = sock.recv(4096)
                    if data:
                        try:
                            jsonData = json.loads(data[8:])
                        except ValueError as err:
                            print err
                            print respStr
                            return
                        except Exception as e:
                            print e
                            print respStr
                            return

                        if 'id' in jsonData:
                            if 'hb-' in str(jsonData['id']):
                                continue

                        if 'sys.linkhb.post' in data:
                            continue

                        #if 'subscr_id' in data:
                        #    continue

                        if 'error' in jsonData:
                            self.__socket_response_queue.put(data[8:])
                            continue

                        (sep, plen, destEpid, srcEpid, reserved, sep) = struct.unpack("=BHBBHB", data[:8])
                        jsonRPCType, jsonRPCObj = self.__socket_parser(data[8:])
                        if jsonRPCType == JSONPRC_REQUEST:
                            sock.send(self.__createHeader(destEpid, srcEpid, len(jsonRPCObj)) + jsonRPCObj)

                        elif jsonRPCType == JSONRPC_NOTIFICATION:
                            if jsonRPCObj.method == "manager.agent.announce":
                                request_json = self.__managerAgentAdd(jsonRPCObj.params["search_req"]["agent_id"])
                                sock.send(self.__createHeader(HEADER_CLOUD, HEADER_MANAGER, len(request_json)) + request_json)
                            else:
                                self.__socket_response_queue.put(jsonRPCObj.to_string())

                        else:
                            self.__socket_response_queue.put(data[8:])

                    if self.__heartbeat_enable and not self.__heartbeat_started:
                            self.__heartbeat_thread = thread.start_new_thread(self.__heartbeat,())
                            self.__heartbeat_started = True


    def __socket_parser(self, jsonStr):
        jsonrpcObj = pyjsonrpc.Request.from_string(jsonStr)
        if jsonrpcObj.method != None:
            try:
                # response_json is procedure result
                response_json = self.rpc.call(jsonrpcObj.to_string())
                response = pyjsonrpc.Response.from_string(response_json)

                # notification
                if not response:
                    print("Receive a notification({0})".format(jsonrpcObj.method))
                    return JSONRPC_NOTIFICATION, jsonrpcObj

                # the request have to response
                if response.result != None or response.error != None:
                    return JSONPRC_REQUEST, response_json
            except:
                print sys.exc_info()
                return None, None
        return None, None

    # response
    def __cloudRegister(self, manager_id, rwunique, ip = None, redirect = None):
        print("cloud.register: manager_id={0}, rwunique={1}".format(manager_id, rwunique))

        response = {
            "status": 0
        }
        return response

    def __cloudUnregister(self, manager_id, rwunique):
        print("cloud.unregister: manager_id={0}, rwunique={1}".format(manager_id, rwunique))
        return None

    # notification
    def __managerAgentAnnounce(self, manager_id, search_req):
        return None

    def __managerAgentAttach(self, manager_id, agent_id, endpoint_id):
        agent = {
            "agent_id": agent_id,
            "epid": endpoint_id
        }
        #TODO: subscribe_notification
        return None

    def __wlanEventScanresult(self):
        return None

    def __dummpyEventHandler(self):
        return None

    def __heartbeat(self):
        request_json = self.__linkHBEnable()
        self.__client_sock.send(self.__createHeader(HEADER_CLOUD, HEADER_MANAGER, len(request_json)) + request_json)

        # subscribe events
        for eventName in self.subscribe_notification_list:
            request_json = self.__subscribeEvent(eventName)
            self.__client_sock.send(self.__createHeader(HEADER_CLOUD, HEADER_MANAGER, len(request_json)) + request_json)
            self.get_socket_response("subscr_id")
        self.__listener_started = True

        count = 0
        time.sleep(HEARTBEAT_INTERVAL)
        while self.running:
            request_json = self.__linkHBPost(count)
            self.__client_sock.send(self.__createHeader(HEADER_CLOUD, HEADER_MANAGER, len(request_json)) + request_json)
            count += 1
            time.sleep(HEARTBEAT_INTERVAL)

    def __linkHBEnable(self):
        return pyjsonrpc.Request(method = "sys.linkhb.enable", id = "0", params = {"timeout": HEARTBEAT_INTERVAL + 10}).to_string()

    def __linkHBPost(self, sequence):
        return pyjsonrpc.Request(method = "sys.linkhb.post", id = "hb-" + str(sequence), params = {"sequence": sequence}).to_string()

    def __createHeader(self, srcEpid, destEpid, dataLength):
        return struct.pack("=BHBBHB", HEADER_SEPERATOR, socket.htons(dataLength), destEpid, srcEpid, HEADER_RESERVERD, HEADER_SEPERATOR)

    def __subscribeEvent(self, name):
        return pyjsonrpc.create_request_json("sys.notifications.subscribe", name = name)

    def __managerAgentAdd(self, agent_id):
        return pyjsonrpc.create_request_json("manager.agent.add", agent_id = agent_id)
