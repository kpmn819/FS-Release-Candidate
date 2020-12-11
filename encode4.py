#!/usr/bin/python
#-------------------------------------------------------------------------------
# FileName:     Rotary_Encoder-1a.py
# Purpose:      This program decodes a rotary encoder switch.
#

# https://www.raspberrypi.org/forums/viewtopic.php?p=848012

# 10K resistors to ground in parallel with 100 nf caps, 1K resistor to input


#-------------------------------------------------------------------------------

import RPi.GPIO as GPIO
from time import sleep
import pygame
from pygame.locals import *
pygame.init()


# Global constants & variables
# Constants
__author__ = 'Paul Versteeg'

counter = 10  # starting point for the running directional counter

# GPIO Ports
Enc_A = 23  # Encoder input A: input GPIO 23 (active high)
Enc_B = 24  # Encoder input B: input GPIO 24 (active high)
# these pairs need to be kept in order so we can add 1 to the
# first to get the second because can't pass both to routine
enc1_pins = [23,24]
enc2_pins = [25,26]
enc3_pins = [12,13]
enc4_pins = [19,20]
# possible encoder setup enc1_change = [True/False, Direction]
enc1_stat = [False, '']
enc2_stat = [False, '']
enc3_stat = [False, '']
enc4_stat = [False, '']

def init():
    '''
    Initializes a number of settings and prepares the environment
    before we start the main program.
    '''
    print('Rotary Encoder Test Program')

    GPIO.setwarnings(True)

    # Use the Raspberry Pi BCM pins
    GPIO.setmode(GPIO.BCM)

    # define the Encoder switch inputs
    GPIO.setup(enc1_pins[0], GPIO.IN) # pull-ups are too weak, they introduce noise
    GPIO.setup(enc1_pins[1], GPIO.IN)
    GPIO.setup(enc2_pins[0], GPIO.IN) 
    GPIO.setup(enc2_pins[1], GPIO.IN)
    GPIO.setup(enc3_pins[0], GPIO.IN) 
    GPIO.setup(enc3_pins[1], GPIO.IN)
    GPIO.setup(enc4_pins[0], GPIO.IN) 
    GPIO.setup(enc4_pins[1], GPIO.IN)


    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(enc1_pins[0], GPIO.RISING, callback=rotation_decode, bouncetime=2) # bouncetime in mSec
    GPIO.add_event_detect(enc2_pins[0], GPIO.RISING, callback=rotation_decode, bouncetime=2)
    GPIO.add_event_detect(enc3_pins[0], GPIO.RISING, callback=rotation_decode, bouncetime=2)
    GPIO.add_event_detect(enc4_pins[0], GPIO.RISING, callback=rotation_decode, bouncetime=2)
    #
    return


def rotation_decode(enc_pin):
    # gets passed the first of two consecutive gpio ports
    '''
    This function decodes the direction of a rotary encoder and in- or
    decrements a counter.

    The code works from the "early detection" principle that when turning the
    encoder clockwise, the A-switch gets activated before the B-switch.
    When the encoder is rotated anti-clockwise, the B-switch gets activated
    before the A-switch. The timing is depending on the mechanical design of
    the switch, and the rotational speed of the knob.

    This function gets activated when the A-switch goes high. The code then
    looks at the level of the B-switch. If the B switch is (still) low, then
    the direction must be clockwise. If the B input is (still) high, the
    direction must be anti-clockwise.

    All other conditions (both high, both low or A=0 and B=1) are filtered out.

    To complete the click-cycle, after the direction has been determined, the
    code waits for the full cycle (from indent to indent) to finish.

    '''
    # for the flight sim we don't need to maintain a counter rather we are 
    # interested in which encoder was turned and which way

    global counter

    sleep(0.002) # extra 2 mSec de-bounce time

    # read both of the switches
    Switch_A = GPIO.input(enc_pin)
    Switch_B = GPIO.input(enc_pin + 1)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        counter += 1
        print ('direction -> ', str(counter))
        # set the status so it can be read
        if enc_pin == enc1_pins[0]:
            enc1_stat = [True, 'up'] 
        if enc_pin == enc2_pins[0]:
            enc2_stat = [True, 'up']
        if enc_pin == enc3_pins[0]:
            enc3_stat = [True, 'up']
        if enc_pin == enc4_pins[0]:
            enc4_stat = [True, 'up']
        # generate a pygame event and see who salutes hope we can use this
        knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= 'u', key= pygame.locals.K_u,
        mod= pygame.locals.KMOD_NONE)
        pygame.event.post(knob_event)
        # at this point, B may still need to go high, wait for it
        while Switch_B == 0:
            Switch_B = GPIO.input(enc_pin + 1)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(enc_pin + 1)
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        counter -= 1
        print('direction <- ', str(counter))
        if enc_pin == enc1_pins[0]:
            enc1_stat = [True, 'dn'] 
        if enc_pin == enc2_pins[0]:
            enc2_stat = [True, 'dn']
        if enc_pin == enc3_pins[0]:
            enc3_stat = [True, 'dn']
        if enc_pin == enc4_pins[0]:
            enc4_stat = [True, 'dn']
        knob_event = pygame.event.Event(pygame.locals.KEYDOWN, unicode= 'd', key= pygame.locals.K_d,
        mod= pygame.locals.KMOD_NONE)
        pygame.event.post(knob_event)
         # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(enc_pin)
        return

    else: # discard all other combinations
        return



def main():
    '''
    The main routine.

    '''

    try:

        init()
        while True :
            #
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print('have a keydown')
            # wait for an encoder click
            sleep(1)

    except KeyboardInterrupt: # Ctrl-C to terminate the program
        GPIO.cleanup()


if __name__ == '__main__':
    main()