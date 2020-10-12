# flashtnc
Firmware updater for N9600A NinoTNCs. This Python3 script uses the bootloader resident in N9600A firmwares from v2.20 and later to reflash the dsPIC device without an external programmer. The instructions below include separate sections for 64-Bit Windows, 32-Bit Windows, and Debian Linux. Make sure you read the __Notes For All Platforms__ section at the bottom of this document.
## Software Requirements
* Python3 
* pyserial module
## Generic Recipe
1. Install Python3 on your system
2. Install the pyserial software module
3. Download the flashtnc repository
4. Connect your NinoTNC to your system, determine its serial port identifier
5. Run the flashtnc program to update firmware on your TNC
## Firmware Versions
* The change log for firmware versions is contained in release-notes.txt.
* I recommend using the most recent firmware (highest version number, currently 2.75).
* Firmweare 2.70 and later allows deletion of RN2 by enabling internal pulldowns on some input pins. If your TNC doesn't have RN2, don't downgrade your firmware below 2.7x! The TNC will freeze if you do, and you'll need an ICSP reflash or replacement dsPIC with compatible firmware.
# Instructions for 64-Bit Windows
## Installing Python3 and pyserial (64-Bit Windows)
1. Get the Python3 installer for your system here: https://www.python.org/downloads/
2. During the Python3 install process, make sure "add Python to the PATH" is selected.
3. Install the pyserial module using pip, which is included with Python3. Do this from a command line. I use PowerShell (right click Windows Menu icon, or search for PowerShell), but the normal command line works too.
````
PS C:\Users\ninoc> pip3 install pyserial
````
## Download flashtnc Repository (64-Bit Windows)
* Click the green button above that says **Code**. Select "Download Zip".
* Extract the zip file into a directory you can navigate to easily from a command line.
* The repository includes latest firmware hex file.
## Determine Serial Port Device Identifier (64-Bit Windows)
* The N9600A TNCs use USB to serial bridge devices that are enumerated by the operating system. It's easiest to determine the serial port identifier if the TNC is the only USB serial device attached to the system.  
* In Windows, this will be _comN_ where N is a number. May be double-digits. You can find this in the Control Panel->System->Devices->Ports (COM & LPT). The serial port device identifier might change if you swap out NinoTNCs, reboot the computer, or use a different USB port. Look for a new identifier if a previous working identifier fails to update.
## Critical Precautions to Prevent Bricking your dsPIC!
**Make sure there are no programs running that will access the TNC! Stop all programs that interact with the TNC. If any program accesses the same serial port during firmware update, the dsPIC will certainly brick. Recovery will require an In-Circuit Serial Programmer or replacement of the dsPIC.**
## flashtnc Command Line Usage (64-bit Windows)
* Open your favorite command line (cmd.exe or Powershell will work)
* Navigate to the directory where you extracted the flashtnc repository
````
PS C:\flashtnc-master> py -3 flashtnc.py [hex file] [serial device]
````
# Instructions for 32-Bit Windows
## Installing Python3 and pyserial (32-Bit Windows)
1. Get the "Windows x86 executable installer", version 3.90 is available here: https://www.python.org/ftp/python/3.9.0/python-3.9.0.exe
2. During the Python3 install process, make sure "add Python to the PATH" is selected.
3. Install pip (not included in the 32-bit Windows version of Python). You can do this from a command line. I use Powershell (right click Windows Menu icon, or search for PowerShell), but the normal cmd.exe command line works too.
````
PS C:\Users\ninoc> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
PS C:\Users\ninoc> python get-pip.py
````
4. Install the pyserial module using pip from the command line.
````
PS C:\Users\ninoc> pip3 install pyserial
````
* If you get an error that includes "The term pip3 is not recognized..." then you may need to add an additional PATH environment variable. To do this, search for "env" in the Windows search bar. Select "Edit the System environment variables". Click on the "Environment Variables..." button at the bottom right of the "Advanced" tab. The "Edit environment variable" window will appear. Click the "New" button, and add this path: %USERPROFILE%\AppData\Local\Programs\Python\Python39\Scripts\ (or use the appropriate Python version you installed).
## Download flashtnc Repository (32-Bit Windows)
* Click the green button above that says **Code**. Select "Download Zip".
* Extract the zip file into a directory you can navigate to easily from a command line.
* The repository includes latest firmware hex file.
## Determine Serial Port Device Identifier (32-Bit Windows)
* The N9600A TNCs use USB to serial bridge devices that are enumerated by the operating system. It's easiest to determine the serial port identifier if the TNC is the only USB serial device attached to the system.  
* In Windows, this will be _comN_ where N is a number. May be double-digits. You can find this in the Control Panel->System->Devices->Ports (COM & LPT). The serial port device identifier might change if you swap out NinoTNCs, reboot the computer, or use a different USB port. Look for a new identifier if a previous working identifier fails to update.
## Critical Precautions to Prevent Bricking your dsPIC!
**Make sure there are no programs running that will access the TNC! Stop all programs that interact with the TNC. If any program accesses the same serial port during firmware update, the dsPIC will certainly brick. Recovery will require an In-Circuit Serial Programmer or replacement of the dsPIC.**
## flashtnc Command Line Usage (32-bit Windows)
* Open your favorite command line (cmd.exe or Powershell will work)
* Navigate to the directory where you extracted the flashtnc repository
````
PS C:\flashtnc-master> py -3 flashtnc.py [hex file] [serial device]
````
# Instructions for Debian Linux
## Installing Python3 and pyserial (Debian Linux)
1. Install Python3 and pip through the package manager.  
````
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip
````
2. Install pyserial.
````
$ pip3 install pyserial
````
## Clone Repository Using git (Debian Linux)
First two lines not required if you already have git installed.
````
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/ninocarrillo/flashtnc
````
## Determine Serial Port Device Identifier (Debian Linux)
* The N9600A TNCs use USB to serial bridge devices that are enumerated by the operating system. It's easiest to determine the serial port identifier if the TNC is the only USB serial device attached to the system.  
* In Linux, this will be _/dev/ttyACMN_ or _/dev/ttyUSBN_. N9600A2 TNCs will end in "USBN", while N9600A3 and later TNCs will end in "ACMN". You can find the last USB serial device enumerated in the system by using the following command:  
````
$ sudo dmesg | grep tty
````
## Critical Precautions to Prevent Bricking your dsPIC!
**Make sure there are no programs running that will access the TNC! Stop all programs that interact with the TNC. If any program accesses the same serial port during firmware update, the dsPIC will certainly brick. Recovery will require an In-Circuit Serial Programmer or replacement of the dsPIC.**
## flastnc Command Line Usage (Debian Linux)
````
$ python3 flashtnc.py [hex file] [serial device]
````
# Notes for All Platforms
## If Python Doesn't Start
If your attempt to launch python fails silently (just returns to the command prompt without an error), then try using an alternative command to start Python: "py", "python", and "python3" may work depending on OS. Use "python --version" to confirm you are invoking Python3.
## What to Expect
During firmware update, the LEDs on the TNC will all light up and some will flash extremely quickly (it will just look like dimming). You'll see a progressive line count as the hex file is transferred. Recent firmware has around 9500 lines. It will take about 2 minutes or less to update the firmware once the script is started. The TNC will reboot when the update is complete.
* The DIP switches can be in any position during this procedure.
* The DIP switch funciton mapping may be different after firmware update, check release notes for the firmware version.
* The update may change TX DELAY control sensitivity. Check this if the firmware update causes old links to stop working.
* The update may also change the functionality of LEDs.
## Windows 10 PowerShell or Command Prompt Example
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
## Debian Linux Example
````
nino@islay:~/flashtnc$ python3 flashtnc.py N9600A-v2-5-1.hex /dev/ttyACM0
Opened port /dev/ttyACM0
Opened file N9600A-v2-5-1.hex
Starting TNC reflash mode. Don't interrupt this process, the dsPIC will brick.
TNC successfully entered bootloader mode.
TNC bootlader version:  a
TNC ready for hex file, starting transfer. This will take a few minutes.
Start time:  20:42:39
Lines written:  1000
Lines written:  2000
Lines written:  3000
Lines written:  4000
Lines written:  5000
Lines written:  6000
Lines written:  7000
Lines written:  8000
Lines written:  9000
End time:  20:44:32
Line count:  9415
Firmware update successful.
nino@islay:~/flashtnc$ 
````
## Need Help? Head over to the NinoTNC forum on https://groups.io
