*** Settings ***
Documentation     DFS tests
...

Library           OperatingSystem
Library           redwood/rwm/RWMLibrary.py
Library           ap/AccessPointLibrary.py           WITH NAME    AP

*** Variables ***
${HOST}    127.0.0.1
${PORT}    9000
${PROMPT}    ~#

*** Settings ***
Suite Setup       Init Redwood Manager     ${HOST}    ${PORT}   ${PROMPT}
Test Teardown     close socket
Force Tags        manager

*** Test Cases ***
Check DFS Whitelist Blacklist
    Get DFS whitelist
    
*** Keywords ***
Telnet to Accesspoint
    [Arguments]    ${accesspoint_ip}    ${prompt}
    AP.Create Telnet Connection    ${accesspoint_ip}    ${prompt}   root    12345
    
Init Redwood Manager
    [Arguments]    ${redwood_ip}    ${port}    ${prompt}
    Telnet to Accesspoint    ${redwood_ip}    ${PROMPT}
    AP.Send cmd    /etc/init.d/rwdmanager stop
    Sleep   10
    AP.Send cmd    /etc/init.d/rwdmanager start
    Sleep   10
    Connect to socket     ${redwood_ip}    ${port}
    
Get DFS whitelist
    ${status} =     Send raw command    manager.status   {}    
    Status Check    ${status}    0    
