*** Settings ***
Documentation     Testing wireless configurations, which includes changing ssid, network password, network security mode in both 2G and 5G bands.

# remark and bypass 5G test ,test_pc issue,as below:
#device info: -> ethtool -i wlan0
#driver: rtl8723be
#version: 4.4.0-59-generic
#firmware-version: N/A
#expansion-rom-version: 
#bus-info: 0000:01:00.0
#supports-statistics: yes
#supports-test: no
#supports-eeprom-access: no
#supports-register-dump: no
#supports-priv-flags: no

#frequency list: -> iwlist wlan0 frequency
#wlan0     13 channels in total; available frequencies :
#          Channel 01 : 2.412 GHz
#          Channel 02 : 2.417 GHz
#          Channel 03 : 2.422 GHz
#          Channel 04 : 2.427 GHz
#          Channel 05 : 2.432 GHz
#          Channel 06 : 2.437 GHz
#          Channel 07 : 2.442 GHz
#          Channel 08 : 2.447 GHz
#          Channel 09 : 2.452 GHz
#          Channel 10 : 2.457 GHz
#          Channel 11 : 2.462 GHz
#          Channel 12 : 2.467 GHz
#          Channel 13 : 2.472 GHz

...
...               robot framework practice

Library           AccessPointWebLibrary.py
Suite Setup       Setup Telnet and Open Website and Initial variable
Suite Teardown    Close Telnet and Close Website

*** Variables ***
${PC_eth}           eth0           # the wire interface you want to use
${PC_wlan}          wlan0          # the wireless interface you want to use
${PC_user_pwd}      idltest            # your computer's pwd
${Router_IP}        192.168.8.1    # the router's IP

*** Test Cases ***

2G-SSID
    #Check 2G Default
    Change 2G SSID    ~!@#$%^&*()_+{}|:"<>?`-=[]z;,./
    Change 2G SSID    1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,
    Change 2G SSID    9ol.0p/-[=]`~!@#$%^&*()_+|ABCDE

2G-Security Modes-None
    Change 2G Security Mode    Portal_2Gzzz    None

2G-Security Modes-WPA2-PSK (AES)
    Change 2G Security Mode    1234567890123<>?=+&% The quick b    WPA2    1234567890123<>?=+&% The quick b
    Change 2G Security Mode    1234567890abcdef1234567890abcdef    WPA2    1234567890abcdef1234567890abcdef
    Change 2G Security Mode    12345678901234567890123456789012    WPA2    12345678901234567890123456789012

2G-Security Modes-WPA-PSK(TKIP)+WPA2-PSK(AES) mixed mode
    Change 2G Security Mode    1234567890123<>?=+&% The quick b    WPA/WPA2    1234567890123<>?=+&% The quick b
    Change 2G Security Mode    1234567890abcdef1234567890abcdef    WPA/WPA2    1234567890abcdef1234567890abcdef
    Change 2G Security Mode    12345678901234567890123456789012    WPA/WPA2    12345678901234567890123456789012

2G-broadcast
    Change 2G broadcast        Portal_2Gzzz




#5G-SSID
    ##Check 5G Default
#    Change 5G SSID    ~!@#$%^&*()_+{}|:"<>?`-=[]z;,./
#    Change 5G SSID    1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,
#    Change 5G SSID    9ol.0p/-[=]`~!@#$%^&*()_+|ABCDE

#5G-Security Modes-None
#    Change 5G Security Mode    Portal_5Gzzz    None

#5G-Security Modes-WPA2-PSK (AES)
#    Change 5G Security Mode    1234567890123<>?=+&% The quick b    WPA2    1234567890123<>?=+&% The quick b
#    Change 5G Security Mode    1234567890abcdef1234567890abcdef    WPA2    1234567890abcdef1234567890abcdef
#    Change 5G Security Mode    12345678901234567890123456789012    WPA2    12345678901234567890123456789012

#5G-Security Modes-WPA-PSK(TKIP)+WPA2-PSK(AES) mixed mode
#    Change 5G Security Mode    1234567890123<>?=+&% The quick b    WPA/WPA2    1234567890123<>?=+&% The quick b
#    Change 5G Security Mode    1234567890abcdef1234567890abcdef    WPA/WPA2    1234567890abcdef1234567890abcdef
#    Change 5G Security Mode    12345678901234567890123456789012    WPA/WPA2    12345678901234567890123456789012

#5G-broadcast
#    Change 5G broadcast        12345678901234567890123456789012

*** Keyword ***
Setup Telnet and Open Website and Initial variable
    Init variable    ${PC_eth}  ${PC_wlan}  ${PC_user_pwd}  ${Router_IP}
    Enable Wifi
    #Create telnet connection    ${Router_IP}    ~#    root    CassiniRedwwod42562072Portal
    Open website   ${Router_IP}    Portal    password

Close Telnet and Close Website
    Close website

#####
Check 2G Default
    Refresh page
    Check web default ssid             2.4
    Check portal wireless default      2.4    WPA2

Change 2G SSID
    [Arguments]    ${ssid}
    Refresh page
    Change ssid                  2.4    ${ssid}
    Change encryption mode       2.4    None
    Change encryption mode       2.4    none
    Apply
    Check web status wireless    2.4    ${ssid}
    #Check portal wireless        2.4    ${ssid}
    Check wifi connection        2.4    ${ssid}
    Check web status attached device    2.4
    Delete wifi record           ${ssid}

Change 2G Security Mode
    [Arguments]    ${ssid}    ${security}=${None}    ${password}=${None}
    Refresh page
    Change ssid                  2.4    ${ssid}
    Change encryption mode       2.4    ${security}
    Change network password      2.4    ${password}
    Apply
    Check web status wireless    2.4    ${ssid}    ${security}
    #Check portal wireless        2.4    ${ssid}    ${security}    ${password}
    Check wifi connection        2.4    ${ssid}    ${security}    ${password}
    Check web status attached device    2.4
    Delete wifi record           ${ssid}

Change 2G broadcast
    [Arguments]    ${ssid}
    Refresh page
    Change ssid                  2.4        ${ssid}
    Change encryption mode       2.4        None
    Check broadcast              2.4        ${ssid}

Check 5G Default
    Refresh page
    Check web default ssid             5
    Check portal wireless default      5    WPA2

Change 5G SSID
    [Arguments]    ${ssid}
    Refresh page
    Change ssid                  5    ${ssid}
    Change encryption mode       5    None
    Apply
    Check web status wireless    5    ${ssid}
    Check portal wireless        5    ${ssid}
    Check wifi connection        5    ${ssid}    None
    Check web status attached device    5
    Delete wifi record           ${ssid}


Change 5G Security Mode
    [Arguments]    ${ssid}    ${security}=${None}    ${password}=${None}
    Refresh page
    Change ssid                  5    ${ssid}
    Change encryption mode       5    ${security}
    Change network password      5    ${password}
    Apply
    Check web status wireless    5    ${ssid}    ${security}
    Check portal wireless        5    ${ssid}    ${security}    ${password}
    Check wifi connection        5    ${ssid}    ${security}    ${password}
    Check web status attached device    5
    Delete wifi record           ${ssid}

Change 5G broadcast
    [Arguments]    ${ssid}
    Refresh page
    Change ssid               5          ${ssid}
    Change encryption mode    5          None
    Check broadcast           5        ${ssid}
