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

"""Abstract agent for parameter passing and profile control.

Standard scheme for agent methods in this package.  Agents include:
   * board (e.g. IBOB, BEE2) client
   * demux
   * controller
   * server-client to connect to controller

Note that strict typing is required for standard parameter passing.
   * parameter is a String
   * value is a String
   * parameters are accessed via a list of Strings
   * values are returned via a list of Strings
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

success  = ['True']
failure  = ['False']
index    = ['index']
states   = dict(available = 'a'
                , running = 'r'
                , unknown = 'u'
                )

class Agent:
    """Virtual Agent class."""
    def get(self, keys = index):
        """Get all values of parameters matching keys in keys list.

        If keys is ['index'], return a list of all available parameters.
        i.e. return a list of everything the user can get.

        Keyword arguments:
        keys -- names of parameters to get (default index)
        """
        raise NotImplementedError("virtual method not implemented in class %s"\
                                  % self.__class__.__name__)

    def set(self, keys, values):
        """Set parameters with names which match keys, with supplied values.

        Keyword arguments:
        keys -- sequence of names of parameters to set
        values -- sequence of values of parameters to set
        """
        raise NotImplementedError("virtual method not implemented in class %s"\
                                  % self.__class__.__name__)

    def load(self, keys = index):
        """Load profiles with names which match given keys list.

        If keys is ['index'], return a list of all available profiles to load.
        i.e. return a list of everything the user can load.

        Note that one cannot load a profile on a component in use.

        Keyword arguments:
        keys -- sequence of names of profiles to load (default index)
        """
        raise NotImplementedError("virtual method not implemented in class %s"\
                                  % self.__class__.__name__)

    def unload(self, keys = index):
        """Unload profiles with names which match given keys list.

        If keys is ['index'], return a list of all loaded profiles.
        i.e. return a list of everything the user can unload.

        Keyword arguments:
        keys -- sequence of names of profiles to unload (default index)
        """
        raise NotImplementedError("virtual method not implemented in class %s"\
                                  % self.__class__.__name__)

    def profiles(self, keys = index):
        """Provide information on profiles, either given or found.
        
        If keys is ['index'], return a list of info on all found profiles,
        formatted ['profile_name,s', ...] where s is state of profile.

        See module 'states' property for more information.

        Keyword arguments:
        keys -- sequence of names of profiles for info (default index)
        """
        raise NotImplementedError("virtual method not implemented in class %s"\
                                  % self.__class__.__name__)

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

AgentClass = Agent
