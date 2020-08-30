** Settings ***
Documentation     Testing portal firewall functionality

Library           AccessPointWebLibrary.py
Suite Setup       Setup Telnet and Open Website and Initial variable
Suite Teardown    Close Telnet and Close Website

*** Variables ***
${PC_eth}           eth0               # the wire interface you want to use
${PC_wlan}          wlan0              # the wireless interface you want to use
${PC_user_pwd}      idltest                # your computer's pwd
${Router_IP}              192.168.8.1  # the router's IP
${Remote_PC_IP}           10.10.10.8     # the WAN port PC's IP
${Remote_PC_user_name}    pap1      # the WAN port PC's user name
${Remote_PC_user_pwd}     1234567     # the WAN port PC's password
${PORT_1}                 3000
${PORT_2}                 3010
${PORT_3}                 3020
${PORT_4}                 3030
${IPv4_IP_address}        192.168.8.108


*** Test Cases ***

#1. Allow Inbound TCP Forwarding with any IP
#    Delete inbound firewall rule
#    When inbound WAN source IP is set to any and protocal is TCP
    #All inbound connections should be able to connect to LAN with TCP

    
2. Allow Inbound UDP Forwarding with single IP
   The IP should assign the remote PC's IP
   Delete inbound firewall rule
   When inbound WAN source IP is set to single ip ${Remote_PC_IP} and protocal is UDP
#    Only the ip address should be able to connect to LAN with UDP

#3. Allow Inbound TCP/UDP Forwarding with range IP
## The IP should cover the remote PC's IP
##    Delete inbound firewall rule
##    When inbound WAN source IP is set to a range ${Remote_PC_IP} to 10.10.10.254 and protocal is TCP/UDP
#    Only IP addresses in that range should be able to connect to LAN with TCP/UDP

#4. Comparison the Inbound and DMZ rule priority
##    Delete inbound firewall rule
##    Set firewall inbound rule    test_4    ${PORT_4}    TCP    ${None}    any
##    Configure dmz           192.168.8.150
    #Inbound receive mesg    ${PORT_4}    TCP    ${True}
##    Delete inbound firewall rule
##    Delete DMZ

#5. Blocking Outbound TCP with any LAN IP and any WAN IP
##    Delete outbound firewall rule
##    When outbound WAN destination IP is set to any and protocal is TCP
#    All outbound connections should not be able to connect to LAN with TCP

#6. Blocking Outbound UDP with single LAN IP and single WAN IP
##    Delete outbound firewall rule
##    When outbound WAN destination IP is set to single ${Remote_PC_IP} and protocal is UDP
#    Only the ip address should be not able to connect to WAN with UDP

#7. Blocking Outbound TCP/UDP with range LAN IP and range WAN IP
##    Delete outbound firewall rule
##    When outbound WAN destination IP is set to a range ${Remote_PC_IP} to 10.10.10.254 and protocal is TCP/UDP#
    #Only IP addresses in that range should be able to connect to WAN with TCP/UDP#

#8. Inbound TCP and UDP packets are sent to DMZ host for all ports.
##    Delete outbound firewall rule
##    Configure dmz
#    The all packets through TCP should be received
#    The all packets through UDP should be received
##    Delete DMZ

*** Keyword ***
Setup Telnet and Open Website and Initial variable
    Init variable    ${PC_eth}  ${PC_wlan}  ${PC_user_pwd}  ${Router_IP}  ${Remote_PC_IP}  ${Remote_PC_user_name}  ${Remote_PC_user_pwd}
    #Create telnet connection    ${Router_IP}    ~#    root    CassiniRedwwod42562072Portal
    Disable wifi
    Open website   ${Router_IP}    Portal    password
    Go to page   /firewall/inbound
    #Delete DMZ
    #SSH connect

Close Telnet and Close Website
    Close website
    #Clear all ssh connection
    Enable wifi

### Allow inbound
Inbound WAN source IP is set to any and protocal is ${protocal}
    Set firewall inbound rule    test_1    ${PORT_1}    ${protocal}    ${None}    any

Inbound WAN source IP is set to single ip ${ip_addr} and protocal is ${protocal}
    Set firewall inbound rule    test_2    ${PORT_2}    ${protocal}    ${None}    single    ${ip_addr}

Inbound WAN source IP is set to a range ${ip_start} to ${ip_end} and protocal is ${protocal}
    Set firewall inbound rule    test_3    ${PORT_3}    ${protocal}    ${None}    range    ${ip_start}    ${ip_end}

All inbound connections should be able to connect to LAN with ${protocal}
    Test inbound connection from all    ${PORT_1}   ${protocal}

Only the ip address should be able to connect to LAN with ${protocal}
    Test inbound connection from single ip    ${PORT_2}    ${protocal}

Only IP addresses in that range should be able to connect to LAN with ${protocal}
    Test inbound connection from range ip   ${PORT_3}    ${protocal}

The inbound LAN destination should receive the message with ${protocal}
    Inbound receive mesg    ${PORT_1}    ${protocal}    ${True}

The all packets through ${protocal} should be received
    The all packets should be received    ${protocal}

### Block outbound
Outbound WAN destination IP is set to any and protocal is ${protocal}
    Set firewall outbound rule    test_1   ${PORT_1}   ${protocal}   any   any

Outbound WAN destination IP is set to single ${wan_ip} and protocal is ${protocal}
    Set firewall outbound rule    test_2   ${PORT_2}   ${protocal}   single   single    ${None}    ${None}    ${wan_ip}

Outbound WAN destination IP is set to a range ${wan_start_ip} to ${wan_end_ip} and protocal is ${protocal}
    Set firewall outbound rule    test_3   ${PORT_3}   ${protocal}   range   range    ${None}    ${None}    ${wan_start_ip}    ${wan_end_ip}

All outbound connections should not be able to connect to LAN with ${protocal}
    Test outbound connection to all    ${PORT_1}    ${protocal}

Only the ip address should be not able to connect to WAN with ${protocal}
    Test outbound connection to single ip    ${PORT_2}    ${protocal}

Only IP addresses in that range should be able to connect to WAN with ${protocal}
    Test outbound connection to range ip   ${PORT_3}    ${protocal}

##### MAC filtering
Change 2G SSID
    [Arguments]    ${ssid}
    Change ssid                  2.4    ${ssid}
    Change encryption mode       2.4    None
    Apply
    Wifi connection              ${ssid}
    Delete wifi record           ${ssid}
