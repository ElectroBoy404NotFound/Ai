from picamera import PiCamera
from PIL import Image
import io
import board
import busio
import numpy as np
import adafruit_ssd1306
import cv2

from PIL import Image, ImageDraw

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

camera = PiCamera()
camera.resolution = (128, 64)

while True:
    output = np.empty((64, 128, 3), dtype=np.uint8)
    camera.capture(output, 'bgr')
    
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    ret, thrash = cv2.threshold(gray, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    
    rectangles = 0
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        sides = len(approx)
        print(approx)
        la = [0, 0]
        first = [-1, -1]
        for l in approx:
            if first[0] < 0:
                first = l[0]
            print(l)
            draw.line((la[0], la[1], l[0][0], l[0][1]), fill=255, width=1)
            la = l[0]
        draw.line((la[0], la[1], first[0], first[1]), fill=255, width=1)
        if sides == 4:
            rectangles = rectangles + 1
        #    draw.rectangle((approx[0][0][0], approx[0][0][1], approx[2][0][0], approx[2][0][1]), outline=255, fill=0)
    
    print(rectangles, end=" ")
    print("rectanges found!")
    
    oled.image(image)
    oled.show()