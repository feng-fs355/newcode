# Access Point Web Library

This library automates the test process for Portal's web GUI.

## Installation
This library is written in [Python](https://www.python.org/downloads/). So please have python installed. (python 2.7.12)

This library is built upon [Robot Framework](https://github.com/robotframework/robotframework), an intuitive high level testing framework. Please follow the above link to install Robot Framework.

[Selenium](http://selenium-python.readthedocs.io/), a web driver controller, is also used in this library. Please follow the link to install selenium.

Other packages might be needed as well depending on the which robot test case is run. To be safe, user can install the packages used in all the tests.

These additional packages might be needed(on Ubuntu).

`apt-get install python-dev`

`apt-get install libssl-dev`

`apt-get install iperf`

`apt-get install openssh-server`

A virtual environment is recommended so that these installed python will not interfere and cause conflict to the user's system. Please follow instructions to install [virtualenv]('https://google.com/search?q=python+virtualenv').

Download `required_packages.txt` from this repository and run `pip install -r required_packages.txt` to auto install all packages used.

The OS is base on Linux ubuntu 14.04

## Set up

Each robot test file have a variables section at the top of the the file which have to be manually set to suit each computer and connection setups. Follow the instructions below for more details.

##Execute

### Wireless
1. Go to the AccessPointWebLibrary folder and execute cmd "robot test_wireless.robot"

### WAN
1. Device should connect to Portal via lan
2. Portal should have internet access
3. This test tests DHCP, PPPoE, and static WAN modes. PPPoE test requires a PPPoE connection with username and password. Static connection requires a connectable static internet. Users must enter those credentials manually in test_wan.robot

##### PPPoE
Please setup a valid PPPoE network with correct credentials(username and password) set up in the variables section in test_wan.robot file. `${PPPoE_usr}` should be the username. `${PPPoE_pwd}` should be the password.

##### Static
Please setup a valid internet with a valid static ip. Update the variables `${static_ip}`, `${static_netmask}`, and `${static_gateway}` to the set up connection.

4. Go to the AccessPointWebLibrary folder and execute cmd "robot test_wan.robot"
5. This test also uses a command to disable wifi before the test and reenable wifi after the test. This command works and is tested on Ubuntu. If this does not work, user should manually disable wifi before the test

### LAN
1. Go to the AccessPointWebLibrary folder and execute cmd "robot test_lan.robot"
2. This test also uses a command to disable wifi before the test and reenable wifi after the test. This command works and is tested on Ubuntu. If this does not work, user should manually disable wifi before the test

### Firewall
You have to prepare two computers one as Server and the ohter as Client, and one connects to the Portal's LAN port the other connects to the Portal's WAN port
#### For the WAN port computer:
  Setting the computer IP to static e.g. address: 1.2.3.4, netmask: 255.255.255.0 <br />
  Open ssh server
#### For the Portal:
  Setting the WAN IP to static e.g. address: 1.2.3.5, netmask: 255.255.255.0, gateway: 1.2.3.4

1. Go to the AccessPointWebLibrary folder and execute cmd "robot test_firewall.robot"
2. This test also uses a command to disable wifi before the test and reenable wifi after the test. This command works and is tested on Ubuntu. If this does not work, user should manually disable wifi before the test

### USB
1. Two USB sticks are required for this test, one formatted to NTFS and one to FAT32. The NTFS one should be plugged into slot 1 (The one closer to the LAN ports), FAT32 one should be plugged into slot 2 (The one away from the LAN ports)
2. Two files are also required to be in the same directory as the robot tests. A file of size < 10 MB named small_file and a file of size > 1GB named large_file must be present in the directory and with those corresponding filenames.
3. Go to the AccessPointWebLibrary folder and execute cmd "robot test_usb.robot"

####To create small_file and large_file,
#####For MacOS:
  mkfile -n 1g large_file

  mkfile -n 10m small_file

#####For Linux:
  fallocate -l 1G large_file

  fallocate -l 10M small_file

