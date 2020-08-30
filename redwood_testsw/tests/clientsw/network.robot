*** Settings ***
Documentation 
...    = User Management = 
...    User related functional tests

*** Test Cases ***
On-board a new Portal after signing
    [Documentation]
    ...    = Precondition =
    ...    | = Item = | = Description = |
    ...    | *WiFi* | ON |
    ...    | *Account* | Signed in |
    ...    = Steps = 
    ...    1. Select a Portal to on-board\n\n
    ...    2. Close your phone to the Portal (about 15-20 cm)\n\n
    ...    3. Wait for /Admin Home/ is displayed\n\n
    ...    = Expected Results = 
    ...    1. *Admin Home* is displayed with ONLINE status
    ...    = Miscellaneous = 
    ...    | = Item = | = Description = |
    ...    | *Type* | Manual |
    ...    | *Execution Time* | 120 sec. |
    [Tags]    bat    stress
