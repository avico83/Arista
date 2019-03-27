# !/usr/bin/env python

import time
from jsonrpclib import Server
import syslog
import os, ssl


def get_asn():
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context
    switch = Server( "https://<username>:<password>@127.0.0.1/command-api" )
    get_asn = switch.runCmds(1, ["show ip bgp summary"])
    for asn in get_asn:
        local_asn = asn['vrfs']['default']['asn']
        return local_asn


def reroute_traffic():
    try:
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        switch = Server( "https://<username>:<password>@127.0.0.1/command-api" )
        check_monitor = switch.runCmds(1, ["show monitor connectivity"])
        for monitor in check_monitor:
            nei_lst = []
            for k, v in monitor['hosts'].iteritems():
                if v['packetLoss'] > 0:
                    syslog.openlog('Next-Hop {} is unreachable, lowering the local-preference\n'.format(k), 0,syslog.LOG_LOCAL4)
                    syslog.syslog('%%PROB-FAILED-6-LOG: Log msg: Next-Hop {} is unreachable, lowering the local-preference'.format(v['ipAddr']))
                    print ("We are expiriancing packet loss on device ip {} \nchanging the local preference to 50".format(v['ipAddr']))
                    switch.runCmds(1, ["enable", " configure", "router bgp {}".format(get_asn()),
                                       "neighbor {} import-localpref 50".format(v['ipAddr'])])
                    print ("route for neighbor {} changed local-pref to 50".format(v['ipAddr']))

                elif v['packetLoss'] == 0:
                    syslog.openlog('Next-Hop {} is reachable, removing the local-preference config\n'.format(v['ipAddr']), 0,syslog.LOG_LOCAL4)
                    syslog.syslog('%%PROB-SUCCESS-6-LOG: Log msg: Next-Hop {} is reachable, removing the local-preference config'.format(v['ipAddr']))
                    print ("Neighbor {} is reachable changing the local preference to default".format(v['ipAddr']))
                    switch.runCmds(1, ["enable", " configure", "router bgp {}".format(get_asn()),
                                       "no neighbor {} import-localpref 50".format(v['ipAddr'])])
                else:
                    print ("Cannot locate packet loss value")
    except KeyboardInterrupt as e:
        print "Ok Ok, I'm breaking.."
    except IOError as e:
        print e


get_asn()
reroute_traffic()
