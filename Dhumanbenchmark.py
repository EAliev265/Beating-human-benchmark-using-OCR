import cv2
import mss.tools
import pytesseract
import keyboard
from PIL import Image
import numpy as np
import time
from pynput.keyboard import Key, Controller
keyboard1 = Controller() 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
lower_blue = (120, 50, 50)
upper_blue = (300, 255, 255)
lower_white = (200, 200, 200)
upper_white = (255, 255, 255)

while True:
    if keyboard.is_pressed('n'):
        break
    if keyboard.read_key() == "m":
        with mss.mss() as sct:
            monitor = {'top': 130, 'left': -90, 'width': 1920, 'height': 300}
            sct_img = sct.grab(monitor)
            pil_img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
            white_mask = cv2.inRange(image, lower_white, upper_white)
            final_mask = cv2.bitwise_or(blue_mask, white_mask)
            result = cv2.bitwise_and(image, image, mask=final_mask)
            cv2.imwrite('result_image.png', result)
            image1 = cv2.imread('result_image.png', 0)
            thresh = cv2.threshold(image1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
            

            cv2.imwrite('result_image2.png', thresh)
            print(data)
            time.sleep(3)
            keyboard1.type(data) 
            converted_num = str(data)
            keyboard1.type(converted_num) 
print("Exited the loop.")
            
