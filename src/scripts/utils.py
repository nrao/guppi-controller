from binascii import hexlify
import math, numpy
from time import sleep

try:
    from utility import generate_mask, xstr2float, float2xstr
except ImportError:
    from guppi.utility import generate_mask, xstr2float, float2xstr

def verbose_set(key, value):
    """Performs a set operation with formatted output."""
    print 'set', key, 'to', value, '...', set(key, value)
    
def init(mode="1sfa"):
    """Initializes registers to their default values."""

    # If we're in coherent mode, run init2() instead
    if get_coherent(): return init2()

    # FPGAs 1 and 3 always have the same settings
    for fpga in ["FPGA1", "FPGA3"]:
        verbose_set('BEE2/%s/FFT_SHIFT' % fpga, 'aaaaaaaa')
        if mode == "1sfa":
            verbose_set('BEE2/%s/DC_EN' % fpga, '00000001')
        else:
            verbose_set('BEE2/%s/LE_CNTRL' % fpga, '00000000')
            verbose_set('BEE2/%s/SAMP_CMD' % fpga, '00000000')
            verbose_set('BEE2/%s/DC_SAMP_EN' % fpga, '00000001')
            verbose_set('BEE2/%s/DC_BINS_EN' % fpga, '00000001')
        
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
    verbose_set('BEE2/FPGA2/DEST_IP', '0a110007')
    verbose_set('BEE2/FPGA2/DEST_PORT', '0000c350')
    verbose_set('BEE2/FPGA2/DC_BINS_EN', '00000001')
    if mode == "1sfa":
        bw = get('SYNTH/CFRQ/VALUE')
        bw_sel = '0'
        guppi_pipes_bw_sel = '2'
        if bw == '800MHz':
            bw_sel = '1'
        if bw == '400MHz':
            guppi_pipes_bw_sel = '1'
        verbose_set('BEE2/FPGA2/GUPPi_PIPES_BW_SEL', guppi_pipes_bw_sel)
        verbose_set('BEE2/FPGA2/BW_SEL', bw_sel)
        verbose_set('BEE2/FPGA2/ROL_SEL', '0')
    text = 'begin\nmac = 10:10:10:10:10:11\nip = 10.17.0.8\n' + \
           'gateway = 10.17.0.8\nport = 50000\nend\n'
    verbose_set('BEE2/FPGA2/ten_GbE', hexlify(text))
    print 'encoded from:\n%s' % text

def get_nchan():
    """Determine number of channels from FPGA1/3 bof names."""
    # Note this assumes bof names have structure like:
    #   BEE2/bGDSP_U1_2048_1248_P00_fpga1_2009_Jun_03_1645.bof
    nchan1 = ''
    nchan3 = ''
    for bof in unload():
        (fpga, nchan) = bof.split('_')[1:3]
        if fpga=='U1': nchan1=nchan
        if fpga=='U3': nchan3=nchan
    if nchan1==nchan3: return int(nchan1)
    else: return 0

def get_coherent():
    """Determine if coherent dedispersion mode is loaded."""
    # Looks for the string 'CoDD' to be present somewhere.
    for bof in unload():
        if bof.find('CoDD') > 0: return True
    return False

def init2():
    """Initializes FPGA registers for coherent (guppi2) modes"""

    for fpga in ["FPGA1", "FPGA3"]:
        verbose_set('BEE2/%s/FFT_SHIFT' % fpga, 'aaaaaaaa')
        verbose_set('BEE2/%s/DC_EN' % fpga, '00000001')

    # NOTE: bw_sel=2 only applies for 100, 200 and 800 MHz
    verbose_set('BEE2/FPGA2/GUPPi_PIPES_ARM',    '00000000')
    verbose_set('BEE2/FPGA2/GUPPi_PIPES_BW_SEL', '00000002')

    verbose_set('BEE2/FPGA2/SCALE_P0', '00200000')
    verbose_set('BEE2/FPGA2/SCALE_P1', '00200000')

    # Figure out nchan from bof names
    nchan = get_nchan()
    if nchan>0:
        log2nchan = int(math.log(float(nchan))/math.log(2))
        verbose_set('BEE2/FPGA2/N_CHAN', '%x' % log2nchan)
    else:
        # don't know nchan, set it to 7 (128 chans)
        print "Warning: N_CHAN could not be determined! Assuming 128 channels."
        verbose_set('BEE2/FPGA2/N_CHAN', '00000007')

    # Set BEE2's 10gig IP addresses
    for ip in range(4):
        text = ('begin\nmac = 10:10:10:10:10:%02x\nip = 10.17.0.%d\n' + \
               'gateway = 10.17.0.7\nport = 50000\nend\n') % \
               (16+ip, 20+ip)
        reg = 'BEE2/FPGA2/4_X_10Ge_10Ge_%d_ten_GbE' % ip
        print "Setting %s to:" % reg
        print text
        print "  ...",  set(reg, hexlify(text))

    # Set destination IPs/ports, currently gpu1-8
    for ip in range(8):
        verbose_set('BEE2/FPGA2/IP_%d' % ip, 
                '%02x%02x%02x%02x' % (10,17,0,101+ip))
        verbose_set('BEE2/FPGA2/PT_%d' % ip, '%08x' % 50000)

def reset(synth_freq=None, wait=3):
    """Reset guppi's synthesizer to the frequency given in MHz."""
    # Allow synth_freq to be None
    synth_freq = synth_freq or "0" # clean out False, None
    synth_freq = str(synth_freq)   # ensure is string

    freq_check = float(synth_freq.strip('MmHhZz'))
    if freq_check > 1000000:
        print 'usage: reset(synth_freq)'
        print 'synth_freq should be given in MHz'
        print 'did you mean to provide', freq_check / 1000000, '??'
        return

    if synth_freq and synth_freq != "0":
        verbose_set('SYNTH/CFRQ/VALUE', synth_freq)
    print 'power_cycle()'
    power_cycle()
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

def get_adc_samples(fpga=1, signed=True, fix_count=True):
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

    if fix_count:
        vals32 = unbram(get(prefix + 'DC_HI_SAMP_BRAM'),8)
        vals32 += unbram(get(prefix + 'DC_LO_SAMP_BRAM'),8)
        vals32 = [int(v, 16) for v in vals32]
        for i in range(len(vals32)):
            vals32[i] &= 0xFFFFFFF0  # Kill 4-bit counter
            vals32[i] >>= 3
            vals[4*i] = vals32[i] & 0xFF
            vals32[i] >>= 7
            vals[4*i+1] = vals32[i] & 0xFE
            vals32[i] >>= 7
            vals[4*i+2] = vals32[i] & 0xFE
            vals32[i] >>= 7
            vals[4*i+3] = vals32[i] & 0xFE

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

def set_acc_len(acc_len):
    """Sets ACC_LENGTH properly given the integer number of spectra to be summed."""
    verbose_set('BEE2/FPGA2/ACC_LENGTH', '%x'%(int(acc_len)-1))

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

    def plot_4_chan_adc_hist(ngrab=1, refresh=True):
        if get('BEE2/FPGA1/DESIGN_ID') != 'Error':
            fix_count=True
        else:
            fix_count=False
        d1h = numpy.ndarray(0, dtype=numpy.int8)
        d3h = numpy.ndarray(0, dtype=numpy.int8)
        d1l = numpy.ndarray(0, dtype=numpy.int8)
        d3l = numpy.ndarray(0, dtype=numpy.int8)
        for i in range(ngrab):
            if refresh: dum=get()
            fpgavals=[]
            fpgalowvals=[]
            fpgahighvals=[]
            fpgavals = get_adc_samples(fpga=1,signed=True,fix_count=fix_count)
            fpgalowvals = fpgavals[0:len(fpgavals)/2]
            fpgahighvals = fpgavals[len(fpgavals)/2:len(fpgavals)] 
            d1h = numpy.append(d1h, fpgahighvals)
            d1l = numpy.append(d1l, fpgalowvals)

            fpgavals = get_adc_samples(fpga=3,signed=True,fix_count=fix_count)
            fpgalowvals = fpgavals[0:len(fpgavals)/2]
            fpgahighvals = fpgavals[len(fpgavals)/2:len(fpgavals)] 
            d3h = numpy.append(d3h,fpgahighvals)
            d3l = numpy.append(d3l,fpgalowvals)

        (h1h,x) = numpy.histogram(d1h,bins=128,range=(-128,128))
        (h1l,x) = numpy.histogram(d1l,bins=128,range=(-128,128))
        (h3h,x) = numpy.histogram(d3h,bins=128,range=(-128,128))
        (h3l,x) = numpy.histogram(d3l,bins=128,range=(-128,128))
        s1h = [d1h.mean(), d1h.std(), d1h.min(), d1h.max()]
        s1l = [d1l.mean(), d1l.std(), d1l.min(), d1l.max()]
        s3h = [d3h.mean(), d3h.std(), d3h.min(), d3h.max()]
        s3l = [d3l.mean(), d3l.std(), d3l.min(), d3l.max()]
        target_rms = 20.0

        # Avoid the singularity.
        s1h[1] = s1h[1] or 0.0000000000001
        s3h[1] = s3h[1] or 0.0000000000001
        s1l[1] = s1l[1] or 0.0000000000001
        s3l[1] = s3l[1] or 0.0000000000001

        s1h = tuple(s1h)
        s3h = tuple(s3h)
        s1l = tuple(s1l)
        s3l = tuple(s3l)

        diff1h = 20.0*(math.log10(s1h[1]) - math.log10(target_rms))
        diff3h = 20.0*(math.log10(s3h[1]) - math.log10(target_rms))

        diff1l = 20.0*(math.log10(s1l[1]) - math.log10(target_rms))
        diff3l = 20.0*(math.log10(s3l[1]) - math.log10(target_rms))

        if (diff1h < 0.0):
            verb1h = 'Remove'
            diff1h = -1.0 * diff1h
        else:
            verb1h = 'Add'
        if (diff3h < 0.0):
            verb3h = 'Remove'
            diff3h = -1.0 * diff3h
        else:
            verb3h = 'Add'

        print 'CM4 (FPGA3, main): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s3h
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb3h, diff3h, target_rms)
        print 'CM8 (FPGA1,main ): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s1h
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb1h, diff1h, target_rms)

        if (diff1l < 0.0):
            verb1l = 'Remove'
            diff1l = -1.0 * diff1l
        else:
            verb1l = 'Add'
        if (diff3l < 0.0):
            verb3l = 'Remove'
            diff3l = -1.0 * diff3l
        else:
            verb3l = 'Add'
        print 'RFI1 (FPGA3, aux): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s3l
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb3l, diff3l, target_rms)
        print 'RFI2 (FPGA1, aux): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s1l
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb1l, diff1l, target_rms)

        pylab.plot(x[1:]-0.5, h1h, label='FPGA1-main')
        pylab.plot(x[1:]-0.5, h3h, label='FPGA3-main')
        pylab.plot(x[1:]-0.5, h1l, label='FPGA1-aux')
        pylab.plot(x[1:]-0.5, h3l, label='FPGA3-aux')
        pylab.legend()
        pylab.show()


    def plot_adc_hist(ngrab=1, refresh=True):
        if get('BEE2/FPGA1/DESIGN_ID') != 'Error':
            fix_count=True
        else:
            fix_count=False
        d1 = numpy.ndarray(0, dtype=numpy.int8)
        d3 = numpy.ndarray(0, dtype=numpy.int8)
        for i in range(ngrab):
            if refresh: dum=get()
            d1 = numpy.append(d1, get_adc_samples(fpga=1,signed=True,fix_count=fix_count))
            d3 = numpy.append(d3, get_adc_samples(fpga=3,signed=True,fix_count=fix_count))
        (h1,x) = numpy.histogram(d1,bins=128,range=(-128,128))
        (h3,x) = numpy.histogram(d3,bins=128,range=(-128,128))
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
        print 'CM4 (FPGA3): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s3
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb3, diff3, target_rms)
        print 'CM8 (FPGA1): Mean=%.3f RMS=%.3f Min=%d Max=%d' % s1
        print '       %s %.1f dB attenuation (for target RMS %.1f)' \
                % (verb1, diff1, target_rms)
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
