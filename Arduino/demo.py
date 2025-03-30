import cv2
import numpy as np
import serial
import time
import subprocess

start_arduino_command = "avrdude -p atmega328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:demo.ino.hex:i"

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
	
ser.write("1".encode('utf-8'))
time.sleep(0.5)
ser.write("2".encode('utf-8'))
time.sleep(0.5)
ser.write("3".encode('utf-8'))
time.sleep(0.5)
ser.write("4".encode('utf-8'))
time.sleep(0.5)

cap = cv2.VideoCapture(-1)
if not cap.isOpened():
	print("Cannot open camera")
	exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("Press 'q' to exit.")
while True:
	ret, frame = cap.read()
	if not ret:
		print("Can't receive frame. Exiting ...")
		
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	lower_red1 = np.array([0, 120, 70])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 120, 70])
	upper_red2 = np.array([180, 255, 255])
		
	mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
	mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
	
	red_mask = cv2.bitwise_or(mask1, mask2)
	
	red_result = cv2.bitwise_and(frame, frame, mask=red_mask)
	
	kernel = np.ones((3, 3), np.uint8)
	red_mask = cv2.erode(red_mask, kernel, iterations=1)
	red_mask = cv2.dilate(red_mask, kernel, iterations=1)
	
	contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	if contours:
		largest_contour = max(contours, key=cv2.contourArea)
		area = cv2.contourArea(largest_contour)
		if area >= 400:
			x, y, w, h = cv2.boundingRect(largest_contour)
			center_x = x + w // 2
			center_y = y + h // 2
			
			if center_x < 320 - 20:
				ser.write("7".encode('utf-8'))
			elif center_x > 320 + 20:
				ser.write("5".encode('utf-8'))
			else:
				ser.write("6".encode('utf-8'))
		else:
			ser.write("5".encode('utf-8'))
	else:
		ser.write("5".encode('utf-8'))
		
	
	cv2.imshow("frame", frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	while ser.in_waiting:
		cap.grab()
		try:
			response = ser.readline().decode('utf-8').strip()
			if response:
				print("Arduino: ", response)
		except Exception as e:
			print("Error reading serial data:", e)
			break
	
ser.write("0".encode('utf-8'))
ser.close()
cap.release()
cv2.destroyAllWindows()
