# External WiFi LED  For Raspberry Pi

## About

This is a small script, intended to be run from systemd, that controls
an external LED based on WiFi status.

Note: The pin that drives the LED is identified by the [GPIO
Number](https://www.raspberrypi.org/documentation/usage/gpio/) not the
pysical pin number.

The script runs on a 1 second loop. It uses the external `wpa_cli`
command to get the status of the given WiFi interface.  It looks for
the WiFi status, not the Ethernet link up/down status.  There are many
possible states returned by wpa_cli.  This scripts maps them into
three states:

0.  Off, inactive, error, etc.  *LED off*
1.  Establishing link.  *LED blinks*
2.  Link Up.  *LED on*

These states are printed to `STDOUT`, so they will show up in
`journalctl`.  They are numbered from zero for internal reasons.

## Configuration

There are three necessary configuration items:

1.  WiFi interface.  Usually something like `wlan0`

2.  GPIO pin number for LED

3.  Brigtness.  This is a number from 1 to 255, with 255 being the
brightest.

The script can be configured in one of four ways:

+ *Command line args*.  The args are in the same order as listed
above.  The CLI args would only be used for testing or as arguments in
the ExecStart statement in the [systemd unit
file](examples/systemd/wifi-led.service)

+ *Environment Variables*. See [systemd unit
file](examples/systemd/wifi-led.service)

+ *Environment File*. See [defaults file](examples/default/wifi-led)

+  Defaults that I chose and hard-coded:
  +  Interface: wlan0
  +  GPIO Pin: 21
  +  Brightness: 128

## Special Requirements:

* Python 3.5
* [pigpio](http://abyz.me.uk/rpi/pigpio/)
* pigpio from PyPi

## Installation

Place `wifi-led.py` somewhere from where
systemd can run it, such as `/usr/local/bin`.

Modify `examples/systemd/wifi-led.service` and place it in
`/etc/systemd/system`

If using an environment file, modify
`examples/default/wifi-led` and place it where appropriate
for your OS.  In Raspbian this is `/etc/default/`.

    sudo systemctl enable wifi-led.service
    sudo systemctl start wifi-led.service
    sudo systemctl status wifi-led.service


## Debugging

If the service failed or out of curiosity, use
`journalctl` to investigate:

    sudo journalctl -xe -u wifi-led.service
