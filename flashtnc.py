# N9600A Firmware Updater version a3
# Nino Carrillo 12 Sep 2020
# Exit codes:
# 0 firmware was updated
# 1 firmware not updated - TNC is current
# 2 firmware not updated - not enough arguments
# 3 firmware not updated - could not open serial port
# 4 firmware not updated - could not open file
# 5 firmware not updated - invalid version received from TNC
# 6 firmware not updated - bootloader not detected
# 7 firmware not updated - incompatible bootloader version
# 8 firmware not updated - firmware update failed

import serial
import sys
import time

def GracefulExit(port, file, code):
	try:
		port.close()
		file.close()
	except:
		pass
	finally:
		sys.exit(code)

if len(sys.argv) < 3:
	print('Not enough arguments. Usage: python flashtnc.py <hex file> <serial device>')
	sys.exit(2)

try:
	port = serial.Serial(sys.argv[2], baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, timeout=3)
except:
	print('Unable to open serial port.')
	sys.exit(3)

print('Opened port', sys.argv[2])

try:
	file = open(sys.argv[1], "r")
except:
	print('Unable to open input file.')
	port.close()
	sys.exit(4)

print('Opened file', sys.argv[1])
input_data = port.read(1)
while input_data != b'':
	port.reset_input_buffer() # Discard all contents of input buffer
	input_data = port.read(1)

print("Starting TNC reflash mode. Don't interrupt this process, the dsPIC will brick.")
port.write(b'\xc0\x0d\x37\xc0') # Initiate bootloader mode on TNC
input_data = port.read(2) # Wait for 2 'K' characters
try:
	input_data = input_data.decode("ascii")
except:
	print('Invalid response entering bootloader mode.')
	print(input_data)
	GracefulExit(port, file, 6)
	
if input_data != "KK":
	print('TNC bootloader mode not detected. Terminating.')
	port.write(b'R') # Try to return TNC to normal KISS mode
	time.sleep(1)
	GracefulExit(port, file, 6)

print("TNC successfully entered bootloader mode.")

port.write(b'V')# send command to read bootloader version
input_data = port.read(1)
low_version = 97
high_version = 97
version = input_data[0]
if version <= high_version and version >= low_version:
	print('TNC bootlader version: ', input_data.decode("ascii"))
else:
	print('Unsupported TNC bootloader version, terminating.')
	port.write(b'R') # attempt to reset TNC
	time.sleep(1)
	GracefulExit(port, file, 7)

print('TNC ready for hex file, starting transfer. This will take a few minutes.')
line = file.readline()
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print('Start time: ', current_time)
line_count = 0
while line != "":
	if line_count == 0:
		try:
			for data in line:
				port.write(bytes(data, "ascii"))
				time.sleep(.1) # Write the first line slowly to allow for a page erase.
		except:
			print("Line 1 error.")
		finally:
			input_data = port.read(1)
			if input_data == b'K':
				line_count = line_count + 1
				line = file.readline()
			elif input_data == b'Z':
				print("Flash successful.")
				line = ""
				result = 1
			elif input_data == b'F':
				print("Flash failed, dsPIC may need replacement.")
				line = ""
				result = 0
			elif input_data == b'N':
				print("Line checksum invalid. Hex file may be corrupt.")
				line = ""
				result = 0
			elif input_data == b'X':
				print("Invalid character in line. Hex file may be corrupt.")
				line = ""
				result = 0
			else:
				print("No response from TNC, dsPIC may need replacement or ICSP reflash.")
				line = ""
				result = 0
	else:
		if line_count % 1000 == 0:
			print("Lines written: ", str(line_count))
		try:
			if line[-2:] == "\r\n" or line[-2:] == "\n\r":
				port.write(bytes(line[:-1], "ascii"))
			else:
				port.write(bytes(line, "ascii"))
		except:
			print("Line error.")
		finally:
			input_data = port.read(1)
			if input_data == b'K':
				line_count = line_count + 1
				line = file.readline()
			elif input_data == b'Z':
				line = ""
				result = 1
			elif input_data == b'F':
				print("Flash failed, dsPIC may need replacement.")
				line = ""
				result = 0
			elif input_data == b'N':
				print("Line checksum invalid. Hex file may be corrupt.")
				line = ""
				result = 0
			elif input_data == b'X':
				print("Invalid character in line. Hex file may be corrupt.")
				line = ""
				result = 0
			else:
				print("No response from TNC, dsPIC may need replacement or ICSP reflash.")
				line = ""
				result = 0

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print('End time: ', current_time)
print('Line count: ', str(line_count))

if result == 1:
	print('Firmware update successful.')
else:
	print('Firmware update failed.')
	GracefulExit(port, file, 8)

GracefulExit(port, file, 0)

