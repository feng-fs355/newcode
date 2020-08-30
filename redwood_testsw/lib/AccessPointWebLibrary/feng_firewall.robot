*** Settings ***
Documentation     Testing portal firewall functionality
...
...               robot framework practice with ABC

Library           BuiltIn
Library           ./AccessFirewall_Entry.py
Library           ./AccessPointWebLibrary.py


Suite Setup       Setup SSH and Open Website and Initial variable
Suite Teardown    Close SSH and Close Website


*** Variables ***
${PC_eth}                 eth0                    # the wire interface you want to use
${PC_wlan}                wlan0                   # the wireless interface you want to use
${PC_user_pwd}            idltest                 # your computer's pwd
${Router_IP}              192.168.8.1             # the router's IP
${Remote_PC_IP}           ${RL_PC_IP}             # remote PC's IP 
${Remote_PC_user_name}    ${RL_PC_user_name}      # = RL_PC_user_name
${Remote_PC_user_pwd}     ${RL_PC_user_pwd}       # = RL_PC_user_pwd
${Static_IP}              192.168.8.111           # should be in the same subnet with the router's IP
${RL_PC_IP}               10.10.10.8              # Remote TCP Server
${LL_PC_IP}               192.168.8.3             # For Inbound only / Local TCP Server 
${RC_PC_IP}               10.10.10.8              # Remote TCP Client section ,ps:Local TCP Client no need
${RCS_PC_IP}              10.10.10.2              # Remote TCP Client links target address(Note: Router WAN IP or Remote PC)
${RL_PC_user_name}        pap1                    # the WAN port PC's user name (Remote PC)
${RL_PC_user_pwd}         12345678                # the WAN port PC's password  (Remote PC)
${RL_S_port}              3000                    # Start port 
${RL_E_port}              3020                    # End port (note:suggest test < 20 Ports,because script performance issue)
${PORT_1}                 3000-3050               # Role 1 port range 
${PORT_2}                 3030-3040               # Role 2 port range
${PORT_3}                 4000-4010               # Role 3 port range
${PORT_4}                 5000-5100               # Role 4 port range
${IPv4_IP_address}        192.168.8.108
${tcp_case_1}             True                    # Expected Result for Test Case 1 (True or False) 
${tcp_case_2}             True                    # Expected Result for Test Case 2 (True or False) 
${tcp_case_3}             False                   # Expected Result for Test Case 3 (True or False)  
${tcp_case_4}             True                    # Expected Result for Test Case 4 (True or False)
${tcp_case_5}             False                   # Expected Result for Test Case 5 (True or False)
${tcp_case_6}             False                   # Expected Result for Test Case 6 (True or False)
${tcp_case_7}             True                    # Expected Result for Test Case 7 (True or False)

${R_S_Tag1}               R                       # TCP Server mode, if R=Remote / L=Local
${R_S_Tag2}               L                       # TCP Server mode, if R=Remote / L=Local   
${R_C_Tag1}               L                       # TCP Client mode, if R=Remote / L=Local
${R_C_Tag2}               R                       # TCP Client mode, if R=Remote / L=Local 

*** Test Cases ***

1. Allow Inbound TCP Forwarding with any IP         # using check ${PORT_1}

   [Tags]    Inbound_TCP

   Delete inbound firewall rule
   When inbound WAN source IP is set to any and protocal is TCP
   
   run tcpserver    ${LL_PC_IP}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RL_S_port}    ${RL_E_port}    ${R_S_Tag2}   
 
   Sleep    10   # sleep 10 sec

   ${tcp_result}    check tcpclient    ${RL_PC_IP}    ${RL_S_port}    ${RL_E_port}    ${R_C_Tag2}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RCS_PC_IP}    

   Should Be Equal    ${tcp_case_1}    ${tcp_result}

#3. Allow Inbound TCP/UDP Forwarding with range IP   # using check ${PORT_3}

#   [Tags]    Inbound_TCP
   
#   Delete inbound firewall rule
#   When inbound WAN source IP is set to a range ${Remote_PC_IP} to 10.10.10.254 and protocal is TCP/UDP
   
#   run tcpserver    ${LL_PC_IP}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RL_S_port}    ${RL_E_port}    ${R_S_Tag2}   
 
#   Sleep    10   # sleep 10 sec

#   ${tcp_result}    check tcpclient    ${RL_PC_IP}    ${RL_S_port}    ${RL_E_port}    ${R_C_Tag2}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RCS_PC_IP}    

#   Should Be Equal    ${tcp_case_3}    ${tcp_result}

#4. Comparison the Inbound and DMZ rule priority    # using check ${PORT_1}
 
#    [Tags]    Inbound_TCP

#    Delete inbound firewall rule
#    Set firewall inbound rule    test_4    ${PORT_4}    TCP    ${None}    any
#    Configure dmz           192.168.8.3

#    run tcpserver    ${LL_PC_IP}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RL_S_port}    ${RL_E_port}    ${R_S_Tag2}   
 
#    Sleep    10   # sleep 10 sec

#    ${tcp_result}    check tcpclient    ${RL_PC_IP}    ${RL_S_port}    ${RL_E_port}    ${R_C_Tag2}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RCS_PC_IP}    

#    Should Be Equal    ${tcp_case_1}    ${tcp_result}   

#    Delete inbound firewall rule
#    Delete DMZ   
  

#5. Blocking Outbound TCP with any LAN IP and any WAN IP    # using check ${PORT_1}


#   [Tags]    Outbound_TCP

#   Delete outbound firewall rule
#   When outbound WAN destination IP is set to any and protocal is TCP

#   run tcpserver    ${RL_PC_IP}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RL_S_port}    ${RL_E_port}    ${R_S_Tag1}   

#   Sleep    30   # sleep 30 sec , because remote tcp server need more time

#   ${tcp_result}    check tcpclient    ${RL_PC_IP}    ${RL_S_port}    ${RL_E_port}    ${R_C_Tag1}

#   Should Be Equal    ${tcp_case_5}    ${tcp_result}     


#7. Blocking Outbound TCP/UDP with range LAN IP and range WAN IP    # using check ${PORT_3}

#   [Tags]    Outbound_TCP

#   Delete outbound firewall rule
   
#   When outbound WAN destination IP is set to a range ${RL_PC_IP} to 10.10.10.254 and protocal is TCP/UDP
   
#   run tcpserver    ${RL_PC_IP}    ${RL_PC_user_name}    ${RL_PC_user_pwd}    ${RL_S_port}    ${RL_E_port}    ${R_S_Tag1}

#   Sleep    30   # sleep 30 sec , because remote TCP Server needs more time   
 
#   ${tcp_result}    check tcpclient    ${RL_PC_IP}    ${RL_S_port}    ${RL_E_port}    ${R_C_Tag1}

#   Should Be Equal    ${tcp_case_7}    ${tcp_result}         
    
 

*** Keyword ***
Setup SSH and Open Website and Initial variable
    Init variable    ${PC_eth}  ${PC_wlan}  ${PC_user_pwd}  ${Router_IP}  ${RL_PC_IP}  ${RL_PC_user_name}  ${RL_PC_user_pwd}
    Create ssh connection    ${Router_IP}    ~#    root    CassiniRedwwod42562072Portal
    Disable wifi
    Open website   ${Router_IP}    Portal    password
    Go to page   /firewall/inbound
    Delete DMZ
    #SSH connect

Close SSH and Close Website
    Close website
    #Clear all ssh connection
    Enable wifi
### Allow inbound
Inbound WAN source IP is set to any and protocal is ${protocal}
    Set firewall inbound rule    test_1    ${PORT_1}    ${protocal}    ${None}    any

Inbound WAN source IP is set to single ip ${ip_addr} and protocal is ${protocal}
    Set firewall inbound rule    test_2    ${PORT_2}    ${protocal}    ${None}    single    ${ip_addr}

Inbound WAN source IP is set to a range ${ip_start} to ${ip_end} and protocal is ${protocal}
    Set firewall inbound rule    test_3    ${PORT_3}    ${protocal}    ${None}    range    ${ip_start}    ${ip_end}

All inbound connections should be able to connect to LAN with ${protocal}
    Test inbound connection from all    ${PORT_1}   ${protocal}

Only the ip address should be able to connect to LAN with ${protocal}
    Test inbound connection from single ip    ${PORT_2}    ${protocal}

Only IP addresses in that range should be able to connect to LAN with ${protocal}
    Test inbound connection from range ip   ${PORT_3}    ${protocal}

The inbound LAN destination should receive the message with ${protocal}
    Inbound receive mesg    ${PORT_1}    ${protocal}    ${True}

The all packets through ${protocal} should be received
    The all packets should be received    ${protocal}

### Block outbound
Outbound WAN destination IP is set to any and protocal is ${protocal}
    Set firewall outbound rule    test_1   ${PORT_1}   ${protocal}   any   any

Outbound WAN destination IP is set to single ${wan_ip} and protocal is ${protocal}
    Set firewall outbound rule    test_2   ${PORT_2}   ${protocal}   single   single    ${None}    ${None}    ${wan_ip}

Outbound WAN destination IP is set to a range ${wan_start_ip} to ${wan_end_ip} and protocal is ${protocal}
    Set firewall outbound rule    test_3   ${PORT_3}   ${protocal}   range   range    ${None}    ${None}    ${wan_start_ip}    ${wan_end_ip}

All outbound connections should not be able to connect to LAN with ${protocal}
    Test outbound connection to all    ${PORT_1}    ${protocal}

Only the ip address should be not able to connect to WAN with ${protocal}
    Test outbound connection to single ip    ${PORT_2}    ${protocal}

Only IP addresses in that range should be able to connect to WAN with ${protocal}
    Test outbound connection to range ip   ${PORT_3}    ${protocal}

##### MAC filtering
Change 2G SSID
    [Arguments]    ${ssid}
    Change ssid                  2.4    ${ssid}
    Change encryption mode       2.4    None
    Apply
    Wifi connection              ${ssid}
    Delete wifi record           ${ssid}
