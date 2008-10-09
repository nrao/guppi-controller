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

"""Provide AgentSim with parameters and profiles.  See update_simulator.py"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

from agent import states

parameters = {
  'BEE2/FPGA2/vacc_subsys_V_V_3_BRAM': 'fffffffeffffffe600000007ffffffe3'
, 'BEE2/FPGA2/vacc_subsys_V_V_2_BRAM': 'ffffffae00000012fffffff8ffffffe1'
, 'BEE2/FPGA2/vacc_subsys_V_V_1_BRAM': '000000430000001500000007fffffff3'
, 'BEE2/FPGA2/vacc_subsys_V_V_0_BRAM': '00000711fffffffefffffff10000002c'
, 'BEE2/FPGA2/vacc_subsys_U_U_3_BRAM': '0000004d0000004b000000310000002f'
, 'BEE2/FPGA2/vacc_subsys_U_U_2_BRAM': '000001010000008f0000000900000070'
, 'BEE2/FPGA2/vacc_subsys_U_U_1_BRAM': '00000143000000770000002300000037'
, 'BEE2/FPGA2/vacc_subsys_U_U_0_BRAM': '0014c3f500000079000000290000003b'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_3_BRAM': 'ffffffbbffffffcffffffffdffffffcb'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_2_BRAM': 'ffffffccffffffcbffffffe600000017'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_1_BRAM': '00000026fffffff30000001200000002'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_0_BRAM': 'ffdcf568000000080000001bffffffcd'
, 'BEE2/FPGA2/vacc_subsys_I_I_3_BRAM': '0000014a000000960000009e000000d5'
, 'BEE2/FPGA2/vacc_subsys_I_I_2_BRAM': '0000011a000000810000009e0000008e'
, 'BEE2/FPGA2/vacc_subsys_I_I_1_BRAM': '0000021d0000011a000000b5000000c4'
, 'BEE2/FPGA2/vacc_subsys_I_I_0_BRAM': '002878df0000014600000069000000a0'
, 'BEE2/FPGA2/ten_GbE': '626567696e0a096d6163203d2031303a'
, 'BEE2/FPGA2/SCALE_V': '07fffffc'
, 'BEE2/FPGA2/SCALE_U': '07fffffc'
, 'BEE2/FPGA2/SCALE_Q': '07fffffc'
, 'BEE2/FPGA2/SCALE_I': '07fffffc'
, 'BEE2/FPGA2/OFFSET_V': '00000000'
, 'BEE2/FPGA2/OFFSET_U': '00000000'
, 'BEE2/FPGA2/OFFSET_Q': '00000000'
, 'BEE2/FPGA2/OFFSET_I': '00000000'
, 'BEE2/FPGA2/GUPPi_PIPES_ARM': '00000000'
, 'BEE2/FPGA2/DEST_PORT': '0000c350'
, 'BEE2/FPGA2/DEST_IP': 'c0a80307'
, 'BEE2/FPGA2/DC_P1_BINS_3_BRAM': 'ffe20000ffdd0005ffdd000cffcefff9'
, 'BEE2/FPGA2/DC_P1_BINS_2_BRAM': 'ffe40010ffe2ffd7ffeffff8ffebffce'
, 'BEE2/FPGA2/DC_P1_BINS_1_BRAM': 'ffe4fffeffd8ffe4ffed00400001ffee'
, 'BEE2/FPGA2/DC_P1_BINS_0_BRAM': 'ef36fffdffc9fffafff7fff500040004'
, 'BEE2/FPGA2/DC_P0_BINS_3_BRAM': 'fff4ffeafffc0001ffd5ffe50017ffbe'
, 'BEE2/FPGA2/DC_P0_BINS_2_BRAM': 'ffedfff9ffff0001ffed000effe6ffd7'
, 'BEE2/FPGA2/DC_P0_BINS_1_BRAM': 'ffd900130003000a0006fff1ffddfffa'
, 'BEE2/FPGA2/DC_P0_BINS_0_BRAM': 'faaefffe0009ffe4ffe1000cffe5ffe5'
, 'BEE2/FPGA2/DC_BINS_EN': '00000001'
, 'BEE2/FPGA2/ACC_LENGTH': '0000000f'
, 'BEE2/FPGA1/SAMP_CMD': '00000000'
, 'BEE2/FPGA1/LE_CNTRL': '00000000'
, 'BEE2/FPGA1/FFT_SHIFT': 'aaaaaaaa'
, 'BEE2/FPGA1/DC_STATUS_BRAM': '00000002000000020000000200000002'
, 'BEE2/FPGA1/DC_SAMP_EN': '00000001'
, 'BEE2/FPGA1/DC_LO_SAMP_BRAM': '00fe02f8e20c08e8f0060cfe00fa14fe'
, 'BEE2/FPGA1/DC_HI_SAMP_BRAM': '0a00fe0812f404f802000000de1afaf2'
, 'BEE2/FPGA1/DC_BINS_EN': '00000001'
, 'BEE2/FPGA1/DC_BINS_3_BRAM': 'fff4ffeafffc0001ffd5ffe50017ffbe'
, 'BEE2/FPGA1/DC_BINS_2_BRAM': 'ffedfff9ffff0001ffed000effe6ffd7'
, 'BEE2/FPGA1/DC_BINS_1_BRAM': 'ffd900130003000a0006fff1ffddfffa'
, 'BEE2/FPGA1/DC_BINS_0_BRAM': 'faaefffe0009ffe4ffe1000cffe5ffe5'
, 'BEE2/FPGA3/SAMP_CMD': '00000000'
, 'BEE2/FPGA3/LE_CNTRL': '00000000'
, 'BEE2/FPGA3/FFT_SHIFT': 'aaaaaaaa'
, 'BEE2/FPGA3/DC_STATUS_BRAM': '00000002000000020000000200000002'
, 'BEE2/FPGA3/DC_SAMP_EN': '00000001'
, 'BEE2/FPGA3/DC_LO_SAMP_BRAM': '08080ef0f2ea001002f00c0208000aee'
, 'BEE2/FPGA3/DC_HI_SAMP_BRAM': 'e404080efef8f8140012e00c02f012fa'
, 'BEE2/FPGA3/DC_BINS_EN': '00000001'
, 'BEE2/FPGA3/DC_BINS_3_BRAM': 'ffe20000ffdd0005ffdd000cffcefff9'
, 'BEE2/FPGA3/DC_BINS_2_BRAM': 'ffe40010ffe2ffd7ffeffff8ffebffce'
, 'BEE2/FPGA3/DC_BINS_1_BRAM': 'ffe4fffeffd8ffe4ffed00400001ffee'
, 'BEE2/FPGA3/DC_BINS_0_BRAM': 'ef36fffdffc9fffafff7fff500040004'
, 'DAQ/SCANNUM': '1'
, 'DAQ/TELESCOP': 'GBT'
, 'DAQ/OBSERVER': 'unknown'
, 'DAQ/PROJID': 'TKA_09OCT08'
, 'DAQ/FRONTEND': 'Rcvr26_40'
, 'DAQ/NRCVR': '2'
, 'DAQ/FD_POLN': 'CIRC'
, 'DAQ/OBSFREQ': '7724.604'
, 'DAQ/SRC_NAME': '103359+731745'
, 'DAQ/TRK_MODE': 'UNKNOWN'
, 'DAQ/RA_STR': '14:55:21.2640'
, 'DAQ/RA': '223.8386'
, 'DAQ/DEC_STR': '+46:35:2.7600'
, 'DAQ/DEC': '46.5841'
, 'DAQ/LST': '50785'
, 'DAQ/AZ': '44.1400102583'
, 'DAQ/ZA': '12.1359562952'
, 'DAQ/BMAJ': '0.0266838417709'
, 'DAQ/BMIN': '0.0266838417709'
, 'DAQ/OBSBW': '800.0'
, 'DAQ/STT_IMJD': '54748'
, 'DAQ/STT_SMJD': '65453'
, 'DAQ/STT_OFFS': '0.0'
, 'DAQ/TFOLD': '30.0'
, 'DAQ/OBS_MODE': 'SEARCH'
, 'DAQ/BASENAME': 'guppi_54748_103359+731745_0001'
, 'DAQ/CAL_MODE': 'OFF'
, 'DAQ/SCANLEN': '28800.0'
, 'DAQ/BACKEND': 'GUPPI'
, 'DAQ/PKTFMT': 'GUPPI'
, 'DAQ/DATAHOST': 'bee2_10'
, 'DAQ/DATAPORT': '50000'
, 'DAQ/POL_TYPE': 'IQUV'
, 'DAQ/CAL_FREQ': '25.0'
, 'DAQ/CAL_DCYC': '0.5'
, 'DAQ/CAL_PHS': '0.0'
, 'DAQ/OBSNCHAN': '2048'
, 'DAQ/NPOL': '4'
, 'DAQ/NBITS': '8'
, 'DAQ/PFB_OVER': '4'
, 'DAQ/NBITSADC': '8'
, 'DAQ/ACC_LEN': '16'
, 'DAQ/ONLY_I': '0'
, 'DAQ/DS_TIME': '1'
, 'DAQ/DS_FREQ': '1'
, 'DAQ/NBIN': '256'
, 'DAQ/PARFILE': 'None'
, 'DAQ/OFFSET0': '0.0'
, 'DAQ/SCALE0': '1.0'
, 'DAQ/OFFSET1': '0.0'
, 'DAQ/SCALE1': '1.0'
, 'DAQ/OFFSET2': '0.5'
, 'DAQ/SCALE2': '1.0'
, 'DAQ/OFFSET3': '0.5'
, 'DAQ/SCALE3': '1.0'
, 'DAQ/TBIN': '4.096e-05'
, 'DAQ/CHAN_BW': '0.390625'
}

profiles = {
  'BEE2/b2_GOUT_U2_4K_800_A_NR_fpga2_2008_Sep_15_1400.bof': states['running']
, 'BEE2/b2_GDSP_U1_4K_800_A_XA_fpga1_2008_Jul_30_1356.bof': states['running']
, 'BEE2/b2_GDSP_U3_4K_800_A_XA_fpga3_2008_Jul_30_1414.bof': states['running']
, 'BEE2/b2_GDSP_U3_8K_800_A_NB_fpga3_2008_Oct_01_1037.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_LB_fpga2_2008_Sep_15_0950.bof': states['available']
, 'BEE2/b2_GOUT_U2_8K_800_A_NR_fpga2_2008_Sep_30_1212.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_03_fpga2_2008_Aug_20_1555.bof': states['available']
, 'BEE2/b2_GDSP_U1_8K_800_A_FB_fpga1_2008_Aug_26_1143.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_JR_fpga2_2008_Sep_05_1047.bof': states['available']
}

