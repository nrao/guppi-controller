# Copyright (C) 2008 Associated Universities, Inc. Washington DC, USA.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

from soaplib.client import make_service_client

from agent import index
from agent_server import AgentServer

def AgentClient(agent_class = None, host = 'localhost', port = 9090):
    return make_service_client('http://%s:%d' % (host, port),
                               AgentServer(agent_class))

def _test():
    """Test this module:
    >>> client = AgentClient()
    >>> keys = client.get(index)
    >>> values = client.get(keys)
    >>> for i in range(len(keys)):
    ...     new_value = values[i][:-1] + str(int(values[i][-1]) + 1)
    ...     print 'set', keys[i], 'from', values[i], 'to', new_value
    ...     client.set([keys[i]], [new_value])
    ...
    set BEE2/FPGA1/TEST_BRAM from FFFFFFFF00000001 to FFFFFFFF00000002
    ['True']
    set BEE2/FPGA1/TEST_REG from 00000001 to 00000002
    ['True']
    set BEE2/FPGA2/TEST_BRAM from FFFFFFFF00000002 to FFFFFFFF00000003
    ['True']
    set BEE2/FPGA2/TEST_REG from 00000002 to 00000003
    ['True']
    set BEE2/FPGA3/TEST_BRAM from FFFFFFFF00000003 to FFFFFFFF00000004
    ['True']
    set BEE2/FPGA3/TEST_REG from 00000003 to 00000004
    ['True']
    set BEE2/FPGA4/testarg from 00000042 to 00000043
    ['True']
    >>> keys = client.get(index)
    >>> values = client.get(keys)
    >>> for i in range(len(keys)):
    ...     new_value = values[i][:-1] + str(int(values[i][-1]) - 1)
    ...     print 'set', keys[i], 'from', values[i], 'to', new_value
    ...     client.set([keys[i]], [new_value])
    ...
    set BEE2/FPGA1/TEST_BRAM from FFFFFFFF00000002 to FFFFFFFF00000001
    ['True']
    set BEE2/FPGA1/TEST_REG from 00000002 to 00000001
    ['True']
    set BEE2/FPGA2/TEST_BRAM from FFFFFFFF00000003 to FFFFFFFF00000002
    ['True']
    set BEE2/FPGA2/TEST_REG from 00000003 to 00000002
    ['True']
    set BEE2/FPGA3/TEST_BRAM from FFFFFFFF00000004 to FFFFFFFF00000003
    ['True']
    set BEE2/FPGA3/TEST_REG from 00000004 to 00000003
    ['True']
    set BEE2/FPGA4/testarg from 00000043 to 00000042
    ['True']
    >>> print client.get(client.get(index))[:4]
    ['FFFFFFFF00000001', '00000001', 'FFFFFFFF00000002', '00000002']
    >>> client.load(index)[:3]
    ['BEE2/FPGA4/testarg']
    >>> client.unload(index)
    ['BEE2/FPGA1/profile_c', 'BEE2/FPGA2/profile_a', 'BEE2/FPGA3/profile_a']
    >>> client.unload(['BEE2/FPGA1/profile_c'])
    ['True']
    >>> client.unload(index)
    ['BEE2/FPGA2/profile_a', 'BEE2/FPGA3/profile_a']
    >>> client.load(['BEE2/FPGA1/profile_a', 'BEE2/FPGA1/profile_b'])
    ['True', 'False']
    >>> client.unload(index)
    ['BEE2/FPGA1/profile_a', 'BEE2/FPGA2/profile_a', 'BEE2/FPGA3/profile_a']
    >>> client.unload(['BEE2/FPGA1/profile_a', 'BEE2/FPGA2/profile_a',
    ...                'BEE2/FPGA3/profile_b', 'BEE2/FPGA3/profile_a'])
    ...
    ['True', 'True', 'False', 'True']
    >>> client.load(['BEE2/FPGA1/profile_b', 'BEE2/FPGA2/profile_b',
    ...              'BEE2/FPGA3/profile_b'])
    ...
    ['True', 'True', 'True']
    >>> client.unload(index)
    ['BEE2/FPGA1/profile_b', 'BEE2/FPGA2/profile_b', 'BEE2/FPGA3/profile_b']
    >>> client.profiles(['fake'])
    ['fake,u']
    >>> client.profiles(['fake1', 'fake2', 'BEE2/FPGA1/profile_b'])
    ['fake1,u', 'fake2,u', 'BEE2/FPGA1/profile_b,r']
    >>> client.profiles(client.load(index))[:2]
    ['BEE2/FPGA4/testarg,a']
    >>> len(client.profiles(index))
    8
    >>> len(client.profiles(client.load(index)))
    1
    >>> client.parameters(index)[:2]
    ['BEE2/FPGA1/TEST_BRAM,r', 'BEE2/FPGA1/TEST_REG,r']
    >>> client.parameters(['fake'])
    ['fake,u']
    >>> client.parameters(['fake1', 'fake2', 'BEE2/FPGA1/TEST_REG'])
    ['fake1,u', 'fake2,u', 'BEE2/FPGA1/TEST_REG,r']
    >>> len(client.parameters(index))
    7
    >>> len(client.parameters(client.get(index)))
    7
    >>> client.unload(client.unload(index))
    ['True', 'True', 'True']
    >>> client.load(['BEE2/FPGA1/profile_c', 'BEE2/FPGA2/profile_a',
    ...              'BEE2/FPGA3/profile_a'])
    ...
    ['True', 'True', 'True']
    >>>
    """
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    client = AgentClient()
    print client.hello('dave')
    print client.listme('dave')
    print client.get(index)
    print client.get(['index'])
    print client.load(['index'])
    print client.profiles(['index'])
    _test()
