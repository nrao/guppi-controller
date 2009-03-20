import re
from telnetconnection import TelnetConnection
from agent import Agent, index

class PowerstripAgent(Agent):
    def __init__(self, host='power_strip', port=None):
        self.__host = host
        self.__port = port
        self.__conn = TelnetConnection()
        self.__kwds = ['outlet/1', 'outlet/2', 'outlet/3', 'outlet/4',
                       'outlet/5', 'outlet/6', 'outlet/7', 'outlet/8'] #,
                       # 'group/ibobs'] # not ready yet

    def _open(self):
        self.__conn.open(self.__host, self.__port)
        self.__conn.write('guppi\r')
        self.__conn.write('guppi\r')
        self.__conn.read_until('iBootBar > ')
        # For some reason it eats the first character after this...
        # sending a non-whitespace character seems to fix it
        # (i.e., sending a space breaks the parsing on the box)
        self.__conn.write('\x08') # ASCII backspace

    def _close(self):
        self.__conn.close()


    def get(self, keys=index):
        self._open()
        result = []
        if keys == index:
            result += self.__kwds[:]
        else:
            for k in keys:
                response = self.__conn.roundtrip(
                    'get %s\r\n' % (' '.join(k.split('/'))), 'iBootBar > ')
                regex = re.compile('O(n|ff)\s{1,2}OK', re.I | re.M)
                # Hackage for group semantics
                #!!! Clean up
                if k.startswith('group'):
                    regex = re.compile('([N\s]+|[F\s]+)\s+OK', re.I | re.M)
                match = regex.search(response)
                if match:
                    if k.startswith('group'):
                        match = match.group().strip()
                        result.append({'N': 'On', 'F': 'Off'}[match[0]])
                    else:
                        result.append(match.group()[:-4])
                else:
                    result.append('Communication error')
        self._close()
        return result
                
    def set(self, keys, values):
        self._open()
        result = []
        if keys[0] and values[0] and len(keys) == len(values):
            for k, v in zip(keys, values):
                response = self.__conn.roundtrip(
                    'set %s %s\r\n' % (k.replace('/', ' '), v), 'iBootBar > ')
                regex = re.compile('O(n|ff)\s{1,2}OK', re.I | re.M)
                # Hackage for group semantics
                #!!! Clean up
                if k.startswith('group'):
                    regex = re.compile('OK', re.I | re.M)
                match = regex.search(response)
                if match:
                    if k.startswith('group'):
                        result.append('True')
                    else:
                        result.append(
                            str(match.group()[:-4].lower() == v.lower()))
                else:
                    result.append('Communication error')
        else:
            result.append('Key/value mismatch')
        self._close()
        return result
