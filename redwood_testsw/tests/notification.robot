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
Library           ${CURDIR}/../lib/redwood/cloud/RWCloudLibrary.py

*** Variables ***
${PORT}    62300


*** Test Cases ***
Open Socket
    Start cloud socket    ${PORT}
    Wait Until Keyword Succeeds    20 s    1 s    Is manager registerd

Manager props get
    Execute Method    manager.props.get    none    1    0


AP SCAN (SSID)
    Execute Method    wlan.scan.request    {"dwell_time":"10", "passive":"false", "band":"2.4G"}    1    0
    Wait For Notification    wlan.event.scanresult    SSID    timeout=20

AP SCAN (BSSID)
    Execute Method    wlan.scan.request    {"dwell_time":"10", "passive":"false", "band":"2.4G"}    1    0
    Wait For Notification    wlan.event.scanresult    BSSID    timeout=20

AP SCAN (entries)
    Execute Method    wlan.scan.request    {"dwell_time":"10", "passive":"false", "band":"2.4G"}    1    0
    Wait For Notification    wlan.event.scanresult    entries    timeout=20

Force DFS
    Execute Method    wlan.ap.test.forcedfs    {"channel":"52", "clear":"false"}    1    0
    Wait For Notification    wlan.ap.event.dfslist    whitelist    timeout=20


*** Keywords ***
Execute Method
    [Arguments]    ${method}    ${parameter}    ${destEpid}    ${expectedStatus}
    ${status} =    Send raw command    ${method}    ${parameter}    255    ${destEpid}
    Log    ${status}
    Status Check    ${status}    ${expectedStatus}
