#!/usr/bin/python3

import subprocess
import pigpio
import os
import sys
import re
import time

class WifiStatus:
    def __init__(self, config):
        self.interface=config.interface
        self.cmd=config.cmd
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
        cmd=self.cmd
        completed=subprocess.run([cmd, "-i", self.interface, "status"], capture_output=True)
        status=str(completed.stdout)
        rawstate=re.search("wpa_state=(\w+)", status)
        if rawstate == None:
            state="UNKNOWN"
        else:
            state=rawstate.group(1)
        return self.statusmap[state]

class LED:
    def __init__(self, config):
        self.gpio=int(config.gpio)
        self.blink=0
        self.freq=int(config.freq)
        self.duty=int(config.brightness)
        self.blinkoff=int(self.duty / 6)
        self.pigpio=pigpio.pi()
        self.pigpio.set_PWM_frequency(self.gpio, self.freq)
    def LedOn(self):
        print("Turn on LED {}".format(self.gpio), flush=True)
        self.pigpio.set_PWM_dutycycle(self.gpio, self.duty)
    def LedOff(self):
        print("Turn off LED {}".format(str(self.gpio)), flush=True)
        self.pigpio.set_PWM_dutycycle(self.gpio, 0)
    def LedBlinkOff(self):
        print("Turn down LED {}".format(str(self.gpio)), flush=True)
        self.pigpio.set_PWM_dutycycle(self.gpio, self.blinkoff)
    def LedBlink(self):
        if self.blink==1:
            self.blink=0
            self.LedOn()
        else:
            self.blink=1
            self.LedBlinkOff()

class Config:
    def __init__(self):
        self.defaults={
            "interface": "wlan0",
            "gpio": 21,
            "brightness": 128
        }
        self.cmd="/sbin/wpa_cli"
        self.freq=1000
        self.SetInt()
        self.SetGPIO()
        self.SetBrightness()
    def SetInt (self):
        interface=self.defaults["interface"]
        if len(sys.argv) > 1:
            interface=sys.argv[1]
            print ("Interface {} from command line".format(interface), flush=True)
        elif "ENV_INT" in os.environ:
            interface=os.getenv("ENV_INT")
            print ("Interface {} from environment".format(interface), flush=True)
        else:
            print ("Using default interface {}".format(interface), flush=True)
        self.interface=interface
    def SetGPIO (self):
        gpio=self.defaults["gpio"]
        if len(sys.argv) > 2:
            gpio=sys.argv[2]
            print ("GPIO {} from command line".format(gpio), flush=True)
        elif "ENV_GPIO" in os.environ:
            gpio=os.getenv("ENV_GPIO")
            print ("GPIO {} from environment".format(gpio), flush=True)
        else:
            print ("Using default GPIO {}".format(gpio), flush=True)
        self.gpio=gpio
    def SetBrightness (self):
        brightness=self.defaults["brightness"]
        if len(sys.argv) > 3:
            gpio=sys.argv[3]
            print ("Brightness {} from command line".format(brightness), flush=True)
        elif "ENV_BRIGHTNESS" in os.environ:
            gpio=os.getenv("ENV_BRIFHTNESS")
            print ("Brightness {} from environment".format(brightness), flush=True)
        else:
            print ("Using default brightness {}".format(brightness), flush=True)
        self.brightness=brightness

def mainloop(oldstate):
    state=wifi.GetState()
    if state == 2:
        LED.LedBlink()
    if state != oldstate:
        print ("New state: {}".format(state), flush=True)
        if state == 1:
            LED.LedOn()
        else:
            LED.LedOff()
    return state

config=Config()
wifi=WifiStatus(config)
LED=LED(config)

loopstate=3

while True:
    loopstate=mainloop(loopstate)
    time.sleep(1)
