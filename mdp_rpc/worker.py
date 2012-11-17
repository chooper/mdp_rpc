#!/usr/bin/env python

import sys
import traceback as tb
import msgpack
from mdp.worker import MDPWorker
from .exceptions import NoSuchMethod

class MRPCWorker(MDPWorker):
    HB_INTERVAL = 1000
    HB_LIVENESS = 3

    def _decode_msg(self, req):
        """Decodes a message. Currently just msgpacked dict,
        may change later.
        """
        return msgpack.unpackb(req[0])

    def on_request(self, req):
        args, kwargs = self._decode_msg(req)
        method = args[0]
        args = args[1:]

        # call local method
        try:
            func = getattr(self, method)
            rep = ('OK', func(*args, **kwargs))
        except AttributeError:
            # TODO: Tracepacks
            func = None
            rep = ('ERR', 'NXMETHOD', method)
        except Exception:
            exc_infos = sys.exc_info()
            rep = ('ERR',
                'EXC',
                str(exc_infos[0]),
                str(exc_infos[1]),
                tb.format_tb(exc_infos[2]),
            )

        # send reply
        encoded_rep = msgpack.packb(rep)
        self.reply(encoded_rep)


