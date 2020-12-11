#!/usr/bin/env python3
# ------------ IMPORTS -----------------
# this is a change
# starting with 19 is the change log
# known issue click_wait passing 0,0 back during mouse move and mouse up
# no exit with lower left mouse click
# in 19 starting cleanup of unused stuff in Data_Modual3
# got rid of specific refs to ap_page instead using current_pg everywhere
# going to add page change intercept to main
# major updates got page switching working properly implimented led keys
# known issues: on return to AP page leds not lighting, no end program from LL click
# return issue fixed in 21, going to add color and test vs/vlc logic in 22
print('program running V21')
import time
import sys, pygame
#from pygame.locals import *
FPS = 30
import os
from pathlib import Path
base_path = Path.cwd()
base_path = base_path / 'Downloads'

print(os.name)
if os.name != 'nt':
    import RPi.GPIO as gpio
    gpio.setmode(gpio.BCM)

import Data_Module3

# ---------- END IMPORTS --------------------
# ----------START SET VARIABLES ------------
# these are the indexes for the key list
# {'name'[0],x1[1],x2[2],y1[3],y2[4],key_mod[5],key_code[6],status[7], number[8]}


# ----------END SET VARIABLES ---------------




# ---------- VARIABLE DECLARATIONS ------------
NULL_CHAR = chr(0)
s = 0.5
release_delay = .2

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
led_color = 9
# on / off keys

keys_with_leds = (Data_Module3.ap_on, Data_Module3.tog_ap_alt_hold, Data_Module3.tog_ap_hdg,
                  Data_Module3.tog_apn1_hold, Data_Module3.tog_appr_hold, Data_Module3.tog_ap_bc,
                  Data_Module3.tog_ap_vs, Data_Module3.tog_ap_flc, Data_Module3.tog_fd)
# this key may be used when returning to the AP page to allow leds to turn on
# without changing any meaningful status
#dummy_key = {'dummy', 0, 1, 0, 1, mod_dict['nul'], key_dict['nul'], 'off', 1}
# ------------- END DEFINE DICTIONARIES -----------------------

# ------------ DEFINE COMMANDS --------------------
# then put the commands together

# ----------- METHODS ------------------
def write_report(key_mod,key_code):
    print('report got ' + str(key_mod) + ', ' + str(key_code))
    report = (chr(int(key_mod)) + chr(int(mod_dict['nul'])) + chr(int(key_code)) + chr(int(mod_dict['nul'])) *5)
    #-------- modifier------------ mfr reserved null ------------- key press ---------------- 5 pad nulls ========
    if os.name != 'nt':
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())

        time.sleep(release_delay)
    else:
        pass
    # now release all keys by sending 8 nulls
    report = (chr(int(mod_dict['nul'])) * 8)
    if os.name != 'nt':
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
        counter = 0
        # iterate through big_list to find a match
        while counter < len(current_pg):
            found_it = find_button(current_pg[counter], x_touch, y_touch)
            if found_it != None:
                # got it, ready to feed output routine
                print(str(found_it[1]), ' ', str(found_it[2]))
                return current_pg[counter]
            counter = counter + 1

def click_wait():
    click_spot =(0,0)
    while True:
        event = pygame.event.wait()
    
        if event.type == pygame.QUIT: 
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_spot =(pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            print('Clicked in click_wait ', str(click_spot[0]), '-', str(click_spot[1]))
         
            if 0 <= click_spot[0] <= 100 and 600 <= click_spot[1] <= 500:
                print('this should kill it')
            # extreem lower left hidden exit
                pygame.QUIT()
                sys.exit()

        break
    return click_spot

def blit_new_bkg(bkg_file):
    global current_pg
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
    print('in the blitter now')
    background = pygame.image.load(str(bkg_path)).convert_alpha()
    display.blit(background, (0, 0))
    if bkg_file == 'ap_page.png':
        # for now this is the only page with leds so go get them
        for items in keys_with_leds:
            if items[status] == 'on':
                x_loc = items[x1] + off_x
                y_loc = items[y1] + off_y
                display.blit(red_led, (x_loc, y_loc))
    pygame.display.flip()

    pass

def led_buttons(changed, keys_with_leds):
    # toggle the status of the changed button
    # set x,y offset from upper left x1,y1
    off_x = 15
    off_y = 20
    if changed[status] == 'on':
        changed[status] = 'off'
    else:
        changed[status] = 'on'
   
    # blit the background
    display.blit(background, (0,0))
    # iterate through the list and blit leds with fixed offset from x1 y1
    for items in keys_with_leds:
        if items[status] == 'on':
            x_loc = items[x1] + off_x
            y_loc = items[y1] + off_y
            display.blit(red_led, (x_loc, y_loc))
            
    # flip display
    pygame.display.flip()
    pass

def vs_vlc_logic(vlc_or_vs):
    who_called = vlc_or_vs
    if who_called == tog_ap_flc:
        caller = tog_ap_flc
        other = tog_ap_vs
    else:
        caller = tog_ap_vs
        other = tog_ap_flc
    if caller[status] == 'on':
        if other[status] == 'on':
            other[status] = 'off'
        else:
            pass #caller is already on when here
    

# --------- END METHODS -----------------



# -------- RUN ONCE STUFF ---------------

pygame.init()
display=pygame.display.set_mode((1024,600))
pygame.display.set_caption('FS Panel')
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
pygame.display.flip()


# ---------- MAIN PROGRAM START -------------
def main(): # The actual main program
    
    
    while True:
        try:
            
            # returns mouse coords on click
            click_spot = click_wait()
            
            # if clicked in a blank area None will be returned so ignore
            if click_spot != None:
                #print('Clicked Main2 ', str(click_spot[0]), '-', str(click_spot[1]))
                x_touch = click_spot[0]
                y_touch = click_spot[1]

                # uses current_pg to decide which buttons are active
                search_result = sort_list(x_touch, y_touch, current_pg)

                # again want to filter None and get ready to blit a new page
                if search_result != None:
                    if search_result[status] == 'page':
                        print('got a page change in main!!!!!!!!!!!!!') 
                        # send the file name to the blitter
                        blit_new_bkg(search_result[key_name])
                    # going to change the active page to AP, NAVCOM, AUX1, AUX2
                    if search_result[status] != 'page':
                        print('Command= ',search_result[0])
                        write_report(search_result[5], search_result[6])
                    # here a button with a led has been pressed
                    if (search_result[status] == 'on') or (search_result[status] == 'off'):
                        print(' I got a toggle button-----')
                        led_buttons(search_result, keys_with_leds)

                
            else:
                x_touch = 0
                y_touch = 0
            

       
    
# ------------ END MAIN PROGRAM -----------------

        except KeyboardInterrupt:
            #cleanup at end of program
            print('   Shutdown')
            if os.name != 'nt':
                GPIO.cleanup()

if __name__ == '__main__':
    main()
    # If this is being run stand-alone then execute otherwise it is being
    # imported and the importing program will use the modules it needs
    main() # Invoke the program
