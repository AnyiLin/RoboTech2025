import cv2
import numpy as np

cap = cv2.VideoCapture(cv2.CAP_V4L2)
if not cap.isOpened():
	print("Cannot open camera")
	exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
		
		x, y, w, h = cv2.boundingRect(largest_contour)
		
		threshold_area = 400
		
		box_color = (0, 255, 0) if area >= threshold_area else (255, 0, 0)
		
		cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
	

	cv2.imshow('USB Camera', frame)
	#cv2.imshow('Red Mask', red_mask)
	#cv2.imshow('Red Regions', red_result)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
