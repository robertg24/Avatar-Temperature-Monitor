import cv2
from PIL import Image
import numpy as np
import requests

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

red = [0, 0, 255]  # Red color in BGR
green = [0, 255, 0]  # Green color in BGR

cap = cv2.VideoCapture(0)

url = ''

# Airtable API Key
API_KEY = ''

# Headers for the request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json' 
}

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("captured_image.jpg", frame)
        print("Image Captured and Saved!")

        # Read the captured image
        captured_image = cv2.imread("captured_image.jpg")
        
        hsvImage = cv2.cvtColor(captured_image, cv2.COLOR_BGR2HSV)
        
        # Get the dynamic color range for red and green
        lowerLimitRed, upperLimitRed = get_limits(color=red)
        lowerLimitGreen, upperLimitGreen = get_limits(color=green)
        
        # Mask for red color
        maskRed = cv2.inRange(hsvImage, lowerLimitRed, upperLimitRed)
        
        # Mask for green color
        maskGreen = cv2.inRange(hsvImage, lowerLimitGreen, upperLimitGreen)
        
        # Count pixels for red and green masks
        red_pixels = cv2.countNonZero(maskRed)
        green_pixels = cv2.countNonZero(maskGreen)
        
        dominant_color = None
        if red_pixels > green_pixels:
            dominant_color = "Red"
        elif green_pixels > red_pixels:
            dominant_color = "Green"
        
        # Draw rectangles around detected regions in the captured image
        if dominant_color == "Red":
            mask_ = Image.fromarray(maskRed)
            bbox = mask_.getbbox()

            if bbox is not None:
                x1, y1, x2, y2 = bbox
                captured_image_with_box = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        elif dominant_color == "Green":
            mask_= Image.fromarray(maskGreen)
            bbox = mask_.getbbox()

            if bbox is not None:
                x1, y1, x2, y2 = bbox
                captured_image_with_box = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        
        # Show the captured image with box around detected region
        cv2.imshow('Captured Image', captured_image_with_box)
        # Display the dominant color
        if dominant_color is not None:
            print("Dominant Color: " + dominant_color)
            
        payload = {
            'fields':{
                'Color': dominant_color
            }
        }
        response = requests.patch(url, headers=headers, json=payload)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

