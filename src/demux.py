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

from agent import Agent, index, success, failure
from agent_client import AgentClient
from bee2_agent import Bee2Agent

# Hard-code a single client for now...

class Demux(Agent):
    def __init__(self):
        self.clients = {'BEE2': AgentClient(Bee2Agent, host = 'bee2')}

    def get(self, keys = index):
        """Get all values of parameters matching keys in keys list.

        If keys is ['index'], return a list of all available parameters.
        i.e. return a list of everything the user can get.

        Keyword arguments:
        keys -- names of parameters to get (default index)
        """
        if keys == index:
            return ['BEE2/' + key for key in self.clients['BEE2'].get(keys)]
        keys = [key.replace('BEE2/', '') for key in keys]
        return self.clients['BEE2'].get(keys)

    def set(self, keys, values):
        """Set parameters with names which match keys, with supplied values.

        Keyword arguments:
        keys -- sequence of names of parameters to set
        values -- sequence of values of parameters to set
        """
        keys = [key.replace('BEE2/', '') for key in keys]
        return self.clients['BEE2'].set(keys, values)

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
        keys = [key.replace('BEE2/', '') for key in keys]
        return self.clients['BEE2'].load(keys)

    def unload(self, keys = index):
        """Unload profiles with names which match given keys list.

        If keys is ['index'], return a list of all loaded profiles.
        i.e. return a list of everything the user can unload.

        Keyword arguments:
        keys -- sequence of names of profiles to unload (default index)
        """
        if keys == index:
            return ['BEE2/' + key for key in self.clients['BEE2'].unload(keys)]
        keys = [key.replace('BEE2/', '') for key in keys]
        return self.clients['BEE2'].unload(keys)

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

AgentClass = Demux
