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

from agent import Agent, index
import agent_client

class Client(Agent):
    '''General entry point for all client-side programming/scripting.
    Stand-alone scripts or console/interpreter apps should use this class.

    Example uses:
        c = Client() # currently defaults to localhost
        c.get()

        c = Client(host = 'beef.gb.nrao.edu') # access from anywhere in NRAO
        c.get()

        c = Client(host = 'bee2') # access bee2 from beef
        c.get()
    '''

    def __init__(self, *args, **kwargs):
        self._client = agent_client.AgentClient(*args, **kwargs)

    def arm(self):
        self._client.arm()

    def get(self, keys = index):
        if isinstance(keys, str):
            keys = [keys]
            return self._client.get(keys)[0]
        return self._client.get(keys)

    def set(self, keys, values = None):
        # support set([(key1, value1), (key2, value2)]) and set({...})
        if not values:
            if isinstance(keys, dict):
                keys = keys.items()
            if isinstance(keys, list) or isinstance(keys, tuple):
                items = keys
                keys = []
                values = []
                for k, v in items:
                    keys.append(k)
                    values.append(v)

        # Support using strings instead of lists for a single key, value pair.
        if isinstance(keys, str):
            keys = [keys]
            if isinstance(values, str):
                values = [values]
            return self._client.set(keys, values)[0]

        # Support set(['key1', 'key2'], 'value') to set key1 and key2 to value.
        if isinstance(values, str):
            values = [values] * len(keys)
        elif len(values) == 1 and len(keys) > 1:
            values = values * len(keys)

        return self._client.set(keys, values)

    def parameters(self, keys = index):
        if isinstance(keys, str):
            keys = [keys]
            return self._client.parameters(keys)[0]
        return self._client.parameters(keys)

    def profiles(self, keys = index):
        if isinstance(keys, str):
            keys = [keys]
            return self._client.profiles(keys)[0]
        return self._client.profiles(keys)

    def load(self, keys = index):
        if isinstance(keys, str):
            keys = [keys]
            return self._client.load(keys)[0]
        return self._client.load(keys)

    def unload(self, keys = index):
        if isinstance(keys, str):
            keys = [keys]
            return self._client.unload(keys)[0]
        return self._client.unload(keys)

AgentClient = Client
