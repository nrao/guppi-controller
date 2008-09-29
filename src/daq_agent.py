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
from guppi_utils import guppi_status

# code simple daq client until interaction with daq is better understood.
class DaqAgent(Agent):
    def __init__(self):
        self.status = guppi_status()

    def get(self, keys = index):
        if keys == index:
            return self.status.keys()

        return [self.status[key] for key in keys]

    def set(self, keys, values):
        # IMPORTANT: need to handle types; current interface assumes type
        result = []
        for i in range(len(keys)):
            try:
                self.status.update(keys[i], values[i])
            except:
                result += failure
            else:
                result += success
        return result

AgentClass = DaqAgent
