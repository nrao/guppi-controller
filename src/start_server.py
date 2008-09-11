#!/usr/bin/env python
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

from cherrypy.wsgiserver import CherryPyWSGIServer
import sys

from agent_server import AgentServer

agent_module = 'agent_sim'
if len(sys.argv) > 1:
    agent_module = sys.argv[1]

AgentClass = __import__(agent_module).AgentClass
server = AgentServer(AgentClass)

try:
    server.start()
    http_server = CherryPyWSGIServer(('0.0.0.0', 9090), server, numthreads = 1)
    http_server.start()
except KeyboardInterrupt:
    http_server.stop()
