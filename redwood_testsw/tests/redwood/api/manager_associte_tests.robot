*** Settings ***
Documentation     API test for manager.associate
...

Library           OperatingSystem
Library           redwood/rwm/RWMLibrary.py

*** Variables ***
${HOST}    127.0.0.1
${PORT}    9000

*** Settings ***
Suite Setup       Connect to socket     ${HOST}    ${PORT}
Test Teardown     close socket
Force Tags        manager

*** Test Cases ***
Manager associate
    Execute Associate Method   test     Test Network    0
    
Manager deassocite
    Execute Associate Method   ${EMPTY}     ${EMPTY}    1
    
Invalid parameters
    [Template]    Associate with invalid parameters
    ${EMPTY}        ${EMPTY}    0
    test            ${EMPTY}    0   
    ${EMPTY}        2345        0
    
*** Keywords ***
Execute Associate Method
    [Arguments]     ${admin_id}    ${network_name}    ${reassoc}
    ${status} =     Send raw command    manager.associate   {"admin_id":"${admin_id}","network_name":"${network_name}","reassoc":${reassoc}}    
    Status Check    ${status}    0
        
Associate with invalid parameters
    [Arguments]    ${admin_id}    ${network_name}   ${reassoc}
    ${status} =    Send raw command    manager.associate   {"admin_id":"${admin_id}","network_name":"${network_name}","reassoc":${reassoc}}    
    Status Check   ${status}    -1
