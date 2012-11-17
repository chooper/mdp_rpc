# -*- coding: utf-8 -*-

"""Module for RPC layer on top of Majordomo Protocol.

For the MDP specification see: http://rfc.zeromq.org/spec:7
"""

__license__ = """
    This file is part of mdp-rpc.

    mdp-rpc is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MDP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with mdp-rpc.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'Charles Hooper'
__email__ = 'charles.hooper@dotcloud.com'


from setuptools import setup

setup(
    name        = 'mdp_rpc',
    package_dir = {'mdp_rpc': 'mdp_rpc'},
    packages    = ['mdp_rpc'],
    zip_safe    = False,
    version     = '0.1',
)
