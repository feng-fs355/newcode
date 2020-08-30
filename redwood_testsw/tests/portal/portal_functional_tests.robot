*** Settings ***
Documentation     Portal Functional Test
...
...               Test portal (fake cloud <--> rw-manager <--> rw-agnet <--> saturn)
...               Only 1 Cloud to 1 RWM supported now.
...
...               Note: It's used to do end-to-end tests for portal.
...                     For example, change SSID:
...                     It will simulate cloud send change SSID command to RWM and RWM proxy it to RWA.
...                     Then, check it from staurn itself, see if SSID been changed.


Library           OperatingSystem
Library           ${CURDIR}/../../lib/redwood/cloud/RWCloudLibrary.py    WITH NAME    Cloud
Library           ${CURDIR}/../../lib/ap/AccessPointLibrary.py           WITH NAME    AP

#Suite Setup    Telnet to Accesspoint    ${AP_HOST}    ${PROMPT}
#...    Start cloud socket    ${PORT}
#...    Wait Until Keyword Succeeds    20 s    1 s    Is manager registerd


*** Variables ***
${PORT}    62300
${AP_HOST}    127.0.0.1
${PROMPT}    /#

*** Test Cases ***

AP Telnet Connection
    Telnet to Accesspoint    ${AP_HOST}    ${PROMPT}

Open Socket
    Start cloud socket    ${PORT}
    Wait Until Keyword Succeeds    20 s    1 s    Is manager registerd


Manager props get
    Execute Method    manager.props.get    none    1    0

Agent props get(To RWA)
    Execute Method    agent.props.get      none    2    0

Subscribe Agent Statechange
    Subscribe notification    wlan.ap.event.statechange    2

Change SSID
    Execute Method    sys.ubus.call    {"path":"uci","parameters":{"values":{"encryption":"psk2","ssid":"test_2g_fkk","key":"12345678"},"match":{"ifname":"ath0"},"config":"wireless"},"procedure":"set"}    2    0
    Sleep    10
    Execute Method    sys.ubus.call    {"path":"uci","parameters":{"config":"wireless"},"procedure":"commit"}    2    0
    Sleep    10
    Execute Method    wlan.ap.statecontrol    {"action":"restart","BSSID":"abc"}    2    0
    Wait For Notification    wlan.ap.event.statechange    state    timeout=20
    ${ap_ssid}=    Get ssid    2G
    Should Contain    ${ap_ssid}    test_5g_fkk

Change SSID (CMD)
    AP.Send cmd    uci set wireless.@wifi-iface[0].ssid=test123
    Execute Method    wlan.ap.statecontrol    {"action":"restart","BSSID":"abc"}    2    0
    Wait For Notification    wlan.ap.event.statechange    state    timeout=20
    ${ap_ssid}=    Get ssid    2G
    Should Contain    ${ap_ssid}    test123


*** Keywords ***
Execute Method
    [Arguments]    ${method}    ${parameter}    ${destEpid}    ${expectedStatus}
    ${status} =    Cloud.Send raw command    ${method}    ${parameter}    255    ${destEpid}
    Log    ${status}
    Status Check    ${status}    ${expectedStatus}


Telnet to Accesspoint
    [Arguments]    ${accesspoint_ip}    ${prompt}
    AP.Create Telnet Connection    ${accesspoint_ip}    ${prompt}