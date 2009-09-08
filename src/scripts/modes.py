# modes.py - utils for loading sets of bof files
import sys

# The list of GUPPI modes
guppi_modelist = {
        'old2048': [
            'BEE2/b2_GOUT_U2_4K_800_A_NR_fpga2_2008_Sep_15_1400.bof',
            'BEE2/b2_GDSP_U1_4K_800_A_XA_fpga1_2008_Jul_30_1356.bof',
            'BEE2/b2_GDSP_U3_4K_800_A_XA_fpga3_2008_Jul_30_1414.bof'
            ],
        '128': [
            'BEE2/bGOUT_U2_256_1SFA_D26_fpga2_2009_Apr_21_1155.bof',
            'BEE2/bGDSP_U1_256_1248_D20_fpga1_2009_Apr_14_2030.bof',
            'BEE2/bGDSP_U3_256_1248_D20_fpga3_2009_Apr_14_2111.bof'
            ],
        '256': [
            'BEE2/bGOUT_U2_0256_1SFA_P00_fpga2_2009_Jul_07_0843.bof',
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof',
            'BEE2/bGDSP_U1_0256_1248_P00_fpga1_2009_Jul_07_1057.bof',
            'BEE2/bGDSP_U3_0256_1248_P00_fpga3_2009_Jul_07_1129.bof'
            ],
        '512': [
            'BEE2/bGOUT_U2_0512_1SFA_P00_fpga2_2009_Jul_06_1540.bof',
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof',
            'BEE2/bGDSP_U1_0512_1248_P00_fpga1_2009_Jul_07_0710.bof',
            'BEE2/bGDSP_U3_0512_1248_P00_fpga3_2009_Jul_07_0746.bof'
            ],
        '1024': [
            'BEE2/bGOUT_U2_1024_1SFA_P00_fpga2_2009_Jul_06_1118.bof',
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof',
            'BEE2/bGDSP_U1_1024_1248_P00_fpga1_2009_Jul_06_1330.bof',
            'BEE2/bGDSP_U3_1024_1248_P00_fpga3_2009_Jul_06_1408.bof'
            ],
        '2048': [
            'BEE2/bGOUT_U2_2048_1SFA_P00_fpga2_2009_Jun_04_1032.bof',
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof',
            'BEE2/bGDSP_U1_2048_1248_P00_fpga1_2009_Jun_03_1645.bof',
            'BEE2/bGDSP_U3_2048_1248_P00_fpga3_2009_Jun_03_1725.bof'
            ],
        '4096': [
            'BEE2/bGOUT_U2_4096_1SFA_P00_fpga2_2009_Jul_14_0927.bof',
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof',
            'BEE2/bGDSP_U1_4096_1248_P00_fpga1_2009_Jul_06_0847.bof',
            'BEE2/bGDSP_U3_4096_1248_P00_fpga3_2009_Jul_06_0929.bof'
            ],
        'fast4k': [
            'BEE2/bGOUT_U2_4096_1SFA_P01_fpga2_2009_Sep_03_1003.bof',
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof', 
            'BEE2/bGDSP_U1_4096_1248_P00_fpga1_2009_Jul_06_0847.bof', 
            'BEE2/bGDSP_U3_4096_1248_P00_fpga3_2009_Jul_06_0929.bof' 
            ]
        }

def mode(modename="none"):
    """Load a GUPPI hardware mode (set of bof files) from a predefined list."""

    # If no arg was given, print list of choices
    if modename == "none":
        print "Valid modes: ", guppi_modelist.keys()
        return 

    # Check if modename is valid
    if not modename in guppi_modelist:
        print "Unknown mode: '%s'" % modename
        print "Valid choices: ", guppi_modelist.keys()
        return 

    # Print what bofs we're about to load
    print "Mode '%s':" % modename
    for b in guppi_modelist[modename]:
        print b

    # Unload currently running bofs
    print "Unloading current mode: ", 
    sys.stdout.flush()
    print unload(unload())

    # Load new set
    print "Loading '%s' mode: " % modename, 
    sys.stdout.flush()
    print load(guppi_modelist[modename])

