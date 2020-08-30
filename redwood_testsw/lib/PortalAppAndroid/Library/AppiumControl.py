import subprocess
import psutil
import logging
import time

LOG_FILE = "appium_server.log"
HOST = "127.0.0.1"

class AppiumControl(object):
    def __init__(self, port, bp, uuid, server = HOST, logfile = LOG_FILE):
        self.port = port
	self.bp = bp
	self.uuid = uuid
	self.host = server
        self.logfile = logfile

    def start(self):
	cmd = "appium -a %s -p %d -bp %d -U %s --log %s" % (self.host, self.port, self.bp, self.uuid, self.logfile)
	self.appium = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while True:
            if "listener started" in self.appium.stdout.readline():
                break
            time.sleep(1)
	logging.info("Appium server started.")

    def stop(self, force = True):
	ps = psutil.Process(self.appium.pid)
	for sps in ps.children(recursive=True):
	    sps.kill()
	ps.kill()
	logging.info("Appium server stoped.")
