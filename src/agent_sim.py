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

"""Simulated agent for parameter passing and profile control.
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

import re

from agent import Agent, index, failure, success, states
import simulator

class AgentSim(Agent):
    """Simulated Agent class."""
    def __init__(self):
        self.parameters_sim = simulator.parameters
        self.profiles_sim = simulator.profiles

    def get(self, keys = index):
        """Get all values of parameters matching keys in keys list.

        If keys is ['index'], return a list of all available parameters.
        i.e. return a list of everything the user can get.

        Keyword arguments:
        keys -- names of parameters to get (default index)
        """
        if keys == index:
            result = self.parameters_sim.keys()
            result.sort()
            return result

        return [self.parameters_sim[key] for key in keys]

    def set(self, keys, values):
        """Set parameters with names which match keys, with supplied values.

        Keyword arguments:
        keys -- sequence of names of parameters to set
        values -- sequence of values of parameters to set
        """
        if keys == index:
            return failure

        result = []
        for i in range(len(keys)):
            if self.parameters_sim.has_key(keys[i]):
                new_value = values[i]
                for j in range(8 - len(new_value)):
                    new_value = '0' + new_value
                self.parameters_sim[keys[i]] = new_value
                result += success
            else:
                result += failure
        return result

    def load(self, keys = index):
        """Load profiles with names which match given keys list.

        If keys is ['index'], return a list of all available profiles to load.
        i.e. return a list of everything the user can load.

        Note that one cannot load a profile on a component in use.

        Keyword arguments:
        keys -- sequence of names of profiles to load (default index)
        """
        profile_re = re.compile('.*fpga(\d).*')

        if keys == index:
            result = []
            possibilities = self.profiles_sim.keys()
            possibilities.sort()

            running = self.unload()
            components = [profile_re.match(key).groups()[0] for key in running]

            for profile in possibilities:
                component = profile_re.match(profile).groups()[0]
                if component not in components:
                    result.append(profile)

            return result

        result = []
        for profile in keys:
            running = self.unload()
            components = [profile_re.match(key).groups()[0] for key in running]
            component = profile_re.match(profile).groups()[0]
            if profile not in self.profiles_sim.keys():
                result += failure
            elif component in components:
                result += failure
            else:
                self.profiles_sim[profile] = states['running']
                result += success

        return result

    def unload(self, keys = index):
        """Unload profiles with names which match given keys list.

        If keys is ['index'], return a list of all loaded profiles.
        i.e. return a list of everything the user can unload.

        Keyword arguments:
        keys -- sequence of names of profiles to unload (default index)
        """
        if keys == index:
            result = [profile for profile in self.profiles_sim.keys() if
                      self.profiles_sim[profile] == states['running'] or
                      self.profiles_sim[profile] == states['unknown']]
            result.sort()
            return result

        result = []
        for profile in keys:
            if profile not in self.profiles_sim.keys():
                result += failure
            elif self.profiles_sim[profile] == states['available']:
                result += failure
            else:
                self.profiles_sim[profile] = states['available']
                result += success
        return result

    def profiles(self, keys = index):
        """Provide information on profiles, either given or found.
        
        If keys is ['index'], return a list of info on all found profiles,
        formatted ['profile_name,s', ...] where s is state of profile.

        See module 'states' property for more information.

        Keyword arguments:
        keys -- sequence of names of profiles for info (default index)
        """
        profiles = self.profiles_sim.keys()
        profiles.sort()
        if keys == index:
            keys = profiles

        result = []
        for profile in keys:
            if profile in profiles:
                profile_state = self.profiles_sim[profile]
                result.append(profile + ',' + profile_state)
            else:
                result.append(profile + ',' + states['unknown'])
        return result

    def parameters(self, keys = index):
        """Provide information on parameters, either given or found.
        
        If keys is ['index'], return a list of info on all found
        parameters, formatted ['parameter_name,s', ...] where s is state of
        parameter.

        See module 'states' property for more information.

        Keyword arguments:
        keys -- sequence of names of parameters for info (default index)
        """
        parameters = self.parameters_sim.keys()
        parameters.sort()
        if keys == index:
            keys = parameters

        result = []
        for parameter in keys:
            if parameter in parameters:
                result.append(parameter + ',' + states['running'])
            else:
                result.append(parameter + ',' + states['unknown'])
        return result

AgentClass = AgentSim

def _test():
    """Test this module:
    >>> client = AgentSim()
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
    _test()
