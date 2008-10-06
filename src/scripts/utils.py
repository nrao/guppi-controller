from binascii import hexlify
import numpy


def verbose_set(key, value):
    """Performs a set operation with formatted output."""
    print 'set', key, 'to', value, '...', set(key, value)

    
def init():
    """Initializes registers to their default values."""
    verbose_set(['BEE2/FPGA1/FFT_SHIFT'], ['aaaaaaaa'])
    verbose_set(['BEE2/FPGA1/LE_CNTRL'], ['00000000'])
    verbose_set(['BEE2/FPGA1/SAMP_CMD'], ['00000000'])
    verbose_set(['BEE2/FPGA1/DC_SAMP_EN'], ['00000001'])
    verbose_set(['BEE2/FPGA1/DC_BINS_EN'], ['00000001'])
    
    verbose_set(['BEE2/FPGA2/GUPPi_PIPES_ARM'], ['00000000'])
    verbose_set(['BEE2/FPGA2/OFFSET_I'], ['00000000'])
    verbose_set(['BEE2/FPGA2/OFFSET_Q'], ['00000000'])
    verbose_set(['BEE2/FPGA2/OFFSET_U'], ['00000000'])
    verbose_set(['BEE2/FPGA2/OFFSET_V'], ['00000000'])
    verbose_set(['BEE2/FPGA2/SCALE_I'], ['00010000'])
    verbose_set(['BEE2/FPGA2/SCALE_Q'], ['00010000'])
    verbose_set(['BEE2/FPGA2/SCALE_U'], ['00010000'])
    verbose_set(['BEE2/FPGA2/SCALE_V'], ['00010000'])
    verbose_set(['BEE2/FPGA2/ACC_LENGTH'], ['0000000f'])
    verbose_set(['BEE2/FPGA2/DEST_IP'], ['c0a80307'])
    verbose_set(['BEE2/FPGA2/DEST_PORT'], ['0000c350'])
    verbose_set(['BEE2/FPGA2/DC_BINS_EN'], ['00000001'])
    text = 'begin\nmac = 10:10:10:10:10:11\nip = 192.168.3.8\n' + \
           'gateway = 192.168.3.8\nport = 50000\nend'
    verbose_set(['BEE2/FPGA2/ten_GbE'], [hexlify(text)])
    
    verbose_set(['BEE2/FPGA3/FFT_SHIFT'], ['aaaaaaaa'])
    verbose_set(['BEE2/FPGA3/LE_CNTRL'], ['00000000'])
    verbose_set(['BEE2/FPGA3/SAMP_CMD'], ['00000000'])
    verbose_set(['BEE2/FPGA3/DC_SAMP_EN'], ['00000001'])
    verbose_set(['BEE2/FPGA3/DC_BINS_EN'], ['00000001'])


def unbram(bram, value_nibbles=2):
    """Breaks each bram word into the specified number of nibbles.

    Most GUPPI bram values are four 8-bit values concatenated.

    Keyword arguments:
    bram -- sequence of bram values to separate
    value_nibbles -- size of resulting values in nibbles
    """
    result = []
    for word in bram:
        temp = word
        while len(temp) > value_nibbles:
            head = temp[0:value_nibbles]
            result += [head]
            temp = temp[value_nibbles:]
        result += [temp]
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


try:
    import math
    import pylab
except:
    print 'Plotting functions are not available.'
else:
    print 'Plotting functions added successfully.'

    def plot_adc_hist(ngrab=1):
        d1 = numpy.ndarray(0, dtype=numpy.int8)
        d3 = numpy.ndarray(0, dtype=numpy.int8)
        for i in range(ngrab):
            d1 = numpy.append(d1, get_adc_samples(fpga=1,signed=True))
            d3 = numpy.append(d3, get_adc_samples(fpga=3,signed=True))
        (h1,x) = numpy.histogram(d1,bins=128,range=(-128,128),new=True)
        (h3,x) = numpy.histogram(d3,bins=128,range=(-128,128),new=True)
        s1 = (d1.mean(), d1.std(), d1.min(), d1.max())
        s3 = (d3.mean(), d3.std(), d3.min(), d3.max())
        target_rms = 20.0
        print 'FPGA1: Mean=%.3f RMS=%.3f Min=%d Max=%d' % s1
        print '       Add %.1f dB attenuation (for target RMS %.1f)' \
                % (20.0*(math.log10(s1[1]) - math.log10(target_rms)), \
                target_rms)
        print 'FPGA3: Mean=%.3f RMS=%.3f Min=%d Max=%d' % s3
        print '       Add %.1f dB attenuation (for target RMS %.1f)' \
                % (20.0*(math.log10(s3[1]) - math.log10(target_rms)), \
                target_rms)
        pylab.plot(x[1:]-0.5, h1, label='FPGA1')
        pylab.plot(x[1:]-0.5, h3, label='FPGA3')
        pylab.legend()
        pylab.show()
