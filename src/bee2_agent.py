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

"""Agent subclass for the BEE2.

Note that strict typing is required for standard parameter passing.
   * parameter is a String
   * value is a String
   * parameters are accessed via a list of Strings
   * values are returned via a list of Strings
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"


from agent import index
from agent import Agent

from bee2_utils import Bee2Utils

from binascii import a2b_hex, b2a_hex
from string import zfill


class Bee2Agent(Agent):
    """Agent for the BEE2.

    Handles incoming requests.
    """
    def __init__(self):
        self.utils = Bee2Utils()


    def get(self, keys = index):
        """Get all values of parameters matching keys in keys list.

        If keys is ['index'], return a list of all available parameters.
        i.e. return a list of everything the user can get.

        Keyword arguments:
        keys -- names of parameters to get (default index)
        """
        result = []
        if keys != index:
            result += [self.utils.reg_read(reg) for reg in keys]
            # Keep hexlification of registers separate to preserve time coupling
            result = [b2a_hex(r) for r in result]
        else:
            result += self.utils.build_file_list()
        return result


    def load(self, keys = index):
        """Load profiles with names which match given keys list.

        If keys is ['index'], return a list of all available profiles to load.
        i.e. return a list of everything the user can load.

        Note that one cannot load a profile on a component in use.

        Keyword arguments:
        keys -- sequence of names of profiles to load (default index)
        """
        result = []
        if keys != index:
            result += [self.utils.bof_start(proc) for proc in keys]
        else:
            result += self.utils.available_bofs()
        return result


    def set(self, keys, values):
        """Set parameters with names which match keys, with supplied values.

        Keyword arguments:
        keys -- sequence of names of parameters to set
        values -- sequence of values of parameters to set
        """
        result = []
        #!!! What happens with an empty list
        if keys[0] and values[0] and len(keys) == len(values):
            # This looks a bit dumb but it relies on integer rounding
            # in the division, so in this case (n/8)*8 != n for all n
            values = [zfill(str(value), 8*((len(value)+7)/8))
                      for value in values]
            result += [self.utils.reg_write(reg, data)
                       for reg, data in zip(keys, values)]
        else:
            self.utils.debug('set: key or value mismatch')
            result += ['False' for i in keys]
        return result
    

    def unload(self, keys = index):
        """Unload profiles with names which match given keys list.

        If keys is ['index'], return a list of all loaded profiles.
        i.e. return a list of everything the user can unload.

        Keyword arguments:
        keys -- sequence of names of profiles to unload (default index)
        """
        result = []
        if keys != index:
            result += [self.utils.bof_stop(proc) for proc in keys]
        else:
            result += self.utils.running_bofs()
        return result


    def profiles(self, keys = index):
        """Provide information on profiles, either given or found.
        
        If keys is ['index'], return a list of info on all found profiles,
        formatted ['profile_name,s', ...] where s is state of profile.

        See module 'states' property for more information.

        Keyword arguments:
        keys -- sequence of names of profiles for info (default index)
        """
        result = []
        if keys != index:
            result += [bof for bof in self.utils.build_proc_list()
                       if bof[:-2] in keys]
        else:
            result += self.utils.build_proc_list()
        return result

AgentClass = Bee2Agent
