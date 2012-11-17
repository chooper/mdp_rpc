#!/usr/bin/env python

import sys
import time
import msgpack
import zmq
zmq.DEALER = zmq.XREQ
zmq.ROUTER = zmq.XREP
from zmq.eventloop.ioloop import IOLoop
from mdp_rpc.worker import MRPCWorker

def debug(msg):
    sys.stderr.write(repr(msg) + "\n")

class PongWorker(MRPCWorker):
    _rpc_service = 'ping'

    def __init__(self, context, endpoint):
        MRPCWorker.__init__(self, context, endpoint, self._rpc_service)

    def ping(self, seq_num, ts):
        return ('PONG', seq_num, ts)

    def time(self):
        return time.time()


if __name__ == '__main__':
    def shutdown(worker):
        worker.shutdown()
        sys.exit(0)

    context = zmq.Context()
    worker = PongWorker(context, "tcp://127.0.0.1:5555")
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        shutdown(worker)
    shutdown(worker)

