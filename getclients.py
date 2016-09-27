#!/usr/bin/env python

import requests
import re
import sys

ROUTER_IP = '192.168.1.1'
COOKIE = dict(Authorization='Basic XXXXXXXXXXXXXXXXXXXXXXXX') # put your auth cookie here
POST_DATA = '''[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,4\r
leaseTimeRemaining\r
MACAddress\r
hostName\r
IPAddress\r
'''
HEADERS = {
    'Content-Type': 'text/plain',
    'Referer': 'http://' + ROUTER_IP + '/'
}

regex = r"\[.*\].\n.*\n.*=(.*)\n.*=(.*)\n.*=(.*)"
subst = "\\3\\t\\1\\t\\2"


def main():

    # Ask the router for a list of DHCP clients
    r = requests.post('http://' + ROUTER_IP + '/cgi?5', data=POST_DATA, cookies=COOKIE, headers=HEADERS)

    if not r.ok:
        print("Got status " + str(r.status_code), file=sys.stderr)
        exit(1)

    # remove the '[error]0' line from the response
    s = r.text[:r.text.rfind('\n')]
    # transform to IP - MAC - Name
    s = re.sub(regex, subst, s, 0)
    # sort by IP
    s = '\n'.join(sorted(s.split('\n')))

    print(s)


if __name__ == "__main__":
    main()
