** Settings ***
Documentation     Testing portal LAN connection
...
...               robot framework practice

Library           AccessPointWebLibrary.py
Suite Setup       Setup SSH and Open Website and Initial variable
Suite Teardown    Close SSH and Close Website

*** Variables ***
${PC_eth}           eth0             # the wire interface you want to use
${PC_wlan}          wlan0            # the wireless interface you want to use
${PC_user_pwd}      idltest             # your computer's pwd
${Router_IP}        192.168.8.1      # the router's IP
${Static_IP}        192.168.8.111    # should be in the same subnet with the router's IP

*** Test Cases ***

#### 2.1: LAN IP address and subnet Mask ####

2.1: LAN IP address and subnet Mask

    Check LAN default    ${Router_IP}    255.255.255.0
    Try ClassD and E     224.1.1.1
    Try ClassD and E     240.1.1.1
    Configure LAN        10.1.1.1       255.0.0.0
    Configure LAN        172.16.1.1     255.255.0.0
    Configure LAN        ${Router_IP}    255.255.255.0

#### 2.2: DHCP Server ####
# 20170124 Remark,this case can't execute

#2.2: Test DHCP Server
#    Disable DHCP server
#    Enable DHCP server


#### 2.5: Bridge Mode ####

2.5.2: Test Bridge mode with static IP config
    Bridge mode with static IP        ${Router_IP}     255.255.255.0

*** Keyword ***
Setup SSH and Open Website and Initial variable
    Init variable    ${PC_eth}  ${PC_wlan}  ${PC_user_pwd}  ${Router_IP}
    Create ssh connection    ${Router_IP}    ~#    root    CassiniRedwwod42562072Portal
    Disable wifi
    Open website   ${Router_IP}    Portal    password

Close SSH and Close Website
    Close website
    Enable wifi

Configure LAN
    [Arguments]    ${ip_address}    ${subnet_mask}

    Configure LAN with static    ${ip_address}    ${subnet_mask}
    Close website
    Renew PC IP address
    Check route IP               ${ip_address}    ${subnet_mask}
    Check connect web            ${ip_address}    Portal    password

Disable DHCP server

    Toggle DHCP server         ${False}
    Apply
    Close website
    Renew PC IP address
    Check PC IP address       ${False}

Enable DHCP server

    Set eth manually          ${Static_IP}    255.255.255.0
    Check connect web         ${Router_IP}    Portal    password
    Toggle DHCP server        ${True}
    Apply
    Close website
    Renew PC IP address
    Check PC IP address       ${True}
    Check connect web         ${Router_IP}    Portal    password

Bridge mode with static IP
    [Arguments]    ${ip_address}    ${subnet_mask}

    Toggle bridge mode           ${True}
    Configure LAN with static    ${ip_address}    ${subnet_mask}
    Close website
    Renew PC IP address
    Set eth manually             ${Static_IP}    255.255.255.0
    Check connect web            ${Router_IP}    Portal    password
    Toggle bridge mode           ${False}
    #Toggle DHCP server           ${True}
    Apply
    Close website
    Renew PC IP address
    Open Website                 ${Router_IP}    Portal    password
    Check connect wan
