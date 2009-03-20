from binascii import hexlify
import numpy
from time import sleep

try:
    from utility import generate_mask, xstr2float, float2xstr
except ImportError:
    from guppi.utility import generate_mask, xstr2float, float2xstr

def verbose_set(key, value):
    """Performs a set operation with formatted output."""
    print 'set', key, 'to', value, '...', set(key, value)
    
def init():
    """Initializes registers to their default values."""
    verbose_set('BEE2/FPGA1/FFT_SHIFT', 'aaaaaaaa')
    verbose_set('BEE2/FPGA1/LE_CNTRL', '00000000')
    verbose_set('BEE2/FPGA1/SAMP_CMD', '00000000')
    verbose_set('BEE2/FPGA1/DC_SAMP_EN', '00000001')
    verbose_set('BEE2/FPGA1/DC_BINS_EN', '00000001')
    
    verbose_set('BEE2/FPGA2/GUPPi_PIPES_ARM', '00000000')
    verbose_set('BEE2/FPGA2/OFFSET_I', '00000000')
    verbose_set('BEE2/FPGA2/OFFSET_Q', '00000000')
    verbose_set('BEE2/FPGA2/OFFSET_U', '00000000')
    verbose_set('BEE2/FPGA2/OFFSET_V', '00000000')
    verbose_set('BEE2/FPGA2/SCALE_I', '01000000')
    verbose_set('BEE2/FPGA2/SCALE_Q', '01000000')
    verbose_set('BEE2/FPGA2/SCALE_U', '01000000')
    verbose_set('BEE2/FPGA2/SCALE_V', '01000000')
    verbose_set('BEE2/FPGA2/ACC_LENGTH', '0000000f')
    verbose_set('BEE2/FPGA2/DEST_IP', 'c0a80307')
    verbose_set('BEE2/FPGA2/DEST_PORT', '0000c350')
    verbose_set('BEE2/FPGA2/DC_BINS_EN', '00000001')
    text = 'begin\nmac = 10:10:10:10:10:11\nip = 192.168.3.8\n' + \
           'gateway = 192.168.3.8\nport = 50000\nend\n'
    verbose_set('BEE2/FPGA2/ten_GbE', hexlify(text))
    print 'encoded from:\n%s' % text

    verbose_set('BEE2/FPGA3/FFT_SHIFT', 'aaaaaaaa')
    verbose_set('BEE2/FPGA3/LE_CNTRL', '00000000')
    verbose_set('BEE2/FPGA3/SAMP_CMD', '00000000')
    verbose_set('BEE2/FPGA3/DC_SAMP_EN', '00000001')
    verbose_set('BEE2/FPGA3/DC_BINS_EN', '00000001')

def reset(synth_freq = None, wait = 3):
    print 'bofs = unload()'
    bofs = unload()
    print 'unload(bofs)'
    unload(bofs)
    if synth_freq:
        verbose_set('SYNTH/CFRQ/VALUE', synth_freq)
    verbose_set('POWER/group/ibobs', 'Off')
    sleep(wait)
    verbose_set('POWER/group/ibobs', 'On')
    print 'load(bofs)'
    load(bofs)
    print 'init()'
    init()

def snapshot_bins(brams, limit = 512):
    bins = []
    count = 0
    while count < limit:
        bins.append(brams[0][count])
        bins.append(brams[1][count])
        bins.append(brams[2][count])
        bins.append(brams[3][count])
        count += 1
    return bins

def unbram(bram, value_nibbles = 2):
    """Breaks each bram word into the specified number of nibbles.
    Most GUPPI bram values are four 8-bit values concatenated.

    Keyword arguments:
    bram -- string of bram values to separate
    value_nibbles -- size of resulting values in nibbles
    """
    result = []
    for i in range(0, len(bram), value_nibbles):
        result += [bram[i:i+value_nibbles]]
    return result

def get_adc_samples(fpga=1, signed=True):
    """Retrieve raw ADC samples from the specified signal path.

    Keyword arguments:
    fpga -- FPGA number to get samples from
    signed -- whether to treat the values as signed or not
    """
    prefix = 'BEE2/FPGA%s/' % fpga
    # Note: These are not in actual time order yet
    vals = unbram(get(prefix + 'DC_HI_SAMP_BRAM'))
    vals += unbram(get(prefix + 'DC_LO_SAMP_BRAM'))
    vals = [int(v, 16) for v in vals]
    if signed: 
        vals = numpy.int8(vals)
    else:
        vals = numpy.uint8(vals)
    return vals

def print_reg():
    """Prints all registers and their current values.  Excludes BRAMs."""
    keys = [k for k in get()
            if k.startswith('BEE2')]
    for k in keys:
        v = get(k)
        if 0 < len(v) < 32:
            print k, '\t', v

try:
    import math
    import pylab
except:
    print 'Plotting functions are not available.'
else:
    print 'Plotting functions added successfully.'

    def plot(values, frac_bits = 0, sign_bit = None):
        toplot = []
        for v in values:
            toplot.append(xstr2float(v, frac_bits, sign_bit))
        print
        print 'plotting ...'
        print 'x\ty'
        print '----------'
        for i in range(len(toplot)):
            if toplot[i] != 0:
                print i, '\t', toplot[i]
        print '----------'
        pylab.plot(toplot)
        pylab.show()

    def plot_adc_hist(ngrab=1, refresh=True):
        d1 = numpy.ndarray(0, dtype=numpy.int8)
        d3 = numpy.ndarray(0, dtype=numpy.int8)
        for i in range(ngrab):
            if refresh: dum=get()
            d1 = numpy.append(d1, get_adc_samples(fpga=1,signed=True))
            d3 = numpy.append(d3, get_adc_samples(fpga=3,signed=True))
        (h1,x) = numpy.histogram(d1,bins=128,range=(-128,128),new=True)
        (h3,x) = numpy.histogram(d3,bins=128,range=(-128,128),new=True)
        s1 = [d1.mean(), d1.std(), d1.min(), d1.max()]
        s3 = [d3.mean(), d3.std(), d3.min(), d3.max()]
        target_rms = 20.0

        # Avoid the singularity.
        s1[1] = s1[1] or 0.0000000000001
        s3[1] = s3[1] or 0.0000000000001

        s1 = tuple(s1)
        s3 = tuple(s3)

        diff1 = 20.0*(math.log10(s1[1]) - math.log10(target_rms))
        diff3 = 20.0*(math.log10(s3[1]) - math.log10(target_rms))
        if (diff1 < 0.0):
            verb1 = 'Remove'
            diff1 = -1.0 * diff1
        else:
            verb1 = 'Add'
        if (diff3 < 0.0):
            verb3 = 'Remove'
            diff3 = -1.0 * diff3
        else:
            verb3 = 'Add'
        print 'FPGA1 (CM5): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s1
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb1, diff1, target_rms)
        print 'FPGA3 (CM1): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s3
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb3, diff3, target_rms)
        pylab.plot(x[1:]-0.5, h1, label='FPGA1')
        pylab.plot(x[1:]-0.5, h3, label='FPGA3')
        pylab.legend()
        pylab.show()

    def plot_iquv(iquv = 'IQUV'):
        """Plot the requested spectra.

        Keyword arguments:
        iquv -- one or more of 'I', 'Q', 'U', 'V' stokes parameters to plot;
                must be in alphabetic order.
        """
        bins = {}
        zeroes = []
        length = 0
        iquv = iquv.upper()
        reg_name = 'BEE2/FPGA2/vacc_subsys_%s_%s_%s_BRAM'
        for char in iquv:
            S_0, S_1, S_2, S_3 = (
                unbram(get([reg_name % (char, char, 0)])[0], 8),
                unbram(get([reg_name % (char, char, 1)])[0], 8),
                unbram(get([reg_name % (char, char, 2)])[0], 8),
                unbram(get([reg_name % (char, char, 3)])[0], 8)
                )
            bins[char] = snapshot_bins((S_0, S_1, S_2, S_3))
            length = len(bins[char])

        if length != 0:
            zeroes = ['0'*8 for i in xrange(length)]

        if 'I' in iquv:
            plot(bins.get('I', zeroes) + zeroes + zeroes + zeroes, 16, 32)
        if 'Q' in iquv:
            plot(zeroes + bins.get('Q', zeroes) + zeroes + zeroes, 16, 32)
        if 'U' in iquv:
            plot(zeroes + zeroes + bins.get('U', zeroes) + zeroes, 16, 32)
        if 'V' in iquv:
            plot(zeroes + zeroes + zeroes + bins.get('V', zeroes), 16, 32)
            
def scale_factor(pol,factor):
    """
    Change the scale factor for a polarization by the given (relative) amount.
    Valid pol values are I, Q, U, V
    """
    reg = "BEE2/FPGA2/SCALE_%s" % pol
    cur_val = int(get(reg),16)
    new_val = int(cur_val * factor)
    set([reg],['%08x' % new_val])

def increase_scales(factor=1.2):
    """
    Increase all scale params by a factor of 1.2
    """
    for pol in ('I','Q','U','V'):
        scale_factor(pol,factor)

def decrease_scales(factor=1.2):
    """
    Decrease all scale params by a factor of 1.2
    """
    for pol in ('I','Q','U','V'):
        scale_factor(pol,1.0/factor)
