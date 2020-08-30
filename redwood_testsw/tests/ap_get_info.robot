*** Settings ***
Documentation     Testing robot.
...
...               robot framework practice

Library           ../lib/ap/AccessPointLibrary.py
Library           BuiltIn

*** Test Cases ***
Connect
    Create Telnet Connection    192.168.1.1    /#
    Check System Info


CheckVersion
    ${result} =    Check System Info
    Log To Console    ${result}

SSID
    Get ssid
