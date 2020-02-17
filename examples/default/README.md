# Defaults config file

The config file, if used, would normally be placed somewhere like
`/etc/default` or wherever your OS stores system defaults.

Two values are recognized:

* `ENV_INT` specifies the wifi interface
    + This is usually something like wlan0
* `ENV_GPIO` specifies the GPIO pin to listen on
    + This is the GPIO pin number, not the board's pin number
* `ENV_BRIGHTNESS` specifies the LED brigthness
    + Range from 1 to 255 (255 is the brightest)

See the top-level README for more information
