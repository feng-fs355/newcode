** Settings ***
Documentation     Testing portal WAN connection.
...               Please ensure that the only connection to outside internet is thru the portal itself.
...               (Turn off other external sources of internet such as wifi).
...               Current test for internet connection uses ping

Library           AccessPointWebLibrary.py
Suite Setup       Setup Telnet and Open Website and Initial variable
Suite Teardown    Close Telnet and Close Website

#TODO sniff package instead of using ping

*** Variables ***
${PC_eth}            eth0           # the wire interface you want to use
${PC_wlan}           wlan0          # the wireless interface you want to use
${PC_user_pwd}       idltest            # your computer's pwd
${Router_IP}         192.168.8.1    # the router's IP

#${PPPoE_usr}         75784377@hinet.net
#${PPPoE_pwd}         ubqxskdc

${PPPoE_usr}         pap1
${PPPoE_pwd}         12345678

${static_ip}         10.10.10.200
${static_netmask}    255.255.255.0
${static_gateway}    10.10.10.254

${google_dns}        8.8.8.8
${public_dns}        172.16.10.242

${fake_dns1}         1.1.1.1
${fake_dns2}         2.2.2.2

${url_1}             www.fast.com
${url_2}             www.amazon.com


*** Test Cases ***
5.1 WAN Static
    When configured to Static
    Should have internet connection

6 DNS
    When configured with Google DNS            # 6.2
    Should have internet connection
    When configured with fake DNS
    Should not be able to ping to domain name
    When Configured to auto DNS and DHCP                # 6.1
    Should have internet connection

3.1 WAN DHCP
    When configured to DHCP
    Configure auto DNS
    Should have internet connection
#    TODO test using different A,B,C channels

4.1 WAN PPPoE
    When configured to PPPoE
    Should have internet connection



*** Keyword ***
Setup Telnet and Open Website and Initial variable
    Init variable                  ${PC_eth}       ${PC_wlan}    ${PC_user_pwd}    ${Router_IP}
    Set Log Level                  INFO
    #Create telnet connection      ${Router_IP}    ~#            root       CassiniRedwwod42562072Portal
    Open website                   ${Router_IP}    Portal        password
    Disable wifi

Close Telnet and Close Website
    Close website
    Enable wifi

### DHCP ###
When configured to DHCP
    Configure WAN with DHCP
    #Verify WAN portal info          DHCP
    #Verify WAN web info             DHCP        UP

### PPPoE ###
When configured to PPPoE
    Configure WAN with PPPoE                    ${PPPoE_usr}     ${PPPoE_pwd}
    #Verify WAN portal info          PPPoE       ${PPPoE_usr}     ${PPPoE_pwd}
    #Verify WAN web info             PPPoE       UP

### Static ###
When configured to Static
    Configure WAN with Static                   ${Static_ip}    ${static_gateway}  ${static_netmask}
    Configure manual DNS                        ${google_dns}   ${public_dns}
    #Verify WAN portal info          Static      ${Static_ip}    ${static_gateway}  ${static_netmask}
    #Verify WAN web info             Static      UP              ${Static_ip}       ${static_netmask}

Should have internet connection
    Check internet connection    192.168.8.1       ${True}
    Check internet connection    8.8.8.8           ${True}
    Check internet connection    www.google.com    ${True}
    Check internet connection    ${url_1}          ${True}


Should not be able to ping to domain name
    Check internet connection    192.168.8.1       ${True}
    Check internet connection    8.8.8.8           ${True}
    Check internet connection    www.google.com    ${False}
    Check internet connection    ${url_2}          ${False}

Configured with Google DNS
    # DHCP will auto get dns, so use static mode to test dns
    Configure WAN with Static       ${Static_ip}     ${static_gateway}   ${static_netmask}
    Configure manual DNS            ${google_dns}    ${public_dns}
    Verify WAN web DNS info         ${google_dns}    ${public_dns}

Configured with fake DNS
    Configure manual DNS            ${fake_dns1}     ${fake_dns2}
    Verify WAN web DNS info         ${fake_dns1}     ${fake_dns2}
    #Configure manual DNS            ${google_dns}   #quick fix, else cant connect to portal gui @ 192.168.8.1

Configured to auto DNS and DHCP
    Configure WAN with DHCP
    Configure auto DNS
