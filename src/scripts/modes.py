# modes.py - utils for loading sets of bof files
import sys

# XAUI alignment bof is used in all cases
guppi_xal_bof = 'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof'

# These bofs are common to all coherent modes
# NOTE: updated to non-ARP-spam versions 2013/02/04 PBD
guppi2_common_bofs = [
        'BEE2/bGOUT_U2_1SFA_CoDD_P10_fpga2_2013_Jan_17_1600.bof',
        guppi_xal_bof
        ]

# DSP bofs can be used in either coherent or incoherent modes
# NOTE: updated to match Guppi.conf 2011/06/29 PBD
guppi_dsp_bofs = {
        '32': [
            'BEE2/bGDSP_U1_0032_T12_W095_fpga1_2010_Aug_02_1026.bof',
            'BEE2/bGDSP_U3_0032_T12_W095_fpga3_2010_Aug_02_1046.bof'
            ],
        '64': [
            'BEE2/bGDSP_U1_0064_T12_W095_fpga1_2010_Aug_02_1200.bof',
            'BEE2/bGDSP_U3_0064_T12_W095_fpga3_2010_Aug_02_1226.bof'
            ],
        '128': [
            'BEE2/bGDSP_U1_0128_T12_W095_fpga1_2010_Feb_16_1424.bof',
            'BEE2/bGDSP_U3_0128_T12_W095_fpga3_2010_Feb_16_1517.bof'
            ],
        '256': [
            'BEE2/bGDSP_U1_0256_T12_W095_fpga1_2010_Aug_02_1327.bof',
            'BEE2/bGDSP_U3_0256_T12_W095_fpga3_2010_Aug_02_1347.bof'
            ],
        '512': [
            'BEE2/bGDSP_U1_0512_1248_P01_fpga1_2009_Dec_31_1616.bof',
            'BEE2/bGDSP_U3_0512_1248_P01_fpga3_2009_Dec_31_1616.bof'
            ],
        '512_12T': [
            'BEE2/bGDSP_U1_0512_T12_W095_fpga1_2010_Aug_02_1457.bof',
            'BEE2/bGDSP_U3_0512_T12_W095_fpga3_2010_Aug_02_1518.bof'
            ],
        '1024': [
            'BEE2/bGDSP_U1_1024_T12_W095_fpga1_2010_Aug_03_0953.bof',
            'BEE2/bGDSP_U3_1024_T12_W095_fpga3_2010_Aug_03_1016.bof'
            ],
        '2048': [
            'BEE2/bGDSP_U1_2048_1248_P00_fpga1_2009_Jun_03_1645.bof',
            'BEE2/bGDSP_U3_2048_1248_P00_fpga3_2009_Jun_03_1725.bof'
            ]
        }

# The list of GUPPI modes
# NOTE, the guppi1 DSP blocks have been left at revision P00 until
# we verify any timing offsets between P00 and later revs.  Jumps
# could be due to the fixed PFB issue, as well as different PFB
# filter lengths.  Once this is fixed, we can use the guppi_dsp_bofs
# list.
guppi_modelist = {
        'old2048': [
            'BEE2/b2_GOUT_U2_4K_800_A_NR_fpga2_2008_Sep_15_1400.bof',
            'BEE2/b2_GDSP_U1_4K_800_A_XA_fpga1_2008_Jul_30_1356.bof',
            'BEE2/b2_GDSP_U3_4K_800_A_XA_fpga3_2008_Jul_30_1414.bof'
            ],
        '32': [
            'BEE2/bGOUT_U2_0032_1SFA_P00_fpga2_2010_Feb_12_1237.bof',
            guppi_xal_bof
            ] + guppi_dsp_bofs['32'],
        '64': [
            'BEE2/bGOUT_U2_0064_1SFA_P00_fpga2_2010_Jan_14_1153.bof',
            guppi_xal_bof
            ] + guppi_dsp_bofs['64'],
        '128': [
            'BEE2/bGOUT_U2_0128_1SFA_P00_fpga2_2009_May_14_1515.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_0128_1248_P00_fpga1_2009_Dec_17_1302.bof',
            'BEE2/bGDSP_U3_0128_1248_P00_fpga3_2009_Dec_17_1303.bof'
            ],
        '256': [
            'BEE2/bGOUT_U2_0256_1SFA_P00_fpga2_2013_Jan_18_0837.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_0256_1248_P00_fpga1_2009_Jul_07_1057.bof',
            'BEE2/bGDSP_U3_0256_1248_P00_fpga3_2009_Jul_07_1129.bof'
            ],
        '512': [
            'BEE2/bGOUT_U2_0512_1SFA_P00_fpga2_2013_Jan_18_0840.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_0512_1248_P00_fpga1_2009_Jul_07_0710.bof',
            'BEE2/bGDSP_U3_0512_1248_P00_fpga3_2009_Jul_07_0746.bof'
            ],
        '1024': [
            'BEE2/bGOUT_U2_1024_1SFA_P00_fpga2_2013_Jan_18_0853.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_1024_1248_P00_fpga1_2009_Jul_06_1330.bof',
            'BEE2/bGDSP_U3_1024_1248_P00_fpga3_2009_Jul_06_1408.bof'
            ],
        '2048': [
            'BEE2/bGOUT_U2_2048_1SFA_P00_fpga2_2013_Jan_18_0905.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_2048_1248_P00_fpga1_2009_Jun_03_1645.bof',
            'BEE2/bGDSP_U3_2048_1248_P00_fpga3_2009_Jun_03_1725.bof'
            ],
        '4096': [
            'BEE2/bGOUT_U2_4096_1SFA_P00_fpga2_2013_Jan_18_0908.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_4096_1248_P00_fpga1_2009_Jul_06_0847.bof',
            'BEE2/bGDSP_U3_4096_1248_P00_fpga3_2009_Jul_06_0929.bof'
            ],
        'fast4k': [
            'BEE2/bGOUT_U2_4096_1SFA_P01_fpga2_2013_Jan_18_0824.bof',
            guppi_xal_bof,
            'BEE2/bGDSP_U1_4096_1248_P00_fpga1_2009_Jul_06_0847.bof', 
            'BEE2/bGDSP_U3_4096_1248_P00_fpga3_2009_Jul_06_0929.bof' 
            ],
        'bbdump': [
            'BEE2/bGDSP_U1_0001_1248_P00_fpga1_2010_May_25_1420.bof', 
            'BEE2/bGDSP_U3_0001_1248_P00_fpga3_2010_May_25_1410.bof', 
            'BEE2/bGXAL_U4_XXXX_1SFA_P00_fpga4_2009_Jun_15_1455.bof', 
            'BEE2/bGOUT_U2_1SFA_TDOM_P02_fpga2_2010_Jul_07_1724.bof'
            ],
        'c32':   guppi2_common_bofs + guppi_dsp_bofs['32'],
        'c64':   guppi2_common_bofs + guppi_dsp_bofs['64'],
        'c128':  guppi2_common_bofs + guppi_dsp_bofs['128'],
        'c256':  guppi2_common_bofs + guppi_dsp_bofs['256'],
        'c512':  guppi2_common_bofs + guppi_dsp_bofs['512_12T'],
        'c1024': guppi2_common_bofs + guppi_dsp_bofs['1024'],
        'c2048': guppi2_common_bofs + guppi_dsp_bofs['2048']
        }

def mode(modename="none"):
    """Load a GUPPI hardware mode (set of bof files) from a predefined list."""

    # If no arg was given, print list of choices, and currently loaded
    if modename == "none":
        print "Current mode: ", get_mode()
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

def get_mode():
    """Tries to determine what GUPPI HW mode (bof set) is currently loaded."""

    # Read currently loaded bofs
    bofs = unload()

    # Special return codes
    mode_none = 'None'
    mode_unk = 'Unknown'

    # If nothing is loaded..
    if len(bofs)==0: return mode_none

    # All current modes have 4 bofs
    if len(bofs)!=4: return mode_unk

    # Match set with modelist
    for modename in guppi_modelist.keys():
        if sorted(bofs) == sorted(guppi_modelist[modename]):
            return modename

    # Nothing matched, return unknown
    return mode_unk

