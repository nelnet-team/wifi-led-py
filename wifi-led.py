#!/usr/bin/python3

import subprocess
import pigpio
import os
import sys
import re
import time


class WifiStatus:
    def __init__(self, config):
        self.interface = config.interface
        self.cmd = config.cmd
        self.statusmap = {
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

    def GetState(self):
        cmd = self.cmd
        completed = subprocess.run(
            [cmd, "-i", self.interface, "status"], capture_output=True)
        status = str(completed.stdout)
        rawstate = re.search("wpa_state=(\w+)", status)
        if rawstate == None:
            state = "UNKNOWN"
        else:
            state = rawstate.group(1)
        return self.statusmap[state]


class LED:
    def __init__(self, config):
        self.gpio = int(config.gpio)
        self.blink = 0
        self.freq = int(config.freq)
        self.duty = int(config.brightness)
        self.blinkoff = int(self.duty / 6)
        self.pigpio = pigpio.pi()
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
        if self.blink == 1:
            self.blink = 0
            self.LedOn()
        else:
            self.blink = 1
            self.LedBlinkOff()


class Config:
    def __init__(self):
        self.defaults = {
            "interface": "wlan0",
            "gpio": 21,
            "brightness": 128
        }
        self.cmd = "/sbin/wpa_cli"
        self.freq = 1000
        self.interface = self.GetVal(1, "interface", "ENV_INT")
        self.gpio = self.GetVal(2, "gpio", "ENV_GPIO")
        self.brightness = self.GetVal(3, "brightness", "ENV_BRIGHTNESS")

    def GetVal(self, argpos, argname, envname):
        thisval = self.defaults[argname]
        if len(sys.argv) > argpos:
            thisval = sys.argv[argpos]
            print("{} {} from command line".format(
                argname, thisval), flush=True)
        elif envname in os.environ:
            thisval = os.getenv(envname)
            print("{} {} from environment".format(
                argname, thisval), flush=True)
        else:
            print("Using default {} {}".format(argname, thisval), flush=True)
        return thisval


def mainloop(oldstate):
    state = wifi.GetState()
    if state == 1:
        LED.LedBlink()
    if state != oldstate:
        print("New state: {}".format(state), flush=True)
        if state == 2:
            LED.LedOn()
        else:
            LED.LedOff()
    return state


def wifi_led():
    while True:
        loopstate = mainloop(loopstate)
        time.sleep(1)


config = Config()
wifi = WifiStatus(config)
LED = LED(config)

loopstate = 3

if __name__ == '__main__':
    wifi_led()
