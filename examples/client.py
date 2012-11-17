#!/usr/bin/env python

import time
import zmq
from mdp_rpc.client import MRPCClient

def quick_client():
    context = zmq.Context()
    endpoint = 'tcp://127.0.0.1:5555'
    return MRPCClient(context, endpoint)

if __name__ == '__main__':
    client = quick_client()

    print client.ping.ping(0, time.time())
    print client.ping.time()
    print client.ping.ping('BAD','ARGS','WEE')
    print client.ping.does_not_exist()
    print client.does_not_exist.blah() # times out

