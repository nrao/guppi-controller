# list script files in this directory to execute, in target order
# order counts!  make sure dependecies are met!

lineup = ['utils.py'
          # , 'one.py'
          # , 'two.py'
          ]

for script in lineup:
    try:
        # To do: guarantee proper path to current directory...
        #        scripts/ is probably not working directory
        execfile('scripts/%s' % script)
    except IOError:
        pass
