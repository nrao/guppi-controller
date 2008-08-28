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

"""AgentServer subclass for the Bee2.

Note: this class is potentially superfluous; an AgentServer using the
appropriate Agent class (Bee2Agent) could be used instead.
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Array
from soaplib.serializers.binary import Attachment

from agent import index
from agent_server import AgentServer
from agent_sim import AgentSim
from bee2_agent import Bee2Agent

class Bee2Server(AgentServer):
    """Bee2Server."""
    
    def __init__(self, agent_class = Bee2Agent, namespace = None):
        AgentServer.__init__(self, agent_class, namespace)


if __name__ == '__main__':
    from cherrypy.wsgiserver import CherryPyWSGIServer

    #bee2server = Bee2Server(AgentSim)
    bee2server = Bee2Server(Bee2Agent)

    try:
        bee2server.start()
        http_server = CherryPyWSGIServer(('0.0.0.0', 8000), bee2server)
        http_server.start()
    except KeyboardInterrupt:
        http_server.stop()
