#!/usr/bin/env python

import sys
import traceback as tb
import msgpack
from mdp.worker import MDPWorker
from .exceptions import NoSuchMethod

class MRPCWorker(MDPWorker):
    """Worker component for RPC implementation.

    Subclass this class and add methods for each routine you want to expose.
    """

    # TODO: Make configurable during init

    # Amount of time (in ms) to send heartbeats
    HB_INTERVAL = 1000
    # Number of heartbeats that can be lost
    HB_LIVENESS = 3

    def _decode_msg(self, req):
        """Decodes a message. Currently just msgpacked dict, may change later.
        """
        return msgpack.unpackb(req[0])

    def on_request(self, req):
        """Parse message and call local method"""
        # Parse arguments
        args, kwargs = self._decode_msg(req)
        method = args[0]
        args = args[1:]

        try:
            # Call local method
            func = getattr(self, method)
            rep = ('OK', func(*args, **kwargs))
        except AttributeError:
            # If method doesn't exist...
            func = None
            rep = ('ERR', 'NXMETHOD', method)
        except Exception:
            # Handle tracebacks
            exc_infos = sys.exc_info()
            rep = ('ERR',
                'EXC',
                str(exc_infos[0]),
                str(exc_infos[1]),
                tb.format_tb(exc_infos[2]),
            )

        # Encode and send the reply
        encoded_rep = msgpack.packb(rep)
        self.reply(encoded_rep)


