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

import re

# Prepare tab auto-completion for fuctions.
class Completer:
    '''Create a new completer for the command-line, for use with readline.

    This completer is specifically designed for guppi/cicada.
    This is based on inspiration/examples from Python built-in rlcompleter.
    '''

    def __init__(self):
        self.functions = []
        self.parameters = []
        self.profiles_a = []
        self.profiles_r = []
        self.matches = []

        self._syntax_noarg = ['function()']
        self.syntax = {}
        self.syntax[''] = ['function(parameter)']
        self.syntax['get'] = self._syntax_noarg + self.syntax['']
        self.syntax['set'] = ['function(parameter, value)']
        self.syntax['load'] = self._syntax_noarg + ['function(profile_a)']
        self.syntax['unload'] = self._syntax_noarg + ['function(profile_r)']

    def get_functions(self):
        '''Accessor for self.functions.

        Test usage:
        >>> c = Completer()
        >>> functions = ['one', 'two', 'three']
        >>> for function in functions:
        ...     c.register(function)
        >>> c.get_functions() == functions
        True
        >>> 
        '''
        return self.functions

    def get_syntax(self, function):
        '''Accessor for the registered syntax for a function. Returns [str].

        Test usage:
        >>> c = Completer()
        >>> c.register('one')
        >>> c.get_syntax('one')
        []
        >>> c.register('one', 'function(parameter)')
        >>> c.get_syntax('one')
        ['function(parameter)']
        >>> c.register('one', 'function(profile)')
        >>> c.get_syntax('one')
        ['function(parameter)', 'function(profile)']
        >>> 
        '''
        return self.syntax.get(function, [])

    def get_parameters(self):
        '''Accessor for parameters.

        Test usage:
        >>> c = Completer()
        >>> c.get_parameters()
        []
        >>> c.set_parameters(['a', 'bb', 'ccc'])
        >>> c.get_parameters()
        ['a', 'bb', 'ccc']
        >>> 
        '''
        return self.parameters

    def set_parameters(self, parameters):
        '''Accessor for parameters.
        '''
        self.parameters = parameters

    def get_profiles_a(self):
        '''Accessor for available profiles.

        Test usage:
        >>> c = Completer()
        >>> c.get_profiles_a()
        []
        >>> c.set_profiles_a(['a', 'bb', 'ccc'])
        >>> c.get_profiles_a()
        ['a', 'bb', 'ccc']
        >>> 
        '''
        return self.profiles_a

    def set_profiles_a(self, profiles):
        '''Accessor for available profiles.
        '''
        self.profiles_a = profiles

    def get_profiles_r(self):
        '''Accessor for running profiles.

        Test usage:
        >>> c = Completer()
        >>> c.get_profiles_r()
        []
        >>> c.set_profiles_r(['d', 'ee', 'fff'])
        >>> c.get_profiles_r()
        ['d', 'ee', 'fff']
        >>> 
        '''
        return self.profiles_r

    def set_profiles_r(self, profiles):
        '''Accessor for running profiles.
        '''
        self.profiles_r = profiles

    def get_profiles(self):
        '''Accessor for all profiles.

        Test usage:
        >>> c = Completer()
        >>> c.get_profiles()
        ([], [])
        >>> c.set_profiles_a(['a', 'bb', 'ccc'])
        >>> c.get_profiles()
        (['a', 'bb', 'ccc'], [])
        >>> c.set_profiles_r(['d', 'ee', 'fff'])
        >>> c.get_profiles()
        (['a', 'bb', 'ccc'], ['d', 'ee', 'fff'])
        >>> c.set_profiles(c.get_profiles_r(), c.get_profiles_a())
        >>> c.get_profiles()
        (['d', 'ee', 'fff'], ['a', 'bb', 'ccc'])
        >>> 
        '''
        return self.profiles_a, self.profiles_r

    def set_profiles(self, available, running):
        '''Accessor for all profiles.
        '''
        self.profiles_a = available
        self.profiles_r = running

    def register(self, function, syntax = None):
        '''Register function for completion. Optionally provide syntax.
        If no syntax is provided, completion will guess a default.

        Test usage:
        >>> # Test setup:
        >>> c = Completer()
        >>> c.get_functions()
        []
        >>> c.register('one')
        >>> c.get_functions()
        ['one']
        >>> c.register('two', 'function()')
        >>> c.get_functions()
        ['one', 'two']
        >>> c.get_syntax('two')
        ['function()']
        >>> c.get_syntax('one')
        []
        >>> c.register('two', 'function(parameter)')
        >>> c.get_syntax('two')
        ['function()', 'function(parameter)']
        >>> c.get_syntax('one')
        []
        >>> c.register('one', 'function()')
        >>> c.get_syntax('one')
        ['function()']
        >>> # Note that duplicate syntax doesn't show up.
        >>> c.register('one', 'function()')
        >>> c.get_syntax('one')
        ['function()']
        >>> 
        '''
        if function not in self.functions:
            self.functions.append(function)

        if syntax:
            formats = self.get_syntax(function)
            if syntax not in formats:
                formats.append(syntax)
            self.syntax[function] = formats

    def unregister(self, function):
        '''Remove a function and its known syntax from completion.

        Test usage:
        >>> # Test setup:
        >>> c = Completer()
        >>> c.register('one')
        >>> c.get_functions()
        ['one']
        >>> c.register('two', 'function()')
        >>> c.get_functions()
        ['one', 'two']
        >>> c.get_syntax('two')
        ['function()']
        >>> c.unregister('two')
        >>> c.get_syntax('two')
        []
        >>> c.get_functions()
        ['one']
        >>> c.register('two')
        >>> c.get_functions()
        ['one', 'two']
        >>> c.get_syntax('two')
        []
        >>> c.unregister('two')
        >>> c.get_syntax('two')
        []
        >>> c.get_functions()
        ['one']
        >>> c.unregister('one')
        >>> c.get_functions()
        []
        >>> 
        '''
        self.functions.remove(function)
        self.syntax.pop(function, None)

    def noarg(self, function):
        '''Specifies function as accepting no arguments, plus previous syntax.

        Test usage:
        >>> c = Completer()
        >>> c.register('one')
        >>> c.get_syntax('one')
        []
        >>> c.noarg('one')
        >>> c.get_syntax('one')
        ['function()']
        >>> c.register('two', 'function(parameter)')
        >>> c.get_syntax('two')
        ['function(parameter)']
        >>> c.noarg('two')
        >>> c.get_syntax('two')
        ['function(parameter)', 'function()']
        '''
        for syntax in self._syntax_noarg:
            self.register(function, syntax)

    def accept(self, namespace):
        '''Accepts a namespace of functions for completion. Assumes no syntax.
        '''
        pass

    def ignore(self, function):
        pass

    # def ignore namespace?

    def parameter_matches(self, text):
        '''Returns a list of parameters matching text to be completed.

        Test usage:
        >>> c = Completer()
        >>> parameters = ['ay', 'bee', 'cee', 'alphabet']
        >>> c.set_parameters(parameters)
        >>> c.parameter_matches('a')
        ['ay', 'alphabet']
        >>> c.parameter_matches('al')
        ['alphabet']
        >>> 
        '''
        return [p for p in self.get_parameters() if p.startswith(text)]

    def function_matches(self, text):
        '''Returns a list of functions matching text to be completed.

        Test usage:
        >>> c = Completer()
        >>> functions = ['one', 'two', 'three']
        >>> for function in functions:
        ...     c.register(function)
        >>> c.function_matches('t')
        ['two', 'three']
        >>> c.function_matches('tw')
        ['two']
        >>> 
        '''
        return [f for f in self.get_functions() if f.startswith(text)]

    def complete(self, text, state):
        '''Return the next possible completion for 'text'.
        This is the method to be used with readline.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with text.
        '''
        if state == 0:
            if '(' not in text:
                self.matches = self.function_matches(text)
            else:
                function, blob = text.split('(', maxsplit = 1)

                formats = self.get_syntax(function)
                if not formats:
                    self.matches = [function]

                for syntax in formats:
                    blob


                # Determine quote character and start of argument.
                
                
        try:
            return self.matches[state]
        except IndexError:
            return None


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

    def one(x = None):
        if not x:
            print 'function one'
        else:
            print x

    def two(x = None):
        if not x:
            print 'function two'
        else:
            print x * 2

    completer = Completer()
    completer.register('one')
    completer.register('two')
    import readline
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
