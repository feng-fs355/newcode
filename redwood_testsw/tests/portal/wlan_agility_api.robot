*** Settings ***
Documentation     WLAN Agility APIs Testing
...
...               Test all wlan agility APIs defined in:
...               http://172.16.20.242/redwood_api/latest/expandablelist/index.html
...               There are two ways to test the API:
...                   1. Raw command, like the following test cases.
...                   2. Using defined keywords in RWMLibrary, this requires implemetation for each API.

Library           OperatingSystem
Library           ${CURDIR}/../../lib/redwood/rwm/RWMLibrary.py

*** Variables ***
${HOST}    127.0.0.1
${PORT}    9000


*** Test Cases ***
Connect Socket
    Connect to socket    ${HOST}    ${PORT}

#Subscribe Notifications
#    Execute Method    sys.notifications.subscribe    {"name":"wlan.event.scanresult"}
#    Execute Method    sys.notifications.subscribe    {"name":"wlan.ap.event.statechange"}
#    Execute Method    sys.notifications.subscribe    {"name":"wlan.event.spectralreport"}

Manager props get
    Execute Method    manager.props.get    none

Manager agent add
    Execute Method    manager.agent.add    {"agent_id":"abcdef","agent_pub":"abcdef","agent_priv":"abcdef"}


WLAN associate
    Execute Method    wlan.associate    {"admin_id":"abcdef","network_name":"abcdef","reassoc":"false"}

Get WLAN Interface
    Execute Method    wlan.intf.get        none

WLAN SCAN
    Execute Method    wlan.scan.request        {"dwell_time":"10","passive":"false","band":"2.4G"}
    Wait For Notification    wlan.event.scanresult    SSID    timeout=20


WLAN ap statecontrol
    Execute Method    wlan.ap.statecontrol    {'action':'restart','BSSID':'123'}
    Wait For Notification    wlan.ap.event.statechange    state    timeout=20


Agent props get(Fail on purpose)
    Execute Method    agent.props.get      none


Close Socket
    close socket

*** Keywords ***
Execute Method
    [Arguments]    ${method}    ${parameter}
    ${status} =    Send raw command    ${method}    ${parameter}
    Status Check    ${status}    0
