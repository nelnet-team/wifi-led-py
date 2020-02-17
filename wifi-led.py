#!/usr/bin/python3

import subprocess
import pigpio
import os
import sys
import re
import time

#My lame attempt at creating immutable global variables
#I hate mutable global variables
config=("wlan0", "/sbin/wpa_cli", 21, 128, 1000)

class WifiStatus:
    def __init__(self, interface):
        self.interface=interface
        self.statusmap={
            "UNKNOWN": 0,
            "DISCONNECTED": 0,
            "INTERFACE_DISABLED": 0,
            "INACTIVE": 0,
            "SCANNING": 1,
            "AUTHENTICATING": 1,
            "ASSOCIATING": 1,
            "ASSOCIATED": 1,
            "4WAY_HANDSHAKE": 1,
            "GROUP_HANDSHAKE": 1,
            "COMPLETED": 2
        }
    def GetState (self):
        cmd=config[1]
        completed=subprocess.run([cmd, "-i", self.interface, "status"], capture_output=True)
        status=str(completed.stdout)
        rawstate=re.search("wpa_state=(\w+)", status)
        if rawstate == None:
            state="UNKNOWN"
        else:
            state=rawstate.group(1)
        retval=self.statusmap[state]
        return retval

class LED:
    def __init__(self, gpio, brightness):
        self.gpio=int(gpio)
        self.blink=0
        self.freq=config[4]
        self.duty=int(brightness)
        self.blinkoff=int(self.duty / 6)
        self.pigpio=pigpio.pi()
        self.pigpio.set_PWM_frequency(self.gpio, self.freq)
    def LedOn(self):
        print("Turn on LED {}".format(gpio), flush=True)
        self.pigpio.set_PWM_dutycycle(self.gpio, self.duty)
    def LedOff(self):
        print("Turn off LED {}".format(str(gpio)), flush=True)
        self.pigpio.set_PWM_dutycycle(self.gpio, 0)
    def LedBlinkOff(self):
        print("Turn down LED {}".format(str(gpio)), flush=True)
        self.pigpio.set_PWM_dutycycle(self.gpio, self.blinkoff)
    def LedBlink(self):
        if self.blink==1:
            self.blink=0
            self.LedOn()
        else:
            self.blink=1
            self.LedBlinkOff()



def GetInt ():
    interface=config[0]
    if len(sys.argv) > 1:
        interface=sys.argv[1]
        print ("Interface {} from command line".format(interface), flush=True)
    elif "ENV_INT" in os.environ:
        interface=os.getenv("ENV_INT")
        print ("Interface {} from environment".format(interface), flush=True)
    else:
        print ("Using default interface {}".format(interface), flush=True)
    return interface


def GetGPIO ():
    gpio=config[2]
    if len(sys.argv) > 2:
        gpio=sys.argv[2]
        print ("GPIO {} from command line".format(gpio), flush=True)
    elif "ENV_GPIO" in os.environ:
        gpio=os.getenv("ENV_GPIO")
        print ("GPIO {} from environment".format(gpio), flush=True)
    else:
        print ("Using default GPIO {}".format(gpio), flush=True)
    return gpio

def GetBrightness ():
    brightness=config[3]
    if len(sys.argv) > 3:
        gpio=sys.argv[3]
        print ("Brightness {} from command line".format(brightness), flush=True)
    elif "ENV_BRIGHTNESS" in os.environ:
        gpio=os.getenv("ENV_BRIFHTNESS")
        print ("Brightness {} from environment".format(brightness), flush=True)
    else:
        print ("Using default brightness {}".format(brightness), flush=True)
    return brightness


interface=GetInt()
gpio=GetGPIO()
brightness=GetBrightness()

wifi=WifiStatus(interface)

LED=LED(gpio,brightness)
oldstate=3

while True:
    state=wifi.GetState()
    if state == 1:
        LED.LedBlink()
    if state != oldstate:
        print ("New state: {}".format(state), flush=True)
        if state == 2:
            LED.LedOn()
        elif state == 1:
            LED.LedBlink()
        else:
            LED.LedOff()

    oldstate=state
    time.sleep(1)
