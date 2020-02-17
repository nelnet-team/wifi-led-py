# systemd unit

The systemd unit file would normally be placed in `/etc/systemd/system`

The file can set environment variables for the main script, if
desired, in two different ways:

1. The `Environment` option sets the values directly.  See the
comments in the file.

2. The `EnvironmentFile` option specifies a file from which to read
environment variables.  See `examples/default/listen-for-shutdown`.

See the top-level README.md for more information.
