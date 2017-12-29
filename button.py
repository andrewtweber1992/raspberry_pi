import RPi.GPIO as GPIO
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24

GPIO.setmode(GPIO.BCM)

button_pin = 7
button_pin2 = 12

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
font = ImageFont.load_default()

# Create drawing object.
draw = ImageDraw.Draw(image)

# Define text and get total width.
text = 'Taking over this text!!'
maxwidth, unused = draw.textsize(text, font=font)

counter = 0
loop = 0
loop_running = True

def button_callback(channel):
    global counter
    global loop_running
    #loop_running = False
    print(counter)
    counter += 1
    

try:
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/2, height/2), "test", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=500)
    GPIO.add_event_detect(button_pin2, GPIO.FALLING, callback=button_callback, bouncetime=500)

    while True:
        time.sleep(60)
        
    
except KeyboardInterrupt:
    GPIO.cleanup()

disp.clear()
disp.display()
GPIO.cleanup()
