from telnetconnection import TelnetConnection

class PowerBarClient:
    def __init__(self, host, port=None):
        self.__conn = TelnetConnection(host, port)
        self.__conn.write('guppi\r')
        self.__conn.write('guppi\r')
        self.__conn.read_until('iBootBar > ')
        # For some reason it eats the first character after this...
        # sending a non-whitespace character seems to fix it
        # (i.e., sending a space breaks the parsing on the box)
        self.__conn.write('\x08') # ASCII backspace
        self.__kwds = ['outlet/1', 'outlet/2', 'outlet/3', 'outlet/4',
                       'outlet/5', 'outlet/6', 'outlet/7', 'outlet/8',]

    def get(self, keys=[]):
        result = []
        if keys == []:
            result = self.__kwds[:]
        else:
            for k in keys:
                response = self.__conn.roundtrip(
                    'get %s\r\n' % (' '.join(k.split('/'))), 'iBootBar > ')
                #!!! Parse feedback and add to results
                result.append(
                    str(response.find(k.replace('/', '')[1:]+' On') > 0))
        return result
                
    def set(self, keys, values):
        result = []
        if keys[0] and values[0] and len(keys) == len(values):
            for k, v in zip(keys, values):
                response = self.__conn.roundtrip('set %s %s\r\n' % ( 
                        k.replace('/', ' '), v), 'iBootBar > ')
                result.append(
                    str(response.find('OK\r\niBootBar') > 0))
        else:
            result.append('Key/value mismatch')
        return result
        
