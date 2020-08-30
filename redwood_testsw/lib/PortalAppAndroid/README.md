# InstallingAppium

## Requirements:
  * Java openjdk-7-jdk
  * Linuxbrew (for installing node.js)
  * Node.js
  * Appium
  * Android SDK
  * Python

Before downloading tools, creat a folder in home directory to keep the files and for required environment. Following will using a folder named workspace.  
  
## 1. Install JAVA
```
$ sudo apt-get install openjdk-7-jdk
```
  
*If you cannot find package via apt-get, go to: http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html*  
*Download jdk-7u79-linux-x64.tar.gz for x64 or for jdk-7u79-linux-i586.tar.gz x86, and then decompress it.*  
*Copy the folder to /use/local:*
```
	$ sudo cp -r ~/Download/jdk1.7.0_79 /usr/local/.
```
  
Edit the .bashrc file:
```
$ vim .bashrc
  export JAVA_HOME="/usr/lib/jvm/java--openjdk-amd64"
  export PATH="$PATH:$JAVA_HOME"
$ source .bashrc
```

Check whether JAVA is accessible:
```
$ java -version
```

Should get output like:
```
java version "1.7.0_111"
OpenJDK Runtime Environment (IcedTea 2.6.7) (7u111-2.6.7-0ubuntu0.14.04.3)
OpenJDK 64-Bit Server VM (build 24.111-b01, mixed mode)
```

## 2. Install Apache ant
   
Go to workspace:
```
$ wget http://www.eu.apache.org/dist//ant/binaries/apache-ant-1.9.7-bin.tar.gz
$ tar -xvzf apache-ant-1.9.7-bin.tar.gz
$ rm apache-ant-1.9.7-bin.tar.gz
```
Add path:
```
$vim ~/.bashrc
  export ANT_HOME="$HOME/workspace/apache-ant-1.9.6"
  export PATH="$PATH:$ANT_HOME/bin" # Add ant to PATH
$source ~/.bashrc
```
Go to ANT_HOME directory:
```
$ ant -f fetch.xml -Ddest=system
```


## 3.Install Apache maven

In workspace:
```
$ wget http://www.us.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
$ tar -xvzf apache-maven-3.3.9-bin.tar.gz
$ rm apache-maven-3.3.9-bin.tar.gz
```
Add path:
```
$ vim .bashrc
  export MAVEN_HOME="$HOME/workspace/apache-maven-3.3.9"
  export PATH="$PATH:$MAVEN_HOME/bin"
$source .bashrc
```
Chesk that Maven has been properly configured:
```
$ mvn -v
```
Output should looks like:
```
	Apache Maven 3.3.9 (bb52d8502b132ec0a5a3f4c09453c07478323dc5; 2015-11-10T17:41:47+01:00)
	Maven home: /home/6020peaks/workspace/apache-maven-3.3.9
	Java version: 1.7.0_91, vendor: Oracle Corporation
	Java home: /usr/lib/jvm/java-7-openjdk-amd64/jre
	Default locale: en_US, platform encoding: ANSI_X3.4-1968
	OS name: "linux", version: "3.13.0-74-generic", arch: "amd64", family: "unix"
```


## 4. Install rvm

   From a terminal (from root):
```
$ gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
$ curl -sSL https://get.rvm.io | bash -s stable --ruby
$ source ~/.rvm/scripts/rvm
$ gem update --system
$ gem install --no-rdoc --no-ri bundler
$ gem update
$ gem cleanup
```

## 5. Install Linuxbrew

   This is needed for installing Node.js, otherwise Appium will not work correctly if we use sugo apt-get.
   First, install the Linuxbrew dependencies:
```
$ sudo apt-get install build-essential curl git m4 python-setuptools ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev
```
   Then, install Linuxbrew by running this:
```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/linuxbrew/go/install)"
```
   Add brew to your path:	
```
$ vim ~/.bashrc
  export PATH="$PATH:$HOME/.linuxbrew/bin"
$ source ~/.bashrc
$ brew doctor
$ brew update
```

## 6. Install Node.js
```
$ brew install node # It takes a long time to complete.
```
*If you get errors here, try*
```
$ brew update
```
Once done, check that Node.js and npm have been successfully installed by:
```
$ node --version
$ npm --version
```
 
## 7. Install Grunt
```
$ npm install -g grunt grunt-cli
```
 
## 8. Install Appium

   In workspace:
```
$ wget https://github.com/appium/appium/archive/v1.4.16.tar.gz
$ tar -xvzf appium-1.4.16.tar.gz
$ rm appium-1.4.16.tar.gz
$ npm install -g appium
```
   Make sure whether it can run:
```
$ appium
```
   Output should look like:
```
	[Appium] Welcome to Appium v1.6.0 (REV 15ab5de6dc4434c8cc92cf7a78cae5eacff5583c)
	[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```


## 9. Install Android SDK

   In workspace:
```
$ wget http://dl.google.com/android/android-sdk_r24.4.1-linux.tgz
$ tar -xvzf android-sdk_r24.4.1-linux.tgz
$ rm android-sdk_r24.4.1-linux.tgz
$ android-sdk-linux/tools/android update sdk -u -a
```
   Edit the path:
```
$ vim ~/.bashrc
  export ANDROID_HOME="$HOME/workspace/android-sdk-linux"
  export PATH="$PATH:$ANDROID_HOME/tools"
  export PATH="$PATH:$ANDROID_HOME/platform-tools"
$ source ~/.bashrc
```

## 10. Now get your hands dirty!

   Make sure you have Appium Python Client installed:
```
$ sudo pip install Appium-Python-Client
```
   Plug in an Android phone to your host, then run AndroidAppTest.py. For example:
```
$ python AndroidAppTest.py [Device UUID] [appium server port] [appium bootstrap port] [Portal ID] [Customize password] [Iteration]
$ python AndroidAppTest.py RQ3000GM8U 5000 2251 1CC5 yuijhgty 500
```
   You can also start a appium server by:
```
$ appium
```
   Leave this terminal opened and open another terminal to run python test file.


#### Reference:
https://www.smashingmagazine.com/2016/04/from-zero-to-appium-guide-configuring-appium-android/


