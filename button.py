import RPi.GPIO as GPIO
import time
import math

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
attached_button_pin = 17

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(attached_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

#risk global variables
risk_player_state = True
risk_player_1_score = 0
risk_player_2_score = 0
risk_game_state = True
risk_current_turn_troop_counter = 0
risk_nacho_turn_counter = 0

def risk_button_callback(channel):
    global risk_nacho_turn_counter
    if channel == button_pin:
        risk_add_player_score(1)
    elif channel == button_pin2:
        risk_add_player_score(2)

def get_risk_first_player():
    global risk_player_state
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text(((width/3)+3, height/4), "First", font=font, fill=255)
    draw.text((width/3, height/2), "Player?", font=font, fill=255)
    draw.text((width/3, 3*(height/4)), "<    >", font=font, fill=255)
    disp.image(image)
    disp.display()
    return_player = -1
    
    while True:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        if GPIO.input(button_pin) == 0:
            return_player = 1
            risk_player_state = True
            break
        if GPIO.input(button_pin2) == 0:
            return_player = 2
            risk_player_state = False
            break
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if return_player == 1:
        draw.text((width/3, height/4), "Player 1", font=font, fill=255)
        draw.text((width/3, height/2), "Selected", font=font, fill=255)
    elif return_player == 2:
        draw.text((width/3, height/4), "Player 2", font=font, fill=255)
        draw.text((width/3, height/2), "Selected", font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.5)
    
    return return_player

def risk_refresh_display():
    global risk_player_1_score
    global risk_player_2_score
    global risk_player_state
    global risk_current_turn_troop_counter

    num_troops_to_draw = 0
    draw_string = ""
    if risk_player_state == True:
        num_troops_to_draw = risk_player_1_score / 3
    else:
        num_troops_to_draw = risk_player_2_score / 3

    draw_string = "Draw " + str(risk_current_turn_troop_counter)
    
    #update the scores to the display
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    #p1
    draw.text((width-15,0), "P1", font=font, fill=255)
    draw.text((width-15,10), str(risk_player_1_score), font=font, fill=255)
    draw.line((width-20, 0, width-20, height), fill=255)
    
    #p2
    draw.text((5,0), "P2", font=font, fill=255)
    draw.text((5,10), str(risk_player_2_score), font=font, fill=255)
    draw.line((20, 0, 20, height), fill=255)

    #middle section
    #show turn
    if risk_player_state == True: #first player
        draw.text((width/3, 0), "P1 Turn", font=font, fill=255)
        draw.line((width-19, 20, width-19, height), fill=255)
        draw.line((width-18, 20, width-18, height), fill=255)
        draw.line((width-17, 20, width-17, height), fill=255)
        draw.line((width-16, 20, width-16, height), fill=255)
        draw.line((width-15, 20, width-15, height), fill=255)
        draw.line((width-14, 20, width-14, height), fill=255)
        draw.line((width-13, 20, width-13, height), fill=255)
        draw.line((width-12, 20, width-12, height), fill=255)
        draw.line((width-11, 20, width-11, height), fill=255)
        draw.line((width-10, 20, width-10, height), fill=255)
        draw.line((width-9, 20, width-9, height), fill=255)
        draw.line((width-8, 20, width-8, height), fill=255)
        draw.line((width-7, 20, width-7, height), fill=255)
        draw.line((width-6, 20, width-6, height), fill=255)
        draw.line((width-5, 20, width-5, height), fill=255)
        draw.line((width-4, 20, width-4, height), fill=255)
        draw.line((width-3, 20, width-3, height), fill=255)
        draw.line((width-2, 20, width-2, height), fill=255)
        draw.line((width-1, 20, width-1, height), fill=255)
    else:
        draw.text((width/3, 0), "P2 Turn", font=font, fill=255)
        draw.line((19, 20, 19, height), fill=255)
        draw.line((18, 20, 18, height), fill=255)
        draw.line((17, 20, 17, height), fill=255)
        draw.line((16, 20, 16, height), fill=255)
        draw.line((15, 20, 15, height), fill=255)
        draw.line((14, 20, 14, height), fill=255)
        draw.line((13, 20, 13, height), fill=255)
        draw.line((12, 20, 12, height), fill=255)
        draw.line((11, 20, 11, height), fill=255)
        draw.line((10, 20, 10, height), fill=255)
        draw.line((9, 20, 9, height), fill=255)
        draw.line((8, 20, 8, height), fill=255)
        draw.line((7, 20, 7, height), fill=255)
        draw.line((6, 20, 6, height), fill=255)
        draw.line((5, 20, 5, height), fill=255)
        draw.line((4, 20, 4, height), fill=255)
        draw.line((3, 20, 3, height), fill=255)
        draw.line((2, 20, 2, height), fill=255)
        draw.line((1, 20, 1, height), fill=255)
        
    draw.text((width/3, height/4), draw_string, font=font, fill=255)
    #draw.text((width/3, height/2), str(num_troops_to_draw), font=font, fill=255)
    draw.text((width/3, height/2), "Troops", font=font, fill=255)
    
    #show how many troops to draw
    

    disp.image(image)
    disp.display()

def nacho_turn():
    global risk_nacho_turn_counter
    
    risk_nacho_turn_counter += 1
    nacho_response = ""
    #print(str(risk_nacho_turn_counter))#debugging

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    if risk_nacho_turn_counter == 1:
        #nacho_response = "NACHO TURN"
        draw.text((width/3, height/4), "NACHO TURN", font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(2)
    elif risk_nacho_turn_counter == 2:
        draw.text((width/3, 0), "Trying to", font=font, fill=255)
        draw.text((width/3, 10), "rig the", font=font, fill=255)
        draw.text((width/3, 20), "score?", font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(3)
    elif risk_nacho_turn_counter == 3:
        draw.text((width/3, height/4), "Alright", font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(2)
    else:
        risk_refresh_display
        return

    risk_refresh_display()
    

def risk_add_player_score(player):
    global risk_player_1_score
    global risk_player_2_score
    global risk_game_state
    global risk_player_state
    global risk_nacho_turn_counter

    if player == 1:
        if risk_player_state == True:
            #print("1")#debugging
            risk_player_1_score +=1
            risk_player_2_score -= 1
        else:
            #print("2")#debugging
            nacho_turn()
            if risk_nacho_turn_counter > 3:
                risk_player_1_score +=1
                risk_player_2_score -= 1
    elif player == 2:
        if risk_player_state == False:
            #print("3")#debugging
            risk_player_2_score += 1
            risk_player_1_score -= 1
        else:
            #print("4")#debugging
            nacho_turn()
            if risk_nacho_turn_counter > 3:
                risk_player_2_score += 1
                risk_player_1_score -= 1

    if risk_player_1_score == 0 or risk_player_2_score == 0:
        risk_game_state = False
        time.sleep(1)
        #risk_game_over()
    
    #make call to update scores
    risk_refresh_display()

def risk_game_over():
    global risk_player_1_score
    global risk_player_2_score
    global risk_nacho_turn_counter

    risk_nacho_turn_counter = 0

    GPIO.remove_event_detect(button_pin)
    GPIO.remove_event_detect(button_pin2)
    GPIO.remove_event_detect(attached_button_pin)

    disp.clear()
    disp.display()

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/4), "Game", font=font, fill=255)
    draw.text((width/3, height/2), "Over!", font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(2)

    disp.clear()
    disp.display()
    time.sleep(2)

    winner_string = ""
    
    if risk_player_1_score > risk_player_2_score:
        #draw.text((width/3, height/4), "Player 1", font=font, fill=255)
        #draw.text((width/3, height/2), "Wins!!", font=font, fill=255)
        winner_string = "Player 1 Wins!!!"
    else:
        #draw.text((width/3, height/4), "Player 2", font=font, fill=255)
        #draw.text((width/3, height/2), "Wins!!", font=font, fill=255)
        winner_string = "Player 2 Wins !!!"

    amplitude = height/8
    text_height = height/3
    velocity = -5
    startpos = width
    maxwidth, unused = draw.textsize(winner_string, font=font)
    pos = startpos
    winner_counter = 0
    while True:
        #if winner_counter == 2:
            #break
        #else:
            #winner_counter += 1
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Enumerate characters and draw them offset vertically based on a sine wave.
        x = pos
        for i, c in enumerate(winner_string):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            # Calculate offset from sine wave.
            y = (height/4)+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
            # Draw text.
            draw.text((x, y), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        # Draw the image buffer.
        disp.image(image)
        disp.display()
        # Move position for next frame.
        pos += velocity
        # Start over if text has scrolled completely off left side of screen.
        if pos < -maxwidth:
            break
        # Pause briefly before drawing next frame.
        time.sleep(0.1)  


    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((10, height/3), winner_string, font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.7)
    disp.clear()
    disp.display()
    time.sleep(.2)

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((10, height/3), winner_string, font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.7)
    disp.clear()
    disp.display()
    time.sleep(.2)

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((10, height/3), winner_string, font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.7)
    
    #disp.image(image)
    #disp.display()

    disp.clear()
    disp.display()
    time.sleep(1)

#method to switch turns
def risk_attached_button_callback(channel):
    global risk_player_state
    global risk_player_1_score
    global risk_player_2_score
    global risk_current_turn_troop_counter
    global risk_nacho_turn_counter
    risk_nacho_turn_counter = 0
    
    risk_player_state = not risk_player_state
    if risk_player_state == True:
        risk_current_turn_troop_counter = risk_player_1_score / 3
    else:
        risk_current_turn_troop_counter = risk_player_2_score / 3
        
    risk_refresh_display()
    

def play_risk():
    global risk_player_1_score
    global risk_player_2_score
    global risk_game_state
    global risk_current_turn_troop_counter
    global risk_nacho_turn_counter
    risk_nacho_turn_counter = 0
    
    risk_player_1_score = 21
    risk_player_2_score = 21
    risk_current_turn_troop_counter = 21 / 3
            
    
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/4), "loading", font=font, fill=255)
    draw.text((width/3, height/2), "Risk...", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    time.sleep(2)
    first_player = get_risk_first_player()
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=risk_button_callback, bouncetime=500)
    time.sleep(2)
    GPIO.add_event_detect(button_pin2, GPIO.FALLING, callback=risk_button_callback, bouncetime=500)
    time.sleep(.2)
    GPIO.add_event_detect(attached_button_pin, GPIO.FALLING, callback=risk_attached_button_callback, bouncetime=500)
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/3), "Starting...", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    time.sleep(1.5)

    disp.clear()
    disp.display()

    risk_refresh_display()
    while True:
        time.sleep(.5)
        if risk_game_state == False:        
            time.sleep(1)
            risk_game_over()
            break
        
    disp.clear()
    disp.display()
    
    risk_player_1_score = 21
    risk_player_2_score = 21
    risk_game_state = True
    

def play_chess():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/4), "Chess Not", font=font, fill=255)
    #draw.text((width/3, height/2), "Not", font=font, fill=255)
    draw.text((width/4, (height/2)), "Available :(", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    time.sleep(2)
    return 0

try:
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/3), "loading...", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    
    while True:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((width/3, height/4), "< Risk", font=font, fill=255)
        draw.text((width/3, 2*(height/4)), "Chess >", font=font, fill=255)
        disp.image(image)
        disp.display()
        while True:
            if GPIO.input(button_pin) == 0:
                play_chess()
            if GPIO.input(button_pin2) == 0:
                play_risk()
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((width/3, height/4), "< Risk", font=font, fill=255)
            draw.text((width/3, 2*(height/4)), "Chess >", font=font, fill=255)
            disp.image(image)
            disp.display()
        
        time.sleep(60)
        
    
except KeyboardInterrupt:
    GPIO.cleanup()

disp.clear()
disp.display()
GPIO.cleanup()
