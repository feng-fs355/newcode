*** Settings ***
Documentation     Testing robot.
...
...               robot framework practice

Library           ../lib/ap/AccessPointLibrary.py

*** Test Cases ***
Connect
    Create telnet connection    192.168.1.1    /#

SSID
    Get ssid
