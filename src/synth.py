import re
import socket

class Synth(Agent):
    def __init__(self, addr=('169.254.128.30', 1234)):
        self.__addr = addr
        self.__keys = ['CFRQ', 'RFLV', 'SWEEP', '*IDN', '*RST']
        self.__sepr = ';'
        self.__term = '\n'

    def _recv(self):
        data = ''
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.__addr)
        conn.settimeout(1)
        conn.send('++read' + self.__term)
        while data.find(self.__term) < 0:
            data += conn.recv(1024)
        conn.close()
        return data[:data.find(self.__term)]

    def _send(self, data):
        data = data.strip()
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.__addr)
        conn.send(data + self.__term)
        conn.close()

    def get(self, keys=['index']):
        result = []
        if keys != ['index']:
            for key in keys:
                self._send(str(key).replace('/', ':') + '?')
                #!!! More logic is probably necessary to filter
                #!!! what comes back
                result.append(self._recv().strip(': \n'))
        else:
            result = self.__keys
        return result

    def set(self, keys, values):
        # Replaces '/' with ':' in keys and tests to ensure the value
        # is set properly
        #!!! Test this to make sure it works!
        result = []
        for key, value in zip(keys, values):
            key = key.replace('/', ':')
            self._send('%s %s' % (key, value))
            test = self.get([key])
            if not key.endswith('/VALUE'):
                regex = re.compile(':VALUE [0-9]+\.[0-9]+;', re.IGNORECASE)
                match = regex.search(test)
                if match:
                    test = match.group()
                    result.append(float(value) == float(test[7:test.index(';')]))
                else:
                    result.append('False')
            else:
                result.append(float(value) == float(test))
        return result

#
# Example scripts, plus some cheating
#
def doSweep(start, stop, inc='1MHZ', time='100MS'):
    """Sets synthesizer mode to SWEPT and performs a sweep."""
    a = Marconi()
    a.set(['CFRQ/MODE'], ['SWEPT'])
    a._send('SWEEP:CFRQ:START %s; STOP %s; INC %s; TIME %s'
            % (start, stop, inc, time))
    a._send('SWEEP:RESET')
    a._send('SWEEP:GO')

def freqSlewTo(stop, inc='1MHZ', time='100MS'):
    a = Marconi()
    a.set(['CFRQ/MODE'], ['SWEPT'])
    a._send('SWEEP:CFRQ:START %s; STOP %s; INC %s; TIME %s'
            % (a,get(['CFRQ/VALUE']), stop, inc, time))
    a._send('SWEEP:GO')
