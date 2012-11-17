MDP-RPC
=======

This is a simple (non-production ready) layer for the Majordomo protocol which
is built on top of ZeroMQ.

For the MDP specification see: http://rfc.zeromq.org/spec:7


Example
-------

You'll need three different terminals, screen windows, or whatever.

In terminal one, start the stock pyzmq-mdp broker:

    $ python pyzmq-mdp/mdp/mybroker.py 

In terminal two, start the worker (or many of them!). The example worker 
registers a service named 'ping' that exposes two methods:

* `ping(seq_num, timestamp)` -- Echoes the sequence number and timestamp given
* `time()` -- Returns `time.time()`


    $ python examples/worker.py 

In terminal three, open up a python shell in the examples directory and follow
the instructions:

    $ python
    Python 2.7.3 (default, Aug  1 2012, 05:14:39) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from client import quick_client
    >>> c = quick_client()
    >>> c.ping.time()
    1353111100.29823
    >>> c.ping.ping(0, c.ping.time()) # yeah I know that doesn't make sense :-)
    ('PONG', 0, 1353111149.779033)

The general usage of this implementation is to use
`client.service_name.method(args, kwargs)`. There is really poor exception
support, but at least the worker doesn't crash:

    >>> c.ping.ping('too', 'many', 'args')
    '<type \'exceptions.TypeError\'>\n  File "/home/chooper/projects/pyzmq-mdp-rpc/mdp_rpc/worker.py", line 27, in on_request\n    rep = (\'OK\', func(*args, **kwargs))\n\nping() takes exactly 3 arguments (1 given)'


Installation
------------

First, download this repository. Then:

    $ pip install -r requirements.txt
    $ python setup.py install

