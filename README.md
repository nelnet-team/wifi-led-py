# GPIO Shutdown For Raspberry Pi

## About

This is a small script, intended to be run from systemd, that controls
an external LED based on WiFi status.

Note: The pin that drives the LED is identified by the *GPIO Number*
not the pysical pin number

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

The script can be configured in one of three ways:

1. *Command line args*.  The pin is the first arg.  The state
("FALLING" or "RISING") is the second arg.  If no state, or no pin or
state is specified, then the values will either be the hard-coded
defaults or those values that are defined as below.  The command line
args take precedence over the methods 2 or 3.

2. *Environment Variables*. See `examples/systemd/

3. *Environment File*. See `examples/default/

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
