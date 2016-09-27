# GetDHCPClients
Query my TP-Link router's DHCP leases

## Usage

Edit your auth token in the code. Then:
```
$ getclients.py
192.168.1.123	12:34:56:78:9A:BC	Philips-hue
192.168.1.134	DE:F0:12:34:56:78	raspberrypi
192.168.1.156	9A:BC:DE:F0:12:34	android-1234abcd9876123
192.168.1.178	56:78:9A:BC:DE:F0	horst-PC
192.168.1.190	AB:CD:EF:12:34:56	Surface

```

## How
A Python [request](python-requests.org) to what seems to be *TP-LINK AJAX WEB 1.0*
