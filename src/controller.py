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

import time

from agent import Agent, index, success, failure
from demux import Demux

# from utility import generate_mask, xstr2float, float2xstr

class Controller(Agent):
    def __init__(self):
        self.boards = Demux()

        # Controller has a demux, but for now, doesn't add much to methods.
        self.get = self.boards.get
        self.set = self.boards.set
        self.load = self.boards.load
        self.unload = self.boards.unload
        self.profiles = self.boards.profiles
        self.parameters = self.boards.parameters

    def arm(self):
        set_result = self.set(['BEE2/FPGA2/GUPPi_PIPES_ARM'], ['1'])
        time.sleep(1)
        clr_result = self.set(['BEE2/FPGA2/GUPPi_PIPES_ARM'], ['0'])
        result = set_result == success and clr_result == success
        return (str(result),)

    def update_with_gbtstatus(self):
        return self.boards.update_with_gbtstatus()

    def gbt_arm(self):
        if self.update_with_gbtstatus():
            time.sleep(0.5)
            return self.arm()
        else:
            return failure

    def power_cycle(self, wait=3):
        results = []
        bofs = self.unload()
        results += self.unload(bofs)
        results += self.set(['POWER/group/ibobs'], ['Off'])
        time.sleep(wait)
        results += self.set(['POWER/group/ibobs'], ['On'])
        results += self.load(bofs)
        # for now, just return failure or error if any one failed
        if 'False' in results:
            return failure
        elif 'Error' in results:
            return ['Error']
        else:
            return success

AgentClass = Controller
