import cv2
import numpy as np

cap = cv2.VideoCapture(0)
LOWER_SKIN = np.array([0, 30, 60], dtype=np.uint8)     
UPPER_SKIN = np.array([20, 150, 255], dtype=np.uint8)  

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)                        
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      
    mask = cv2.inRange(hsv, LOWER_SKIN, UPPER_SKIN)   
    cv2.imshow("Hand Pong - Frame", frame)
    cv2.imshow("Hand Pong - Skin Mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):            
        break

cap.release()
cv2.destroyAllWindows()