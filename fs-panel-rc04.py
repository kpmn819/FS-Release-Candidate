#!/usr/bin/env python3
# ------------ CHANGE LOG -----------------

# V26 went back to the original output routine works now
# V28 need to try to get leds working on other pages [solved]
# V28 flap leds now working, could tidy up the code a bit
# V29 minor change to suppress cursor, this is the last version before adding
# rotary_encoder which will end the ability to edit on the pc because of gpio stuff
# managed to sequester gpio and so it still runs on pc
# V31 replaced all encoder code with stripped 3 version
# V32 some tweaks to make it work on the pi, added no_output for testing



# ---------------- IMPORTS -----------------------------
print('program running fs-panel Release Candidate 00 No delay')
import time
import sys, pygame
from pygame.locals import *
FPS = 30
import os
from pathlib import Path
base_path = Path.cwd()


print(os.name)
if os.name != 'nt':
    import RPi.GPIO as gpio
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(True)
else:
    #base_path = base_path / 'Downloads'
    print(base_path)
    #base_path = base_path / ''

import Data_Module3


# ---------- END IMPORTS --------------------

# ---------- VARIABLE DECLARATIONS ------------
NULL_CHAR = chr(0)
#s = 0.5
release_delay = .4
flap_pos = 0
counter = 10

# these pairs need to be kept in order so we can add 1 to the
# first to get the second because can't pass both to routine
enc1_pins = [19,20]
enc2_pins = [21,22]
enc3_pins = [23,24]
enc4_pins = [25,26]
# possible encoder setup enc1_change = [True/False, Direction]
enc1_stat = [False, '']
enc2_stat = [False, '']
enc3_stat = [False, '']
enc4_stat = [False, '']




if os.name != 'nt':
     # define the Encoder switch inputs
    gpio.setup(enc1_pins[0], gpio.IN) # pull-ups are too weak, they introduce noise
    gpio.setup(enc1_pins[1], gpio.IN)
    gpio.setup(enc2_pins[0], gpio.IN) 
    gpio.setup(enc2_pins[1], gpio.IN)
    gpio.setup(enc3_pins[0], gpio.IN) 
    gpio.setup(enc3_pins[1], gpio.IN)
    gpio.setup(enc4_pins[0], gpio.IN) 
    gpio.setup(enc4_pins[1], gpio.IN)




# --------END VARIABLE DECLARATIONS

# --------- START DEFINE DICTIONARIES -------------
# starting in V14 these are stored in Data_Module to keep this code cleaner
# key dictionary first the modifiers
# WHAT DOES WHAT LISTS DICTIONAIRS ETC
# mod_dict holds the decimal codes for the modifiers ctl, shf, alt
mod_dict = Data_Module3.mod_dict

# now the individual keys
# key_dict holds the decimal codes for the letter and symbol keys
key_dict = Data_Module3.key_dict


# ap_list is a list of the buttons available on autopiolot page
ap_list = Data_Module3.ap_list
# radio_list is a list of the buttons on the com / nav page
radio_list = Data_Module3.radio_list
# aux1_list is a list of the buttons on the aux1 page
aux1_list = Data_Module3.aux1_list
# aux2_list is a list of the buttons on the aux2 page
aux2_list = Data_Module3.aux2_list
# knob lists
ap_knobs = Data_Module3.ap_knobs
radio_knobs = Data_Module3.radio_knobs
# initial page setup
current_pg = ap_list

# individual buttons like ap_on have  
# this form {'name'[0],x1[1],x2[2],y1[3],y2[4],key_mod[5],key_code[6],status[7], number[8]}
# buttons with leds have [9] led_color RGBW
# use these index names for easier access
key_name = 0 
x1 = 1
x2 = 2
y1 = 3
y2 = 4
key_mod = 5
key_code = 6
status = 7
presses = 8
color = 9
# on / off keys
# first the ap page
keys_with_leds = (Data_Module3.ap_on, Data_Module3.tog_ap_alt_hold, Data_Module3.tog_ap_hdg,
                  Data_Module3.tog_apn1_hold, Data_Module3.tog_appr_hold, Data_Module3.tog_ap_bc,
                  Data_Module3.tog_ap_vs, Data_Module3.tog_ap_flc, Data_Module3.tog_fd)
# only one button is active on the aux1 page but Python doesn't seem to like to iterate lists with one item
keys_with_leds_aux1 = (Data_Module3.park_brake, Data_Module3.flaps_up, Data_Module3.flaps_dn)
# ------------- END DEFINE DICTIONARIES -----------------------

# ------------ DEFINE COMMANDS --------------------
# then put the commands together

# ----------- METHODS -------------------
def write_report(key_mod,key_code):
    print('report got ' + str(key_mod) + ', ' + str(key_code))
    report = (chr(int(key_mod)) + chr(int(mod_dict['nul'])) + chr(int(key_code)) + chr(int(mod_dict['nul'])) *5)
    #-------- modifier------------ mfr reserved null ------------- key press ---------------- 5 pad nulls ========
    if (os.name != 'nt') and (no_output == ' '):
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())

        time.sleep(release_delay)
    else:
        pass
    # now release all keys by sending 8 nulls
    report = (chr(int(mod_dict['nul'])) * 8)
    if (os.name != 'nt') and (no_output == ' '):
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())
    else:
        pass

def find_button(key_list, x_touch, y_touch):
    x1 = key_list[1]
    x2 = key_list[2]
    y1 = key_list[3]
    y2 = key_list[4]
    # above we pull the coords of the buttons from big_list[counter]
    # and compare to our touch input
    if x_touch in range (x1, x2 +1) and y_touch in range (y1, y2 +1):
        print('found')
        # bring back the whole current list
        return key_list
        
def sort_list(x_touch, y_touch, current_pg):
        # used to return index of button in list
        counter = 0
        # iterate through big_list to find a match
        #while counter < len(current_pg):
        for items in current_pg:
            found_it = find_button(current_pg[counter], x_touch, y_touch)
            if found_it != None:
                # got it, ready to feed output routine
                print(str(found_it[1]), ' ', str(found_it[2]))
                # returns the index of button that was pressed in its list
                return current_pg[counter]
            counter = counter + 1

def click_wait():
    click_spot =(0,0)
    global knob_event
    while True:
        event = pygame.event.wait()
    
        if event.type == pygame.QUIT: 
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_spot =(pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            print('Clicked in click_wait ', str(click_spot[0]), '-', str(click_spot[1]))
         
            if (0 <= click_spot[0] <= 100) and (500 <= click_spot[1] <= 600):
                print('this should kill it')
                # extreem lower left hidden exit
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
                    print('A Knob Has Turned')
                    # the unicode is a string like '1'
                    click_spot = which_knob(knob_event.unicode)
                    # comes back with something like (-3,-3)
                    # flush it out in case an extra one got in
                    pygame.event.clear()

        break
    return click_spot

def blit_new_bkg(bkg_file):
    global current_pg
    global cur_pygame_bkg
    global flap_pos
    off_x = 15
    off_y = 20
    # this could be tarted up but with only 4 pages gets the job done
    if bkg_file == 'navcom_page.png':
        current_pg = radio_list
    if bkg_file == 'ap_page.png':
        current_pg = ap_list
    if bkg_file == 'aux1_page.png':
        current_pg = aux1_list
    if bkg_file == 'aux2_page.png':
        current_pg = aux2_list
    bkg_path = base_path / bkg_file
    cur_pygame_bkg = bkg_path
    print('in the blitter now')
    background = pygame.image.load(str(bkg_path)).convert_alpha()
    display.blit(background, (0, 0))
    if bkg_file == 'ap_page.png':
        # this strung out code could be better but works
 
        for items in keys_with_leds:
            if items[status] == 'on':
                x_loc = items[x1] + off_x
                y_loc = items[y1] + off_y
                if items[color] == 'red':
                    led_color = red_led
                if items[color] == 'green':
                    led_color = green_led
                if items[color] == 'blue':
                    led_color = blue_led
                if items[color] == 'white':
                    led_color = white_led

                display.blit(led_color, (x_loc, y_loc))
    if bkg_file == 'aux1_page.png':
        for items in keys_with_leds_aux1:
            if items[status] == 'on':
                x_loc = items[x1] + off_x
                y_loc = items[y1] + off_y
                if items[color] == 'red':
                    led_color = red_led
                if items[color] == 'green':
                    led_color = green_led
                if items[color] == 'blue':
                    led_color = blue_led
                if items[color] == 'white':
                    led_color = white_led
                display.blit(led_color,(x_loc, y_loc))
            if (items[key_name] == 'flaps dn') and (flap_pos != 0):
                x_loc = items[x1] + off_x
                y_loc = items[y1] + off_y
                if flap_pos == 1:
                    led_color = red_led
                if flap_pos == 2:
                    led_color = green_led
                if flap_pos == 3:
                    led_color = blue_led
                display.blit(led_color,(x_loc, y_loc))
    pygame.display.flip()

    pass

def led_buttons(changed):
    # toggle the status of the changed button
    # set x,y offset from upper left x1,y1

    global keys_with_leds
    global keys_with_leds_aux1
    global flap_pos

    # find out which screen we are on by where the caller is from
    if changed in ap_list:
        active_buttons = keys_with_leds
    if changed in aux1_list:
        active_buttons = keys_with_leds_aux1

    off_x = 15
    off_y = 20
    # allow multi to pass
    if (changed[status] == 'on') or (changed[status] == 'off'):
        print('ENTERED CHANGE STATUS ', changed[status])
        if changed[status] == 'on':
            changed[status] = 'off'
    
        else:
            changed[status] = 'on'
    # there is special logic for vs/flc index [6] vs, [7] flc
    # if one is on the other must be off
    # the logic routine doesn't send any commands of its own because FS does
    # its own logic to make the change
    if changed in ap_list:
        if (changed == keys_with_leds[6]) or (changed == keys_with_leds[7]):
            vs_vlc_logic(changed)
   
    # blit the background
    global cur_pygame_bkg # !!!! this is the path to the file
    
    cur_background = pygame.image.load(str(cur_pygame_bkg)).convert_alpha()
    display.blit(cur_background, (0,0))
    
    # iterate through the list and blit leds with fixed offset from x1 y1

    for items in active_buttons:
        if items[status] == 'on':
            x_loc = items[x1] + off_x
            y_loc = items[y1] + off_y
            if items[color] == 'red':
                    led_color = red_led
            if items[color] == 'green':
                    led_color = green_led
            if items[color] == 'blue':
                    led_color = blue_led
            if items[color] == 'white':
                    led_color = white_led
            display.blit(led_color, (x_loc, y_loc))

        if (items[key_name] == 'flaps dn') and (flap_pos != 0) :
            print('we are here')
            x_loc = items[x1] + off_x
            y_loc = items[y1] + off_y
            if flap_pos == 1:
                led_color = red_led
            if flap_pos == 2:
                led_color = green_led
            if flap_pos == 3:
                led_color = blue_led
            display.blit(led_color, (x_loc, y_loc))
            
    # flip display
    pygame.display.flip()
    pass

def vs_vlc_logic(flc_or_vs):
    who_called = flc_or_vs # indexes [6] vs, [7] flc
    if who_called == keys_with_leds[7]:
        caller = keys_with_leds[7]
        other = keys_with_leds[6]
    else:
        caller = keys_with_leds[6]
        other = keys_with_leds[7]
    if (caller[status] == 'on') and (other[status] == 'on'):
        other[status] = 'off'
        # change button action
    else:
        pass #caller is already on when here

def multi_color_led(search_result):
    # only the flaps dn key will get the led 
    # this routine is called after the characters are sent
    # so we can inject speciality logic with messing up commands
    global flap_pos
    # flap_pos can only have a value of 0 - 3
    if search_result[key_name] == 'flaps dn':
        flap_pos = flap_pos + 1
        if flap_pos > 3:
            flap_pos = 3
    if search_result[key_name] == 'flaps up':
        flap_pos = flap_pos - 1
        if flap_pos < 0:
            flap_pos = 0
    # special routine for changing color 
    print('multi ', search_result[key_name], ' flap_pos ', str(flap_pos))
    # could be flap_up or flap_dn as of now

def rotation_decode1(enc_pin):
    # gets passed the first of two consecutive gpio ports
   
    # for the flight sim we don't need to maintain a counter rather we are 
    # interested in which encoder was turned and which way
    print('NOW IN ENCODER ROUTINE PORT# ', str(enc_pin))
    global counter
    global enc1_stat
    global enc2_stat
    global enc3_stat
    global enc4_stat
    global enc1_pins
    global enc2_pins
    global enc3_pins
    global enc4_pins
    global knob_event

    time.sleep(0.002) # extra 2 mSec de-bounce time

    # read both of the switches
    Switch_A = gpio.input(enc_pin)
    Switch_B = gpio.input(enc_pin + 1)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        counter += 1
        print ('A == 1 and B == 0 direction -> ', str(counter))
        print('INSIDE THE ENCODER 1 STATUS IS', enc1_stat)
        # set the status so it can be read
        if enc_pin == enc1_pins[0]:
            enc1_stat = [True, 'up']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '1', key= pygame.locals.K_1,
            mod= pygame.locals.KMOD_NONE)
        if enc_pin == enc2_pins[0]:
            enc2_stat = [True, 'up']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '2', key= pygame.locals.K_2,
            mod= pygame.locals.KMOD_NONE)
        if enc_pin == enc3_pins[0]:
            enc3_stat = [True, 'up']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '3', key= pygame.locals.K_3,
            mod= pygame.locals.KMOD_NONE)
        if enc_pin == enc4_pins[0]:
            enc4_stat = [True, 'up']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '4', key= pygame.locals.K_4,
            mod= pygame.locals.KMOD_NONE)
        # generate a pygame event and see who salutes hope we can use this
        
        pygame.event.post(knob_event)
        
        print('KNOB EVENT UP')
        
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        counter -= 1
        print('A == 1 and B == 1 direction <- ', str(counter))
        print('INSIDE THE ENCODER 1 STATUS IS', enc1_stat)
        if enc_pin == enc1_pins[0]:
            enc1_stat = [True, 'dn']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '5', key= pygame.locals.K_5,
            mod= pygame.locals.KMOD_NONE)
        if enc_pin == enc2_pins[0]:
            enc2_stat = [True, 'dn']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '6', key= pygame.locals.K_6,
            mod= pygame.locals.KMOD_NONE)
        if enc_pin == enc3_pins[0]:
            enc3_stat = [True, 'dn']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '7', key= pygame.locals.K_7,
            mod= pygame.locals.KMOD_NONE)
        if enc_pin == enc4_pins[0]:
            enc4_stat = [True, 'dn']
            knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '8', key= pygame.locals.K_8,
            mod= pygame.locals.KMOD_NONE)
       
        pygame.event.post(knob_event)
        print('KNOB EVENT DOWN')
        
        return

    else: # discard all other combinations
        return

def which_knob(event_keysim):
    # feeds neg coords so the proper knob can be selected
    # odd looking numbering but this translates sim_keys 1 - 8
    # to the actual values in Datamodule3
    if event_keysim == '1':
        return (-1,-1)
    if event_keysim == '5':
        return (-2,-2)
    if event_keysim == '2':
        return (-3,-3)
    if event_keysim == '6':
        return (-4,-4)
    if event_keysim == '3':
        return (-5,-5)
    if event_keysim == '7':
        return (-6,-6)
    if event_keysim == '4':
        return (-7,-7)
    if event_keysim == '8':
        return (-8,-8)
    else:
        print('got nothing in which_knob')
        return(0,0)
        


# --------- END METHODS -----------------



# -------- RUN ONCE STUFF ------------------------------------------------------------------------------
no_output = input('spacebar for output ')
if no_output == ' ':
    print('OK output coming up')
else:
    print('No output selected')
    
pygame.init()
if os.name != 'nt':
    display=pygame.display.set_mode((1024,600), pygame.FULLSCREEN)
    #display=pygame.display.set_mode((1024,600))
    # setup an event detection thread for the A encoder switch
    gpio.add_event_detect(enc1_pins[0], gpio.RISING, callback=rotation_decode1, bouncetime=2) # bouncetime in mSec
    gpio.add_event_detect(enc2_pins[0], gpio.RISING, callback=rotation_decode1, bouncetime=2)
    gpio.add_event_detect(enc3_pins[0], gpio.RISING, callback=rotation_decode1, bouncetime=2)
    gpio.add_event_detect(enc4_pins[0], gpio.RISING, callback=rotation_decode1, bouncetime=2)    
else:
    display=pygame.display.set_mode((1024,600))
#pygame.display.set_caption('FS Panel')
# --------- test file code
bkg_path = base_path / 'ap_page.png'  
background = pygame.image.load(str(bkg_path)).convert_alpha()
red_path = base_path / 'red_led.png'
red_led = pygame.image.load(str(red_path)).convert_alpha()
blue_path = base_path / 'blue_led.png'
blue_led = pygame.image.load(str(blue_path)).convert_alpha()
green_path = base_path / 'green_led.png'
green_led = pygame.image.load(str(green_path)).convert_alpha()
white_path = base_path / 'white_led.png'
white_led = pygame.image.load(str(white_path)).convert_alpha()
display.blit(background, (0, 0))
# variable cur_pygame_bkg is used in other routines to blit whatever
# is current
cur_pygame_bkg = bkg_path
pygame.display.flip()

    #
# for some reason the pi does not like the cursor surpressed
#pygame.mouse.set_visible(False)
# this knob_event is here to prevent a crash if a random key is hit
knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= '0', key= pygame.locals.K_0,
            mod= pygame.locals.KMOD_NONE)




# ------------------- END RUN ONCE --------------------------------------------------------

# ////////////////////////////// MAIN PROGRAM START //////////////////////////////////////
def main(): # The actual main program
    
    
    while True:
        try:
            
            # returns mouse coords on click
            click_spot = click_wait()
            
            # if clicked in a blank area None will be returned so ignore
            if click_spot != None:
                # returns the x y coords of the touch point
                # knobs return -1, -1
                x_touch = click_spot[0]
                y_touch = click_spot[1]

                # uses current_pg to decide which buttons are active
                search_result = sort_list(x_touch, y_touch, current_pg)
                # sort_list returns the list buttons attributes in the current page list
                # this list can then be parsed for whatever we want

                # again want to filter None and get ready to blit a new page
                if search_result != None:
                    if search_result[status] == 'page':
                        print('got a page change in main!!!!!!!!!!!!!') 
                        # send the file name to the blitter
                        blit_new_bkg(search_result[key_name])
                    # going to change the active page to AP, NAVCOM, AUX1, AUX2
                    if search_result[status] != 'page':
                        for x in range(0, search_result[presses]):
                            print('Command= ', str(x), ' ',search_result[0])
                            # output the characters to USB port 
                            write_report(search_result[5], search_result[6])
                    # here a button with a led has been pressed
                    # we have already sent the command so can do anything here and it will not
                    # affect the output
                    if (search_result[status] == 'on') or (search_result[status] == 'off'):
                        print(' I got a toggle button-----')
                        led_buttons(search_result)

                    if search_result[status] == 'multi':
                        multi_color_led(search_result)
                        # feed display routines with flaps dn so led blit goes to that button
                        led_buttons(aux1_list[4])
                
            else:
                x_touch = 0
                y_touch = 0
            

       
    
# /////////////////////////////////////// END MAIN PROGRAM /////////////////////////////////////////////////////

        except KeyboardInterrupt:
            #cleanup at end of program
            print('   Shutdown')
            if os.name != 'nt':
                gpio.cleanup()
                pygame.quit()

if __name__ == '__main__':
    main()
    # If this is being run stand-alone then execute otherwise it is being
    # imported and the importing program will use the modules it needs
    main() # Invoke the program
