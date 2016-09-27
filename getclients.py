#! /usr/bin/env python3

import requests
import re
import sys
import base64
import argparse

POST_DATA = '''[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,4\r
leaseTimeRemaining\r
MACAddress\r
hostName\r
IPAddress\r
'''
regex = r"\[.*\].\n.*\n.*=(.*)\n.*=(.*)\n.*=(.*)"
subst = "\\3\\t\\1\\t\\2"


def main(ip, user, pw):
    encoded_auth = bytes.decode(base64.b64encode(str.encode(user)+b":"+str.encode(pw)))
    cookie = dict(Authorization='Basic '+encoded_auth)

    headers = {
        'Content-Type': 'text/plain',
        'Referer': 'http://' + ip + '/'
    }

    # Ask the router for a list of DHCP clients
    r = requests.post('http://' + ip + '/cgi?5', data=POST_DATA, cookies=cookie, headers=headers)

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
    parser = argparse.ArgumentParser(description='Query a TP-Link router\'s DHCP leases')
    parser.add_argument('-u', '--user', dest='user', type=str, default='admin',
                        help='Username (default: admin)')
    parser.add_argument('-p', '--password', dest='pw', type=str, default='admin',
                        help='Password (default: admin)')
    parser.add_argument('-i', '--ip', dest='ip', type=str, default='192.168.1.1',
                        help='Router IP (default: 192.168.1.1)')

    args = parser.parse_args()
    main(args.ip, args.user, args.pw)
