*** Settings ***
Documentation     Portal Unit Test with Fake Cloud
...
...               Test redwood APIs on portal (fake cloud <--> manager <--> agnet)
...               Only 1 Cloud to 1 RWM supported now.
...
...               Note: It's used to unit test the redwood application.
...                     It  won't check the actuall setting/behavior on target system.
...                     For example, change SSID on rw-agnet will only perform the APIs and
...                     check the APIs responses. It won't check the network settings on rw-agent(saturn)
...
...               There are two ways to test the API:
...                   1. Raw command, like the following test cases.
...                   2. Using defined keywords in RWMLibrary, this requires implemetation for each API.

Library           OperatingSystem
Library           ${CURDIR}/../../lib/redwood/cloud/RWCloudLibrary.py

*** Variables ***
${PORT}    62300


*** Test Cases ***
Open Socket
    Start cloud socket    ${PORT}
    Wait Until Keyword Succeeds    20 s    1 s    Is manager registerd

### Manager APIs ###

Manager props get
    Execute Method    manager.props.get    none    1    0

Manager agent add
    Execute Method    manager.agent.add    {"agent_id": "abcdef", "agent_pub": "abcdef", "agent_priv": "abcdef"}    1    0

### Manager APIs (END)###

WLAN intf get
    Execute Method    wlan.intf.get        none    1    0

#WLAN ap statecontrol
#    Execute Method    wlan.ap.statecontrol    {'action':'restart','BSSID':'123'}    1    0

WLAN associate
    Execute Method    wlan.associate    {"admin_id":"abcdef","network_name":"abcdef","reassoc":"false"}    1    0

Agent props get(To RWM)
    Execute Method    agent.props.get      none    1    0

Agent props get(To RWA)
    Execute Method    agent.props.get      none    2    0


#Close Socket
#    close socket

*** Keywords ***
Execute Method
    [Arguments]    ${method}    ${parameter}    ${destEpid}    ${expectedStatus}
    ${status} =    Send raw command    ${method}    ${parameter}    255    ${destEpid}
    Log    ${status}
    Status Check    ${status}    ${expectedStatus}