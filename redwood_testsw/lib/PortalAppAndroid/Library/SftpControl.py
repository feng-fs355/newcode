import paramiko
from paramiko import SFTPClient

class SftpControl(object):
    def _init_(self):
        self.host = "172.16.20.242"
        self.port = "22"
        self.user = "idlall"
        self.pwd  = "5733158"
        self.apkdir = "/redfs01/apps/portalapp/latest/"
        self.apk = "portalapp-ppe*-release.apk"       
        
    def fileget(self):
        transport = paramiko.Transport(self.host, self.port)
        transport.connect(username = self.user, password = self.pwd)
        sstp = SFTPClient.from_transport(self.transport)
        sstp.get(self.apkdir, self.apk)
        
if __name__ == '__main__':
    sftp = SftpControl()
    sftp.fileget()