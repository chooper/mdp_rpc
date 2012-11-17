#!/usr/bin/env python

import zmq
from mdp.client import mdp_request, MDPClient
import msgpack

class ServiceProxy(object):
    """Part of the client component for the RPC implementation. Does all the heavy
    lifting on the client end. Encodes and sends requests, parses replies.
    """

    _service = None
    _client = None
    def __init__(self, client, service):
        self._client = client
        self._service = service

    def __getattr__(self, method, *args, **kwargs):
        if method.startswith('_'):
            raise AttributeError
        return lambda *args, **kargs: self(method, *args, **kargs)

    def __call__(self, method, *args, **kwargs):
        # open connection
        socket = self._client._rpc_context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(self._client._rpc_endpoint)

        # encode message
        msg_struct = ((method,) + args, kwargs)
        msg = msgpack.packb(msg_struct)

        # send request
        raw_rep = mdp_request(socket, bytes(self._service), msg, 2.0) # TODO
        if not raw_rep:
            return # TODO  - better handling of non responses
        rep_decoded = msgpack.unpackb(raw_rep[1])

        # parse formatted response
        formatted_reply = None
        if rep_decoded[0] == 'OK':
            formatted_reply = rep_decoded[1]

        elif rep_decoded[0] == 'ERR':
            if rep_decoded[1] == 'NXMETHOD':
                formatted_reply = 'No Such Method: {}'.format('foo')
            elif rep_decoded[1] == 'EXC':
                formatted_reply = "\n".join([
                    str(rep_decoded[2]),
                    str(rep_decoded[4][0]),
                    str(rep_decoded[3]),
                ])
        # return formatted_replyonse
        return formatted_reply
        

class MRPCClient(MDPClient):
    """Client component for RPC implementation. Really just
    creates ServiceProxy components for given service names.
    """

    def __init__(self, context, endpoint):
        self._rpc_context = context
        self._rpc_endpoint = endpoint

    def __getattr__(self, method, *args, **kwargs):
        if method.startswith('_'):
            raise AttributeError
        return ServiceProxy(self, method)


