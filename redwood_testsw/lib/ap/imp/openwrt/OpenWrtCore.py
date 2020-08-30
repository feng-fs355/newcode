import atexit

from robot.libraries import Telnet
from robot.api import logger

class OpenWrtCore(object):

    def __init__(self):
        logger.console("create new Telnet")
        self._tc = Telnet.Telnet()

    def _connect(self, host = None, prompt = None, user = None, password = None):
        try:
            self._tc.open_connection(host, prompt=prompt, timeout=10)
            if (user is not None):
                self._tc.login(user, password)
            else:
                self._tc.read_until_prompt()
        except:
            raise OpenWrtError('Telnet connection failed')

    def _send_cmd(self, cmd):
        self._result = self._tc.execute_command(cmd)
        return self._result

    def _set_ssid(self, ssid):
        cmd = ""
        self._result = self._tc.execute_command(cmd)

    def _get_ssid(self, iface):
        cmd = "uci get wireless.@wifi-iface["+str(iface)+"].ssid"
        self._result = self._tc.execute_command(cmd)
        return self._result

    def _get_cpuinfo(self):
        cmd = "cat /proc/cpuinfo"
        self._result = self._tc.execute_command(cmd)
        return self._result

    def _get_version(self):
        cmd = "cat /proc/version"
        self._result = self._tc.execute_command(cmd)
        return self._result

    @atexit.register
    def goodbye():
        print "You are now leaving the Python sector."

class OpenWrtError(Exception):
    pass
