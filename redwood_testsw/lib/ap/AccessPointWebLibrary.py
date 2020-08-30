from collections import namedtuple

class AccessPointWebLibrary(object):
    """
    This library is an abstract interface which defines APIs for funtions that are supported
    on an access point web page.

    This library will import the actual implementation for various access point, for example,
    Portal, ASUS, Netgear ... etc. And the implementations for web page control should use
    *Selenium* web drive as preference.
    """

    ### Data Structures ###
    T_Net_Settings = namedtuple("DS_Lan_Settings",
        "connection_status \
        ip_address \
        subnet_mask \
        mac_address \
        dns_server")

    T_Wlan_Settings = namedtuple("DS_Wlan_Settings",
        "ssid \
        channel \
        mode \
        mac_address \
        encryption")

    T_Router_Info = namedtuple("DS_Router_Info",
        "hw_ver \
        sw_ver \
        time_zone")

    T_Attached_Device = namedtuple("DS_Attached_Device",
        "ip_address \
        mac_address \
        device_name \
        alias_name")

    def _DS_Net_Settings(self, connection_status = None, ip_address = None, subnet_mask = None,
                        mac_address = None, dns_server = None):
        return self.T_Net_Settings(str(connection_status), str(ip_address), str(subnet_mask), str(mac_address), str(dns_server))

    def _DS_Wlan_Settings(self, ssid = None, channel = None, mode = None,
                        mac_address = None, encryption = None):
        return self.T_Wlan_Settings(str(ssid), str(channel), str(mode), str(mac_address), str(encryption))

    def _DS_Router_Info(self, hw_ver = None, sw_ver = None, time_zone = None):
        return self.T_Router_Info(str(hw_ver), str(sw_ver), str(time_zone))

    def _DS_Attached_Device(self, ip_address = None, mac_address = None, device_name = None, alias_name = None):
        return self.T_Attached_Device(str(ip_address), str(mac_address), str(device_name), str(alias_name))

    ### General Functions ###
    def set_expected_net_settings(self, connection_status = None, ip_address = None, subnet_mask = None,
                        mac_address = None, dns_server = None):
        """Set the exptected LAN network settings, it includes:
        | connection_status |
        | ip_address |
        | subnet_mask |
        | mac_address |
        | dns_server |

        Examples:
        | set_expected_lan_settings | Up | 192.168.8.1 | 255.255.255.0 | 00:11:22:33:44:55 | 8.8.8.8 |
        """
        return self._DS_Net_Settings(connection_status, ip_address, subnet_mask, mac_address, dns_server)

    def set_expected_wlan_settings(self, ssid = None, channel = None, mode = None,
                        mac_address = None, encryption = None):
        """Set the exptected LAN network settings, it includes:
        | ssid |
        | channel |
        | mode |
        | mac_address |
        | encryption |

        Examples:
        | set_expected_lan_settings | PORTAL_1234 | 1 (2.412 GHz) | 802.11ng | 00:11:22:33:44:55 | psk2 |
        """
        return self._DS_Wlan_Settings(ssid, channel, mode, mac_address, encryption)

    def set_expected_version_info(self, hw_ver = None, sw_ver = None, time_zone = None):
        """Set the exptected version information, it includes:
        | hw_ver |
        | sw_ver |
        | time_zone |

        Examples:
        | set_expected_version_info | Portal_V1.0 | Portal-1.4.138_prod-1.2.116 | UTC |
        """
        return self._DS_Router_Info(hw_ver, sw_ver, time_zone)

    def set_expected_attached_devices(self, ip_address, mac_address, device_name, alias_name = None, append = None):
        if not hasattr(self, 'exp_att_dev_list') or not append:
            self.exp_att_dev_list = []
        self.exp_att_dev_list.append(self._DS_Attached_Device(ip_address, mac_address, device_name, alias_name))
        return self.exp_att_dev_list

    def set_expected_attached_devices_list(self, device_list):
        if len(device_list) == 0 or str(device_list[0]) == "None":
            print("Empty expected devices list")
            return None
        counter = 0
        for d in device_list:
            if counter == 0:
                self.set_expected_attached_devices(d['ip'], d['mac'], d['name'], d['alias'])
            else:
                self.set_expected_attached_devices(d['ip'], d['mac'], d['name'], d['alias'], True)
            counter += 1
        return self.exp_att_dev_list

    ### Abstract Functions ###
    def set_web_driver(self, web_driver):
        """Initialize settings to control AP web page."""
        raise Exception(NotImplemented)

    def login(self, host_ip, user_name = None, pwd = None):
        """Login to web page.

        Examples:
        | Login | 192.168.1.1 |
        | Login | 192.168.1.1 | admin | password |
        """
        raise Exception(NotImplemented)

    def logout(self):
        """Logout, web page will still open and it should prompt to login page.

        Examples:
        | Logout |
        """
        raise Exception(NotImplemented)

    def get_net_settings(self, port = None):
        """Get net settings, it will return:
        | connection_status |
        | ip_address |
        | subnet_mask |
        | mac_address |
        | dns_server |

        Examples:
        | get_net_settings | lan |
        | get_net_settings | wan |
        """
        raise Exception(NotImplemented)

    def get_wlan_settings(self, band = None, iface_type = None):
        """Get wlan settings, it will return:
        | ssid |
        | channel |
        | mode |
        | mac_address |
        | encryption |

        Examples:
        | get_wlan_settings | 2.4G | main |
        | get_wlan_settings | 2.4G | guest |
        | get_wlan_settings | 5G | main |
        | get_wlan_settings | 5G | guest |
        """
        raise Exception(NotImplemented)

    def get_version_info(self):
        """Get version info, it will return:
        | hw_ver |
        | sw_ver |
        | time_zone |

        Examples:
        | get_version_info |
        """
        raise Exception(NotImplemented)

    def get_attached_devices(self, band = None, iface_type = None):
        """Get version info, it will a list of:
        | ip_address |
        | mac_address |
        | device_name |

        Examples:
        | get_attached_devices |
        """
        raise Exception(NotImplemented)

    def set_lan_settings(self):
        """Set LAN settings will return get_lan_settings after set done."""
        raise Exception(NotImplemented)

    def set_wan_settings(self):
        """Set WAN settings will return get_wan_settings after set done."""
        raise Exception(NotImplemented)

    def close_browser(self):
        """Close web page"""
        raise Exception(NotImplemented)