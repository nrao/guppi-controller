import re
import socket
from agent import Agent

class SynthAgent(Agent):
    def __init__(self, addr=('gpib_adapter', 1234)):
        self.__addr = addr
        self.__keys = ['CFRQ/VALUE'] # ['CFRQ', 'RFLV', 'CFRQ/VALUE']
        self.__term = '\n'

    def _recv(self):
        data = ''
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.__addr)
        conn.settimeout(10)
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
                if key.find('/') < 0: key += '/VALUE'
                self._send(str(key).replace('/', ':') + '?')
                #!!! More logic is probably necessary to filter
                #!!! what comes back
                #result.append(self._recv().strip(': \n'))
                # Default to MHz for center freq. value.
                received = self._recv().strip(': \n')
                if key == 'CFRQ/VALUE':
                    result.append(re.sub('000000.0$', '', received, 1) + 'MHz')
                else:
                    result.append(received)
        else:
            result = self.__keys
        return result

    def set(self, keys, values):
        """Alternate set.

        Attmempts to ensure that the value was set correctly by writing
        then reading back and checking the value against the request.
        """
        #!!! Stress test
        result = []
        for key, value in zip(keys, values):
            #self._send('%s %s' % (key.replace('/', ':'), value))
            # Default to MHz for center freq. value.
            if key == 'CFRQ/VALUE':
                value = value.strip('MmHhZz') + '000000'
            key = key.replace('/', ':')
            self._send('%s %s' % (key, value))
            test = self.get([key])[0]
            if key.find(':') < 0:
                regex = re.compile('[0-9]+\.[0-9]+;', re.IGNORECASE)
                match = regex.search(test)
                if match:
                    test = match.group()
                    tmp = value.replace('M', '000000').strip('HhZz')
                    result.append(
                        str(float(tmp) == float(test[:-1])))
                else:
                    result.append('False')
            else:
                tmp = value.replace('M', '000000').strip('HhZz')
                result.append(str(float(tmp) == float(test)))
        return result

    def set2(self, keys, values):
        """Basic set.

        Does not ensure that the value was set correctly, only that it is sent.
        """
        result = []
        for key, value in zip(keys, values):
            key = key.replace('/', ':')
            self._send('%s %s' % (key, value))
            result.append('True')
        return result

#AgentClass = SynthAgent
