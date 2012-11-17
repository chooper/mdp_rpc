#!/usr/bin/env python

import contextlib
import httplib
import time
import sys
import urlparse

import zmq
from zmq.eventloop.ioloop import IOLoop
import msgpack
from mdp_rpc.client import MRPCClient
import sys


from mdp_rpc.worker import MRPCWorker

if __name__ == '__main__':
    context = zmq.Context()
    endpoint = 'tcp://127.0.0.1:5555'

    client = MRPCClient(context, endpoint)
    # ping.ping(seq_num, timestamp)
    #   -> (PONG, seq_num, timestamp)
    print client.ping.ping(0, time.time())
    print client.ping.time()
    print client.ping.ping('BAD','ARGS','WEE')
    print client.ping.does_not_exist()
    print client.does_not_exist.blah()

