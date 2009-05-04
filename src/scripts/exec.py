# list script files in this directory to execute, in target order
# order counts!  make sure dependecies are met!

import os

lineup = ('utils.py',
          'modes.py',
          )

for script in lineup:
    try:
        thisdir = os.path.dirname(os.path.abspath(__file__))
        execfile(thisdir + '/' + '%s' % script)
    except IOError:
        try:
            thisdir = os.path.dirname(os.path.abspath(__file__))
            execfile(thisdir + '/scripts' + '/' + '%s' % script)
        except IOError:
            pass
