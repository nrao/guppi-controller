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

class Demux(Agent):
    def __init__(self):
        self.clients = {'BEE2': AgentClient(Bee2Agent, host='bee2', port=8915)
                        , 'POWER': PowerstripAgent()
                        , 'SYNTH': SynthAgent()
                        , 'DAQ': DaqAgent()
                        , 'GPU1/DAQ': AgentClient(DaqAgent, host='gpu1', port=8915)
                        , 'GPU2/DAQ': AgentClient(DaqAgent, host='gpu2', port=8915)
                        , 'GPU3/DAQ': AgentClient(DaqAgent, host='gpu3', port=8915)
                        , 'GPU4/DAQ': AgentClient(DaqAgent, host='gpu4', port=8915)
                        , 'GPU5/DAQ': AgentClient(DaqAgent, host='gpu5', port=8915)
                        , 'GPU6/DAQ': AgentClient(DaqAgent, host='gpu6', port=8915)
                        , 'GPU7/DAQ': AgentClient(DaqAgent, host='gpu7', port=8915)
                        , 'GPU8/DAQ': AgentClient(DaqAgent, host='gpu8', port=8915)
                        , 'GPU9/DAQ': AgentClient(DaqAgent, host='gpu9', port=8915)
                        }
        self.order = sorted(self.clients.keys())
        self.index = {}
        for key in self.order:
            self.index[key + '/' + index[0]] = key

    def get(self, keys = index):
        """Get all values of parameters matching keys in keys list.

        If keys is ['index'], return a list of all available parameters.
        i.e. return a list of everything the user can get.

        Keyword arguments:
        keys -- names of parameters to get (default index)
        """
        if keys == index:
            indices = []
            for name in self.order:
                client = self.clients[name]
                # Returning a get() index should fail silently.
                try:
                    indices += [name + '/' + key for key in client.get(index)]
                except:
                    pass
            return indices
        elif self.index.has_key(keys[0]):
            name = self.index[keys[0]]
            client = self.clients[name]
            return [name + '/' + key for key in client.get(index)]

        # build key order
        client_keys = {'': []}
        for name in self.order:
            client_keys[name] = []
        key_order = []
        for key in keys:
            for name in self.order:
                if re.match('^' + name + '\/', key):
                    key_order.append(name)
                    client_keys[name].append(key)
                    break
            else:
                key_order.append('')
                client_keys[''].append(key)

        client_values = {}
        for name in self.order:
            getmes = [key.replace(name + '/', '') for key in client_keys[name]]
            if getmes:
                client_values[name] = self.clients[name].get(getmes)
        client_values[''] = ['Error' for i in range(len(client_keys['']))]

        result = []
        for name in key_order:
            result.append(client_values[name].pop(0))
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

        # build key order
        client_keys = {'': []}
        client_values = {'': []}
        client_results = {'': []}
        for name in self.order:
            client_keys[name] = []
            client_values[name] = []
            client_results[name] = []
        key_order = []
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            for name in self.order:
                if re.match('^' + name + '\/', key):
                    key_order.append(name)
                    client_keys[name].append(key)
                    client_values[name].append(value)
                    break
            else:
                key_order.append('')
                client_keys[''].append(key)
                client_values[''].append(value)

        for name in self.order:
            setmes = [key.replace(name + '/', '') for key in client_keys[name]]
            setwiths = client_values[name]
            if setmes:
                client_results[name] = self.clients[name].set(setmes, setwiths)
        client_results[''] = ['Error' for i in range(len(client_keys['']))]

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

    def send(self, components, payloads):
        results = []
        # HACK:
        # Support a special case where `send` hits all GPU nodes.
        all_gpus = 'GPUS/DAQ/server'
        if components == [all_gpus] or components[0] == all_gpus:
            for payload in payloads:
                for name in [c for c in self.order if c.startswith('GPU')]:
                    results += self.clients[name].send(['server'], [payload])
            return results
        for i in range(len(components)):
            component = components[i]
            payload = payloads[i]
            for name in self.order:
                server_name = name + '/server'
                if component == server_name:
                    results += self.clients[name].send(['server'], [payload])
                    break
            else:
                results += ['Error']
        return results

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
