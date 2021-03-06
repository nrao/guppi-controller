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
from guppi_daq.guppi_utils import guppi_status
from time import sleep
import datetime
import os

class DaqAgent(Agent):
    status = None

    def _open(self):
        self.status = guppi_status()

    def _close(self):
        del self.status
        self.status = None

    def get(self, keys = index):
        self._open()
        self.status.read()
        if keys == index:
            result = self.status.keys()
        else:
            result = [str(self.status[key]) for key in keys]
        self._close()
        return result

    def set(self, keys, values):
        self._open()
        result = []
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            value = type(self.status[key])(value)
            try:
                self.status.update(key, value)
            except:
                result += failure
            else:
                result += success
        # commit updates
        self.status.write()
        self._close()
        return result

    def load(self, keys = index):
        print "To do: Start guppi_daq instance here (making sure not to" +\
              " have too many running)."
        pass
        return failure

    def unload(self, keys = index):
        print "To do: Stop guppi_daq instance here, PID given by shared mem."
        pass
        return failure

    def update_with_gbtstatus(self):
        self._open()
        result = failure
        try:
            self.status.update_with_gbtstatus()
            # commit updates
            self.status.write()
        except:
            result = failure
        else:
            result = success
        self._close()
        return result

    def check_pulse(self, limit=5):
        try:
            self.get(['DAQPULSE'])[0]
        except:
            return False
        pulse = self.get(['DAQPULSE'])[0]
        pulse_format = '%a %b %d %H:%M:%S %Y'
        delta = datetime.timedelta(0, limit)
        pulse_datetime = datetime.datetime.strptime(pulse, pulse_format)
        return datetime.datetime.now() - pulse_datetime < delta

    def _send(self, component, payload):
        # component is ignored for now
        if not self.check_pulse():
            return failure[0]

        # expected states
        states = {'start': 'running',
                  'stop': 'stopped',
                  'quit': 'exiting',
                  }

        # We want to send False on consecutive stops or consecutive starts.
        if states[payload.lower()] == self.get(['DAQSTATE'])[0].lower():
            return failure[0]

        try:
            fifo_path = '/tmp/guppi_daq_control'
            try:
                os.stat(fifo_path)
            except OSError:
                return failure[0]
            fifo = open(fifo_path, 'w+', 0)
            fifo.flush()
            fifo.write(payload + '\n')
            fifo.close()
        except:
            return failure[0]
        else:
            for delay in (0.001, 1, 5,):
                sleep(delay)
                if states[payload.lower()] == self.get(['DAQSTATE'])[0].lower():
                    return success[0]
            return failure[0]

    def send(self, components, payloads):
        results = []
        for i in range(len(components)):
            component = components[i]
            payload = payloads[i]
            if component == 'server':
                results.append(self._send(component, payload))
            else:
                results.append('Error')
        return results

AgentClass = DaqAgent

if __name__ == '__main__':
    daq = DaqAgent()
