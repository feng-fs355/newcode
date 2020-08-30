*** Settings ***
Documentation 
...    = User Management = 
...    User related functional tests

*** Test Cases ***
Sign up with email via Internet
    [Documentation]
    ...    = Precondition =
    ...    | = Item = | = Description = |
    ...    | *WiFi* | ON |
    ...    | *Account* | Not exist |
    ...    = Steps = 
    ...    1. Launch the app to see landing page.\n\n
    ...    2. Click _Sign Up_\n\n
    ...    3. Input valid information for signing up\n\n
    ...    = Expected Results = 
    ...    1. Signed in toolbar is shown
    ...    = Miscellaneous = 
    ...    | = Item = | = Description = |
    ...    | *Type* | Manual |
    ...    | *Execution Time* | 120 sec. |
    [Tags]    bat
