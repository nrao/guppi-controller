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

from copy import deepcopy
import re

from agent import Agent, index, success, failure
from agent_client import AgentClient
from bee2_agent import Bee2Agent
from daq_agent import DaqAgent
from powerstrip_agent import PowerstripAgent
from synth_agent import SynthAgent

# Hard-code a single BEE2 client for now...
# ... and hard-code client calls

# ... and create client index parameters:
# (These are used in get(...) below.)
bee2_index = deepcopy(index)
bee2_index[0] = 'BEE2/' + bee2_index[0]

daq_index = deepcopy(index)
daq_index[0] = 'DAQ/' + daq_index[0]

power_index = deepcopy(index)
power_index[0] = 'POWER/' + power_index[0]

synth_index = deepcopy(index)
synth_index[0] = 'SYNTH/' + synth_index[0]

class Demux(Agent):
    def __init__(self):
        self.clients = {'BEE2': AgentClient(Bee2Agent, host = 'bee2',
                                            port = 8915)
                        , 'DAQ': DaqAgent()
                        , 'POWER': PowerstripAgent()
                        , 'SYNTH': SynthAgent()
                        }

    def get(self, keys = index):
        """Get all values of parameters matching keys in keys list.

        If keys is ['index'], return a list of all available parameters.
        i.e. return a list of everything the user can get.

        Keyword arguments:
        keys -- names of parameters to get (default index)
        """
        if keys == index:
            return ['BEE2/' + key for key in self.clients['BEE2'].get(index)] +\
                   ['DAQ/' + key for key in self.clients['DAQ'].get(index)] +\
                   ['POWER/' + key for key in self.clients['POWER'].get(index)] +\
                   ['SYNTH/' + key for key in self.clients['SYNTH'].get(index)]
        elif keys == bee2_index:
            return ['BEE2/' + key for key in self.clients['BEE2'].get(index)]
        elif keys == daq_index:
            return ['DAQ/' + key for key in self.clients['DAQ'].get(index)]
        elif keys == power_index:
            return ['POWER/' + key for key in self.clients['POWER'].get(index)]
        elif keys == synth_index:
            return ['SYNTH/' + key for key in self.clients['SYNTH'].get(index)]

        # HACK:
        # try out combining BEE2 and DAQ calls
        # keep subsequent get calls to 1 call to BEE2 and 1 to DAQ
        # Wow, this BADLY needs refactoring... just need to find the time.

        # build key order
        client_keys = {'BEE2': [],
                       'DAQ': [],
                       'POWER': [],
                       'SYNTH': [],
                       '': []}
        key_order = []
        for key in keys:
            if re.match('^BEE2\/', key):
                key_order.append('BEE2')
                client_keys['BEE2'].append(key)
            elif re.match('^DAQ\/', key):
                key_order.append('DAQ')
                client_keys['DAQ'].append(key)
            elif re.match('^POWER\/', key):
                key_order.append('POWER')
                client_keys['POWER'].append(key)
            elif re.match('^SYNTH\/', key):
                key_order.append('SYNTH')
                client_keys['SYNTH'].append(key)
            else:
                key_order.append('')
                client_keys[''].append(key)

        bee2_keys = [key.replace('BEE2/', '') for key in client_keys['BEE2']]
        bee2_values = self.clients['BEE2'].get(bee2_keys)
        daq_keys = [key.replace('DAQ/', '') for key in client_keys['DAQ']]
        daq_values = self.clients['DAQ'].get(daq_keys)
        power_keys = [key.replace('POWER/', '') for key in client_keys['POWER']]
        power_values = self.clients['POWER'].get(power_keys)
        synth_keys = [key.replace('SYNTH/', '') for key in client_keys['SYNTH']]
        synth_values = self.clients['SYNTH'].get(synth_keys)
        none_keys = client_keys['']
        none_values = ['Error' for i in range(len(none_keys))]

        # build result
        client_values = {'BEE2': bee2_values,
                         'DAQ': daq_values,
                         'POWER': power_values,
                         'SYNTH': synth_values,
                         '': none_values}

        result = []
        for key in key_order:
            result.append(client_values[key].pop(0))
        return result

    def set(self, keys, values):
        """Set parameters with names which match keys, with supplied values.

        Keyword arguments:
        keys -- sequence of names of parameters to set
        values -- sequence of values of parameters to set
        """
        # Tweak values.
        value_convert = {'None': ''
                         , 'NULL': None
                         , index[0] : ''}
        values = [value_convert.get(value, value) for value in values]

        # HACK:
        # try out combining BEE2 and DAQ calls
        # keep subsequent get calls to 1 call to BEE2 and 1 to DAQ
        # Wow, this BADLY needs refactoring... just need to find the time.

        # build key order
        client_keys = {'BEE2': [],
                       'DAQ': [],
                       'POWER': [],
                       'SYNTH': [],
                       '': []}
        client_values = {'BEE2': [],
                         'DAQ': [],
                         'POWER': [],
                         'SYNTH': [],
                         '': []}
        key_order = []
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            if re.match('^BEE2\/', key):
                key_order.append('BEE2')
                client_keys['BEE2'].append(key)
                client_values['BEE2'].append(value)
            elif re.match('^DAQ\/', key):
                key_order.append('DAQ')
                client_keys['DAQ'].append(key)
                client_values['DAQ'].append(value)
            elif re.match('^POWER\/', key):
                key_order.append('POWER')
                client_keys['POWER'].append(key)
                client_values['POWER'].append(value)
            elif re.match('^SYNTH\/', key):
                key_order.append('SYNTH')
                client_keys['SYNTH'].append(key)
                client_values['SYNTH'].append(value)
            else:
                key_order.append('')
                client_keys[''].append(key)
                client_values[''].append(value)

        bee2_keys = [key.replace('BEE2/', '') for key in client_keys['BEE2']]
        bee2_values = client_values['BEE2']
        daq_keys = [key.replace('DAQ/', '') for key in client_keys['DAQ']]
        daq_values = client_values['DAQ']
        power_keys = [key.replace('POWER/', '') for key in client_keys['POWER']]
        power_values = client_values['POWER']
        synth_keys = [key.replace('SYNTH/', '') for key in client_keys['SYNTH']]
        synth_values = client_values['SYNTH']
        none_keys = client_keys['']
        none_values = client_values['']

        # build result
        bee2_results = []
        daq_results = []
        power_results = []
        synth_results = []
        none_results = []

        if 'BEE2' in key_order:
            bee2_results = self.clients['BEE2'].set(bee2_keys, bee2_values)
        if 'DAQ' in key_order:
            daq_results = self.clients['DAQ'].set(daq_keys, daq_values)
        if 'POWER' in key_order:
            power_results = self.clients['POWER'].set(power_keys, power_values)
        if 'SYNTH' in key_order:
            synth_results = self.clients['SYNTH'].set(synth_keys, synth_values)

        for key in none_keys:
            none_results += failure
        client_results = {'BEE2': bee2_results,
                          'DAQ': daq_results,
                          'POWER': power_results,
                          'SYNTH': synth_results,
                          '': none_results}

        result = []
        for key in key_order:
            result.append(client_results[key].pop(0))
        return result

    def load(self, keys = index):
        """Load profiles with names which match given keys list.

        If keys is ['index'], return a list of all available profiles to load.
        i.e. return a list of everything the user can load.

        Note that one cannot load a profile on a component in use.

        Keyword arguments:
        keys -- sequence of names of profiles to load (default index)
        """
        if keys == index:
            return ['BEE2/' + key for key in self.clients['BEE2'].load(keys)]
        # keys = [key.replace('BEE2/', '') for key in keys]
        # return self.clients['BEE2'].load(keys)

        # HACK:
        # try out combining BEE2 and DAQ calls
        # keep subsequent get calls to 1 call to BEE2 and 1 to DAQ

        # build key order
        client_keys = {'BEE2': [],
                       'DAQ': [],
                       '': []}
        key_order = []
        for key in keys:
            if re.match('^BEE2\/', key):
                key_order.append('BEE2')
                client_keys['BEE2'].append(key)
            elif re.match('^DAQ$', key):
                key_order.append('DAQ')
                client_keys['DAQ'].append(key)
            else:
                key_order.append('')
                client_keys[''].append(key)

        bee2_keys = [key.replace('BEE2/', '') for key in client_keys['BEE2']]
        bee2_values = self.clients['BEE2'].load(bee2_keys)
        daq_keys = index
        daq_values = []
        if client_keys['DAQ']:
            daq_values = self.clients['DAQ'].load(daq_keys)
        daq_values = [daq_values[0] for i in range(len(client_keys['DAQ']))]
        none_keys = client_keys['']
        none_values = ['Error' for i in range(len(none_keys))]

        # build result
        client_values = {'BEE2': bee2_values,
                         'DAQ': daq_values,
                         '': none_values}

        result = []
        for key in key_order:
            result.append(client_values[key].pop(0))
        return result

    def unload(self, keys = index):
        """Unload profiles with names which match given keys list.

        If keys is ['index'], return a list of all loaded profiles.
        i.e. return a list of everything the user can unload.

        Keyword arguments:
        keys -- sequence of names of profiles to unload (default index)
        """
        if keys == index:
            return ['BEE2/' + key for key in self.clients['BEE2'].unload(keys)]
        # keys = [key.replace('BEE2/', '') for key in keys]
        # return self.clients['BEE2'].unload(keys)

        # HACK:
        # try out combining BEE2 and DAQ calls
        # keep subsequent get calls to 1 call to BEE2 and 1 to DAQ

        # build key order
        client_keys = {'BEE2': [],
                       'DAQ': [],
                       '': []}
        key_order = []
        for key in keys:
            if re.match('^BEE2\/', key):
                key_order.append('BEE2')
                client_keys['BEE2'].append(key)
            elif re.match('^DAQ$', key):
                key_order.append('DAQ')
                client_keys['DAQ'].append(key)
            else:
                key_order.append('')
                client_keys[''].append(key)

        bee2_keys = [key.replace('BEE2/', '') for key in client_keys['BEE2']]
        bee2_values = self.clients['BEE2'].unload(bee2_keys)
        daq_keys = index
        daq_values = []
        if client_keys['DAQ']:
            daq_values = self.clients['DAQ'].unload(daq_keys)
        daq_values = [daq_values[0] for i in range(len(client_keys['DAQ']))]
        none_keys = client_keys['']
        none_values = ['Error' for i in range(len(none_keys))]

        # build result
        client_values = {'BEE2': bee2_values,
                         'DAQ': daq_values,
                         '': none_values}

        result = []
        for key in key_order:
            result.append(client_values[key].pop(0))
        return result

    def profiles(self, keys = index):
        """Provide information on profiles, either given or found.
        
        If keys is ['index'], return a list of info on all found profiles,
        formatted ['profile_name,s', ...] where s is state of profile.

        See module 'states' property for more information.

        Keyword arguments:
        keys -- sequence of names of profiles for info (default index)
        """
        if keys == index:
            return ['BEE2/' + key for key in
                    self.clients['BEE2'].profiles(keys)]
        keys = [key.replace('BEE2/', '') for key in keys]
        return self.clients['BEE2'].profiles(keys)

    def parameters(self, keys = index):
        """Provide information on parameters, either given or found.
        
        If keys is ['index'], return a list of info on all found
        parameters, formatted ['parameter_name,s', ...] where s is state of
        parameter.

        See module 'states' property for more information.

        Keyword arguments:
        keys -- sequence of names of parameters for info (default index)
        """
        raise NotImplementedError("virtual method not implemented in class %s"\
                                  % self.__class__.__name__)

    def update_with_gbtstatus(self):
        return self.clients['DAQ'].update_with_gbtstatus()

AgentClass = Demux
