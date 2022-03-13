# N9600A Firmware Updater version e
# Nino Carrillo 
# David Arthur
# 19 Feb 2022
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
# 9 firmware not updated - unknown hex file type
# 10 firmware not updated - chip version is dsPIC33EP512GP but hex file is for dsPIC33EP256GP
# 11 firmware not updated - chip version is dsPIC33EP256GP but hex file is for dsPIC33EP512GP
# 12 firmware not updated - incompatible version of Python
# 13 Firmware not updated - could not empty serial buffer in reasonable time
import serial
import sys
import time

if sys.version_info < (3, 0): 
	print("Python version should be 3.x, exiting")
	sys.exit(12)

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
	port = serial.Serial(sys.argv[2], baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, timeout=5)
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

# Determine which version of dsPIC this hex file was compiled for by searching for the first line in the bootloader.
print('Scanning hex file to determine target chip.')
hex_file_target = "unknown"
line = file.readline()
while line != "" and hex_file_target == "unknown":
	if ':108800007a00fa0000002200000f7800c3e8a900f7' in line:
		hex_file_target = "dsPIC33EP512GP"
		print("Hex file target:", hex_file_target)
	if ':10427c007a00fa0000002200000f7800c3e8a900c1' in line:
		hex_file_target = "dsPIC33EP256GP"
		print("Hex file target:", hex_file_target)
	if ':10427c007a00fa00403f9800ce389000010f780089' in line:
		hex_file_target = "dsPIC33EP256GP"
		print("Hex file target:", hex_file_target)
	if ':10427c007c00fa00503f980000002200000f7800ec'in line:
		hex_file_target = "dsPIC33EP256GP"
		print("Hex file target:", hex_file_target)
	if ':102800007c00fa00503f980000002200000f780082' in line:
		hex_file_target = "dsPIC33EP256GP"
		print("Hex file target:", hex_file_target)
	if ':102800002f08b000889fbe008a9fbe008c9fbe002c' in line:
		hex_file_target = "dsPIC33EP256GP"
		print("Hex file target:", hex_file_target)
	if ':108800002f08b000889fbe008a9fbe008c9fbe00cc' in line:
		hex_file_target = "dsPIC33EP512GP"
		print("Hex file target:", hex_file_target)
	line = file.readline()

if hex_file_target == "unknown":
	print("Hex file target:", hex_file_target)
	GracefulExit(port, file, 9)

# Reset file read pointer to beginning
file.seek(0)

print('Opened file', sys.argv[1])

port.reset_input_buffer() # Discard all contents of input buffer
# Now read characters for a while until we're sure all the junk is out
buffer_status = "not empty"
print("Flushing serial buffer.")
loop_count = 0
while buffer_status == "not empty":
	input_data = port.read(1)
	#print(input_data)
	loop_count += 1
	if input_data == b'':
		buffer_status = "empty"
	if loop_count > 10:
		GracefulExit(port, file, 13)


# Check for stranded bootloader
TNC_state = "KISS"
success = 0
port.write(b'R')
input_data = port.read(2) # Wait for 2 'K' characters
try:
	input_data = input_data.decode("ascii")
except:
	print("Unable to decode response.")
finally:
	if input_data == "KK":
		print("Found stranded bootloader.")
		TNC_state = "Stranded"
		success = 1

print("Starting TNC reflash mode. Don't interrupt this process, the dsPIC may brick.")

if TNC_state == "KISS":
	port.write(b'\xc0\x0d\x37\xc0') # Initiate bootloader mode on TNC

	buffer_status = "not empty"
	print("Flushing serial buffer again.")
	loop_count = 0
	while buffer_status == "not empty":
		input_data = port.read(1)
		#print("type is: ", type(input_data))
		#print(input_data)
		if input_data == '':
			buffer_status = "empty"
		if input_data == b'K':
			buffer_status = "ready"
		if loop_count > 300:
			GracefulExit(port, file, 13)

	input_data = port.read(2) # Wait for 2 'K' characters
	try:
		input_data = input_data.decode("ascii")
	except:
		print('Invalid response entering bootloader mode.')
		print(input_data)
		GracefulExit(port, file, 6)
	try_count = 0
	success = 0
	while try_count < 4:
		try_count = try_count + 1
		if input_data != "KK":
			print("Retrying")
			port.close()
			port.open()
			input_data = port.read(1)
			while input_data != b'':
				port.reset_input_buffer() # Discard all contents of input buffer
				input_data = port.read(1)
		else:
			success = 1
			try_count = 4
	else:
		success = 1;

if success == 1:
	print("TNC successfully entered bootloader mode.")
else:
	print('TNC bootloader mode not detected. Terminating.')
	print(input_data)
	port.write(b'R') # Try to return TNC to normal KISS mode
	time.sleep(1)
	GracefulExit(port, file, 6)	

port.write(b'V')# send command to read bootloader version
input_data = port.read(1)
version = input_data.decode('ascii')
if version == 'a' or version == 'b' or version == 'B' or version == 'c' or version == 'd' or version == 'C' or version == 'D' :
	print('TNC bootlader version: ', version)
else:
	print('Unsupported TNC bootloader version, terminating.')
	port.write(b'R') # attempt to reset TNC
	print(version)
	time.sleep(1)
	GracefulExit(port, file, 7)
	
# Check hex file version matches bootloader version
chip_revision = "unknown_chip"
if version == 'a' or version == 'b' or version == 'c' or version == 'd': # these bootloaders are installed in dsPIC33EP256GP
	chip_revision = "dsPIC33EP256GP"

if version == 'B' or version == 'C' or version == 'D': # this bootloader is installed in dsPIC33EP512GP
	chip_revision = "dsPIC33EP512GP"

if chip_revision == "unknown_chip":
	print("Chip revision is unknown, terminating.")
	port.write(b'R') # Try to return TNC to normal KISS mode
	time.sleep(1)
	GracefulExit(port, file, 10)
	
if hex_file_target != chip_revision:
	print("Chip version does not match hex file, terminating.")
	port.write(b'R') # Try to return TNC to normal KISS mode
	time.sleep(1)
	GracefulExit(port, file, 10)

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
