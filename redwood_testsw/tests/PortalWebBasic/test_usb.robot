** Settings ***
Documentation     Testing portal USB function
...               Testing samba requires a large file > 1G called 'large_file'
...               and a small file < 10M called small_file. These two are not
...               included in AccessPointWeb library

Library           AccessPointWebLibrary.py
Suite Setup       Setup Telnet and Open Website and Initial variable
Suite Teardown    Close Telnet and Close Website

*** Variables ***
${PC_eth}           eth0           # the wire interface you want to use
${PC_wlan}          wlan0          # the wireless interface you want to use
${PC_user_pwd}      idltest        # your computer's pwd
${Router_IP}        192.168.8.1    # the router's IP
${usb1_format}      vfat           # USB-1 format
${usb2_format}      ext3           # USB-2 format
${user_name}        admin
${password}         password

*** Test Cases ***

13.1 Detect
    Should detect USB slot 1
    USB 1 format should be ${usb1_format}
    Should detect USB slot 2
    USB 2 format should be ${usb2_format}

13.2 Eject
    Given USB 1 is mounted
    Try to eject and detect USB slot 1 for 2 times and it's format should be ${usb1_format}

13.3 Samba
    Given USB 1 is mounted
    Enable samba on slot 1
    #Then Samba should be working on slot 1
    #Should be able to upload small_file through Samba
    #Should be able to upload large_file through Samba

    Given USB 2 is mounted
    Enable samba on slot 2
    #Then Samba should be working on slot 2
    #Should be able to upload small_file through Samba
    #Should be able to upload large_file through Samba
    # TODO implement download thru samba

13.4 FTP
    Given USB 1 is mounted
    #Should be able to upload small_file through FTP
    #Should be able to upload large_file through FTP

13.5 DLNA
    Given USB 1 is mounted
    Enable DLNA on slot 1
    Then DLNA should be working

*** Keyword ***
Setup Telnet and Open Website and Initial variable
    Init variable    ${PC_eth}  ${PC_wlan}  ${PC_user_pwd}  ${Router_IP}
    Create telnet connection    ${Router_IP}    ~#    root    CassiniRedwwod42562072Portal
    Open website   ${Router_IP}    Portal    password
    Create large file
    Create small file

Close Telnet and Close Website
    Close website
    Remove file

### USB ###
Should detect USB slot ${usb_id}
    Go to usb page          ${usb_id}
    Check usb is mounted    ${usb_id}

USB ${usb_id} format should be ${usb_format}
    Go to usb page       ${usb_id}
    Check usb format     ${usb_id}   ${usb_format}

Should be able to eject usb on slot ${usb_id}
    Eject usb slot          ${usb_id}
    Check usb is ejected    ${usb_id}

Should be able to detect usb on slot ${usb_id}
    Detect usb slot         ${usb_id}
    Check usb is mounted    ${usb_id}

USB ${usb_id} is mounted
    Check usb is mounted    ${usb_id}
    Set Test Variable       ${usb_id}

Try to eject and detect USB slot ${usb_id} for ${trying_times} times and it's format should be ${usb1_format}
    Test eject feature      ${usb_id}    ${trying_times}    ${usb1_format}

### FTP ###
Should be able to upload ${filename} through FTP
    Toggle usb FTP               ${usb_id}    ${True}
    Upload file FTP              ${usb_id}    ${filename}    ${user_name}    ${password}
    Check upload successful      ${usb_id}    ${filename}
    Delete usb file              ${usb_id}    ${filename}
    Toggle usb FTP               ${usb_id}    ${False}

### SAMBA ###
${toggle} Samba on slot ${usb_id}
    Toggle usb Samba     ${usb_id}  ${toggle}
    Set Test Variable    ${usb_id}

Samba should be working on slot ${usb_id}
    Check Samba works    ${usb_id}    ${user_name}    ${password}

Should be able to upload ${file_name} through Samba
    Upload Samba file            ${usb_id}    ${file_name}    ${user_name}    ${password}
    Check upload successful      ${usb_id}    ${file_name}
    Delete usb file              ${usb_id}    ${file_name}

Transfer speed should be ${transfer_speed} mbps  # Not implemented
    Samba speed test     ${usb_id}  ${transfer_speed}

### DLNA ###
${toggle} DLNA on slot ${usb_id}
    Toggle usb DLNA      ${usb_id}  ${toggle}
    Set Test Variable    ${usb_id}

DLNA should be working
    Check DLNA works     ${usb_id}
