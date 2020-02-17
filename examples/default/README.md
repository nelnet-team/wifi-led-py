# Defaults config file

The config file, if used, would normally be placed somewhere like
`/etc/default` or wherever your OS stores system defaults.

Two values are recognized:

* `ENV_GPIO` specifies the GPIO pin to listen on
    + This is the GPIO pin number, not the board's pin number
* `ENV_STATE` specifies the state to listen for
    + *RISING* or *FALLING*

See the top-level README for more information
