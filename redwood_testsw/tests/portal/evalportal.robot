*** Settings ***
Documentation
...    = Test cases for portal eval  =
...    These cases will cover\n\n
...    1. Basic information verification\n\n
...    2. Sysupgrade via cloud and igncli.exe\n\n
...
...    = Setup =
...    | = Item = | = Description = |
...    | *Workstation* | windows7 or later |
...    | *eval eval_portal* | igncli.exe package |
...    | *Redwood HW* | ethernet connected  |

*** Test Cases ***
Licence Key and Passkey Verification
    [Documentation]
    ...    = Precondition =
    ...    1. Workstation and Redwood device in the same subnet.\n\n
    ...    2. DHCP server is preferred.\n\n
    ...    3. Workstation running igncli.exe\n\n
    ...    4. Workstation with SSH client tool
    ...
    ...    = Steps =
    ...    1. Check igncli.exe can get workstation's net interface.(same subnet to redwood)
    ...    | CMD | listIF |
    ...    2. Search for redwood. IP address will show up in the results.
    ...    | CMD | search |
    ...    3. Connect to target redwood via IP.
    ...    | CMD | connect --t <IP> |
    ...    4. Connect to target and check target licence key.
    ...    | CMD | manager_props_get |
    ...    5. SSH to target and check the ``/etc/redwood/passkey.bin``.
    ...    | CMD | cat /etc/redwood/passkey.bin |
    ...
    ...    = Expected Results =
    ...    1. Step #4, licence key should be match to the rwmac in IDL internal licence key list.\n\n
    ...    2. Step #5, passkey should be match to the licence key.\n\n
    ...    = Miscellaneous =
    ...    | = Item = | = Description = |
    ...    | *Type* | Manual |
    ...    | *Execution Time* | 120 sec. |
    [Tags]    eval

Sysupgrade Via igncli.exe
    [Documentation]
    ...    = Precondition =
    ...    1. Workstation and Redwood device in the same subnet.\n\n
    ...    2. DHCP server is preferred.\n\n
    ...    3. Workstation running igncli.exe\n\n
    ...    4. Put image bin and md5sum files under ``rwshare/upgrade``, it is relative to where the igncli.exe was installed (or invoked)
    ...
    ...    = Steps =
    ...    1. Check igncli.exe can get workstation's net interface.(same subnet to redwood)
    ...    | CMD | listIF |
    ...    2. Search for redwood. IP address will show up in the results.
    ...    | CMD | search |
    ...    3. Connect to target redwood via IP.
    ...    | CMD | connect --t <IP> |
    ...    4. Execute sysupgrade to update the targe.
    ...    | CMD | update_local --file <filename> |
    ...    5. Search for redwood until it's back to the target list.
    ...    | CMD | search |
    ...    6. Connect to target and check target version.
    ...    | CMD | connect --t <IP> |
    ...    | CMD | manager_props_get |
    ...
    ...    = Expected Results =
    ...    1. No errors during all steps.\n\n
    ...    2. The target redwood shoud show up in search list in step #5.\n\n
    ...    3. Step #6, the returned version should be same as the bin version provided in step #4.\n\n
    ...    4. Redwood device should work normally after upgrade. (no crash)\n\n
    ...    = Miscellaneous =
    ...    | = Item = | = Description = |
    ...    | *Type* | Manual |
    ...    | *Execution Time* | 120 sec. |
    [Tags]    eval

Wlan Scan Request Via igncli.exe
    [Documentation]
    ...    = Precondition =
    ...    1. Workstation and Redwood device in the same subnet.\n\n
    ...    2. DHCP server is preferred.\n\n
    ...    3. Workstation running igncli.exe\n\n

    ...    = Steps =
    ...    1. Check igncli.exe can get workstation's net interface.(same subnet to redwood)
    ...    | CMD | listIF |
    ...    2. Search for redwood. IP address will show up in the results.
    ...    | CMD | search |
    ...    3. Connect to target redwood via IP.
    ...    | CMD | connect --t <IP> |
    ...    4. Ask system for notifications about the event you are interested.
    ...    | CMD | sys_notifications_subcribe --name <NAME> |
    ...    5. Wlan scan request.
    ...    | CMD | wlan_scan_request --dwell_time <DWELL_TIME> --band <BAND> |

    ...    = Expected Results =
    ...    1. No errors during all steps.\n\n


Sysupgrade Via Cloud (sock.ignitiondl.com)
    [Documentation]
    ...    = Precondition =
    ...    1. Workstation and Redwood device in the same subnet.\n\n
    ...    2. DHCP server is preferred.\n\n
    ...    3. Workstation running igncli.exe\n\n
    ...    4. Cloud server should be up and running.
    ...
    ...    = Steps =
    ...    1. Check igncli.exe can get workstation's net interface.(same subnet to redwood)
    ...    | CMD | listIF |
    ...    2. Search for redwood. IP address will show up in the results.
    ...    | CMD | search |
    ...    3. Connect to target redwood via IP.
    ...    | CMD | connect --t <IP> |
    ...    4. Check target version and keep it as old version.
    ...    | CMD | manager_props_get |
    ...    5. Make sure target is connected to cloud.\n\n
    ...    6. Wait until cloud trigger sysupgrade.\n\n
    ...    7. After undate complete, connect to target and check version. Keep it as new_version.
    ...    | CMD | search |
    ...    | CMD | connect --t <IP> |
    ...    | CMD | manager_props_get |
    ...
    ...    = Expected Results =
    ...    1. No errors during all steps.\n\n
    ...    2. Version old_version should be different to new_version.\n\n
    ...    3. Redwood device should work normally after upgrade. (no crash)\n\n
    ...    = Miscellaneous =
    ...    | = Item = | = Description = |
    ...    | *Type* | Manual |
    ...    | *Execution Time* | 600 sec. |
    [Tags]    eval

