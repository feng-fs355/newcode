*** Settings ***
Documentation     Testing robot.
...
...               robot framework practice with ABC

Library           BuiltIn
Library           ../../src/ap/portal/base/APWL_PortalWebBase.py    WITH NAME    APWEB

Suite Setup       Suite Setup Actions
Suite Teardown    Suite Teardown Actions
Test Setup        Test Setup Actions
Test Teardown     Test Teardown Actions


*** Variables ***
${SUITE_LOG_ID}
${TEST_LOG_ID}
&{DUT_LAN_Settings}    connection=Up    ip=192.168.8.1    mask=255.255.255.0    mac=00:78:CD:00:12:68    dns=10.10.10.254 
&{DUT_WAN_Settings}    connection=Up    ip=10.10.10.2    mask=255.255.255.0    mac=00:78:CD:00:12:69     dns=10.10.10.254
&{DUT_2G_Settings}     ssid=Portal_2Gzzz    channel=1 (2.412 GHz)    mode=802.11ng    mac=00:78:CD:00:12:6A    encryption=psk2
&{DUT_5G_Settings}     ssid=1c11 main v1    channel=100 (5.500 GHz)    mode=802.11ac    mac=00:78:CD:00:12:6B    encryption=psk2
&{DUT_Info}            hw_ver=Portal_V1.0    sw_ver=Portal-1.4.138_prod-1.2.116    time_zone=UTC
&{Devices_1}           ip=    mac=38:d5:47:33:fe:34    name=idltest    alias=
&{Devices_2}           ip=    mac=04:69:f8:5f:c3:fc    name=MBPs-iPad      alias=
&{Devices_3}           ip=    mac=58:48:22:f7:a8:03    name=android-b5a941cbc80bc6c6    alias=
@{DUT_Attached_Devices_List}    &{Devices_1}    &{Devices_2}    &{Devices_3}
@{DUT_Attached_Devices_List}    &{Devices_1} 
@{DUT_2.4G_Main_Attached_Devices_List}    &{Devices_1}
@{DUT_5G_Main_Attached_Devices_List}    &{Devices_2}
@{DUT_2.4G_Guest_Attached_Devices_List}
@{DUT_5G_Guest_Attached_Devices_List}

*** Test Cases ***

Check LAN Status
    ${expected} =    APWEB.set_expected_net_settings    ${DUT_LAN_Settings.connection}    ${DUT_LAN_Settings.ip}    ${DUT_LAN_Settings.mask}    ${DUT_LAN_Settings.mac}    ${DUT_LAN_Settings.dns}
    ${result} =    APWEB.get_net_settings    LAN
    Should Be Equal    ${expected}    ${result}    LAN setting not expected

Check WAN Status
    ${expected} =    APWEB.set_expected_net_settings    ${DUT_WAN_Settings.connection}    ${DUT_WAN_Settings.ip}    ${DUT_WAN_Settings.mask}    ${DUT_WAN_Settings.mac}    ${DUT_WAN_Settings.dns}
    ${result} =    APWEB.get_net_settings    WAN
    Should Be Equal    ${expected}    ${result}    WAN setting not expected

Check 2.4G Status
    ${expected} =    APWEB.set_expected_wlan_settings    ${DUT_2G_Settings.ssid}    ${DUT_2G_Settings.channel}    ${DUT_2G_Settings.mode}    ${DUT_2G_Settings.mac}    ${DUT_2G_Settings.encryption}
    ${result} =    APWEB.get_wlan_settings    2.4G    main
    Should Be Equal    ${expected}    ${result}    2.4G setting not expected

#Check 5G Status
#    ${expected} =    APWEB.set_expected_wlan_settings    ${DUT_5G_Settings.ssid}    ${DUT_5G_Settings.channel}    ${DUT_5G_Settings.mode}    ${DUT_5G_Settings.mac}    ${DUT_5G_Settings.encryption}
#    ${result} =    APWEB.get_wlan_settings    5G    main
#    Should Be Equal    ${expected}    ${result}    5G setting not expected

Check Router Information
    ${expected} =    APWEB.set_expected_version_info    ${DUT_Info.hw_ver}    ${DUT_Info.sw_ver}    ${DUT_Info.time_zone}
    ${result} =    APWEB.get_version_info
    Should Be Equal    ${expected}    ${result}    Version info not expected

Check Attached Devices - Wired
    ${expected} =    APWEB.set_expected_attached_devices_list    ${DUT_Attached_Devices_List}
    ${result} =    APWEB.get_attached_devices    wired
    Should Be Equal    ${expected}    ${result}    Attached devices not expected

Check Attached Devices - 2.4G
    ${expected} =    APWEB.set_expected_attached_devices_list    ${DUT_2.4G_Main_Attached_Devices_List}
    ${result} =    APWEB.get_attached_devices    2.4g    main
    Should Be Equal    ${expected}    ${result}    Attached devices not expected

#Check Attached Devices - 5G
#    ${expected} =    APWEB.set_expected_attached_devices_list    ${DUT_5G_Main_Attached_Devices_List}
#    ${result} =    APWEB.get_attached_devices    5g    main
#    Should Be Equal    ${expected}    ${result}    Attached devices not expected

Check Attached Devices - 2.4G Guest
    ${expected} =    APWEB.set_expected_attached_devices_list    ${DUT_2.4G_Guest_Attached_Devices_List}
    ${result} =    APWEB.get_attached_devices    2.4g    guest
    Should Be Equal    ${expected}    ${result}    Attached devices not expected

#Check Attached Devices - 5G Guest
#    ${expected} =    APWEB.set_expected_attached_devices_list    ${DUT_5G_Guest_Attached_Devices_List}
#    ${result} =    APWEB.get_attached_devices    5g    guest
#    Should Be Equal    ${expected}    ${result}    Attached devices not expected

*** Keywords ***
Suite Setup Actions
    [Documentation]    Opens browser and start log captures
    Log To Console    ${OUTPUTDIR}
    APWEB.set_web_driver    firefox
    APWEB.login    192.168.8.1    None    password
    ${log_id} =    APWEB.start_log_capture    path=${OUTPUTDIR}    file_name=${SUITE NAME}_prtsc
    Set Suite Variable    ${SUITE_LOG_ID}    ${log_id}

Suite Teardown Actions
    [Documentation]    Close browser and stop log captures
    APWEB.logout
    APWEB.stop_log_capture    ${SUITE_LOG_ID}
    APWEB.close_browser

Test Setup Actions
    [Documentation]    Start log captures
    ${log_id} =    APWEB.start_log_capture    path=${OUTPUTDIR}    file_name=${TEST NAME}_prtsc
    Set Test Variable    ${TEST_LOG_ID}    ${log_id}

Test Teardown Actions
    [Documentation]    Stop log captures
    APWEB.stop_log_capture    ${TEST_LOG_ID}