import serial
import time
import subprocess

start_arduino_command = "avrdude -p atmega328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:raspi_to_arduino.ino.hex:i"

result = subprocess.run(start_arduino_command, shell=True, capture_output=True, text=True)

print("Standard Output:")
print(result.stdout)
print("Standard Error:")
print(result.stderr)

serial_port = '/dev/ttyACM0'
baud_rate = 115200

try:
	ser = serial.Serial(serial_port, baud_rate, timeout=1)
	time.sleep(2)
	print("Connected to Arduino on", serial_port)
except Exception as e:
	print("Error opening serial port:", e)
	exit()

while True:
	cmd = input("enter command (1, 0, 2): ").strip()
	if cmd not in ["0", "1", "2"]:
		print("Invalid input. Please enter 0, 1, or 2.")
		continue
	
	ser.write(cmd.encode('utf-8'))
	
	if cmd == "2":
		print("Exiting Python script after sending exit command to Arduino")
		break
	
	time.sleep(0.5)
	
	while ser.in_waiting:
		try:
			response = ser.readline().decode('utf-8').strip()
			if response:
				print("Arduino: ", response)
		except Exception as e:
			print("Error reading serial data:", e)
			break
ser.close()
