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

from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import Array, Float, Integer, String

from agent import Agent
from utility import xstr2float, float2xstr

class AgentServer(SimpleWSGISoapApp):
    def __init__(self, agent_class = None, namespace = None):
        self.agent = None
        self.Agent = agent_class or Agent

        SimpleWSGISoapApp.__init__(self)
        self.__tns__ = namespace or 'urn:cicada'

    def started(self):
        if self.agent:
            return True
        return False

    def start(self):
        self.agent = self.Agent()

    @soapmethod(Array(String), _returns=Array(String))
    def get(self, keys):
        return self.agent.get(keys)

    @soapmethod(Array(String), Array(String), _returns=Array(String))
    def set(self, keys, values):
        return self.agent.set(keys, values)

    @soapmethod(Array(String), _returns=Array(String))
    def load(self, keys):
        return self.agent.load(keys)

    @soapmethod(Array(String), _returns=Array(String))
    def unload(self, keys):
        return self.agent.unload(keys)

    @soapmethod(Array(String), _returns=Array(String))
    def profiles(self, keys):
        return self.agent.profiles(keys)

    @soapmethod(Array(String), _returns=Array(String))
    def parameters(self, keys):
        return self.agent.parameters(keys)

    @soapmethod(Array(String), Array(String), _returns=Array(String))
    def send(self, components, payloads):
        return self.agent.send(components, payloads)

    # To do: clean out non-pure methods, inherit in ControllerServer subclass?
    @soapmethod(_returns=Array(String))
    def arm(self):
        return self.agent.arm()

    @soapmethod(_returns=Array(String))
    def update_with_gbtstatus(self):
        return self.agent.update_with_gbtstatus()

    @soapmethod(_returns=Array(String))
    def gbt_arm(self):
        return self.agent.gbt_arm()

    @soapmethod(_returns=Array(String))
    def power_cycle(self):
        return self.agent.power_cycle()

    @soapmethod(String, Integer, Integer, _returns=Float)
    def xstr2float(self, xstr, frac_bits, sign_bit):
        return xstr2float(xstr, frac_bits, sign_bit)

    @soapmethod(Float, Integer, Integer, _returns=String)
    def float2xstr(self, num, frac_bits, sign_bit):
        return float2xstr(num, frac_bits, sign_bit)
