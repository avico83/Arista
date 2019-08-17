# !/usr/bin/env python
import sys
import subprocess
from jsonrpclib import Server
import syslog

switch = Server("unix:/var/run/command-api.sock")

def ping_service(dst, next_hop, name):
    ping = switch.runCmds(1, ["ping {} -i 1 -c 4".format(next_hop).replace(',', ' ')])
    ping = ping[0]['messages'][0]
    if '100% packet loss' in ping:
        syslog.openlog('Next-Hop {} is unreachable, we remove the routes of {}\n'.format(next_hop, dst), 0, syslog.LOG_LOCAL4)
        syslog.syslog('%%ROUTING-REMOVED-6-LOG: Log msg: Next-Hop {} is unreachable, we remove the routes of {}'.format(next_hop, dst))
        print "\nNext-Hop {} is unreachable, we remove the routes of {}\n".format(next_hop, dst)
        switch.runCmds(1, ["configure", "no ip route {} {} name {}".format(dst, next_hop, name).replace(',', ' ')])
    else:
        syslog.openlog('Next-Hop {} is available, routes are {} available\n'.format(next_hop, dst), 0, syslog.LOG_LOCAL4)
        syslog.syslog('%%ROUTING-ADDED-6-LOG: Log msg: Next-Hop {} is reachable, we added the routes of {}'.format(next_hop, dst))
        print "\nNext-Hop {} became available, we added the routes of {}\n".format(next_hop, dst)
        switch.runCmds(1, ["configure", "ip route {} {} name {}".format(dst, next_hop, name).replace(',' ,' ')])

ping_service(sys.argv[1], sys.argv[2], sys.argv[3])

