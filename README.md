# flashtnc
Firmware updater for N9600A TNCs. This Python3 script uses the bootloader resident in N9600A firmwares from v2.20 and later to reflash the dsPIC device without an external programmer.
## Software Requirements
* Python3 
* pyserial module
## Installing Python3 and pyserial in Windows
1. Get the Python3 installer for your system here: https://www.python.org/downloads/
2. Install the pyserial module using pip, which is included with Python3. Do this from a command line. Open PowerShell (right click Windows Menu icon, or search for PowerShell).
````
pip3 install pyserial
````
## Installing Python3 and pyserial in Debian Linux
1. Install Python3 and pip through the package manager.  
````
sudo apt-get update
sudo apt-get install python3 python3-pip
````
2. Install pyserial.
````
pip3 instal pyserial
````
## Download flashtnc Repository
* Click the green button above that says **Code**. Select "Download Zip".
* Extract the zip file into a directory you can navigate to easily from a command line.
* The repository includes latest firmware hex file.
## Determine Serial Port Device Identifier
* The N9600A TNCs use USB to serial bridge devices that are enumerated by the operating system. It's easiest to determine the serial port identifier if the TNC is the only USB serial device attached to the system.  
* In Windows, this will be _comN_ where N is a number. May be double-digits. You can find this in the Control Panel->System->Devices->Ports (COM & LPT).  
* In Linux, this will be _/dev/ttyACMN_ or _/dev/ttyUSBN_. N9600A2 TNCs will end in "USBN", while N9600A3 and later TNCs will end in "ACMN". You can find the last USB serial device enumerated in the system by using the following command:  
````
sudo dmesg | grep tty
````
## Critical Precautions to Prevent Bricking your dsPIC!
**Make sure there are no programs running that will access the TNC! Stop all programs that interact with the TNC. If any program accesses the same serial port during firmware update, the dsPIC will certainly brick. Recovery will require an In-Circuit Serial Programmer or replacement of the dsPIC.**
## flashtnc Command Line Usage
````
python3 flashtnc.py [hex file] [serial device]
````
During firmware update, the LEDs on the TNC will all light up and some will flash extremely quickly (it will just look like dimming). You'll see a progressive line count as the hex file is transferred. Recent firmware has around 9500 lines. It will take about 2 minutes or less to update the firmware once the script is started. The TNC will reboot when the update is complete.
## Windows 10 PowerShell Example
````
PS C:\flashtnc-master> python3 flashtnc.py N9600A-v2-5-1.hex com18
Opened port com18
Opened file N9600A-v2-5-1.hex
Starting TNC reflash mode. Don't interrupt this process, the dsPIC will brick.
TNC successfully entered bootloader mode.
TNC bootlader version:  a
TNC ready for hex file, starting transfer. This will take a few minutes.
Start time:  20:15:02
Lines written:  1000
Lines written:  2000
Lines written:  3000
Lines written:  4000
Lines written:  5000
Lines written:  6000
Lines written:  7000
Lines written:  8000
Lines written:  9000
End time:  20:16:37
Line count:  9415
Firmware update successful.
PS C:\flashtnc-master>
````
## Need Help? Head over to the NinoTNC forum on https://groups.io
