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
  'BEE2/FPGA2/vacc_subsys_V_V_3_BRAM': 'fffe9bdeffff4f0dffff89f4ffff4166'
, 'BEE2/FPGA2/vacc_subsys_V_V_2_BRAM': 'ffffa20bfffefd05ffff59f6ffff6e51'
, 'BEE2/FPGA2/vacc_subsys_V_V_1_BRAM': '000187a9000124fe00014afa00026b82'
, 'BEE2/FPGA2/vacc_subsys_V_V_0_BRAM': '0000069bffff8a33000098c70000d47f'
, 'BEE2/FPGA2/vacc_subsys_U_U_3_BRAM': '0003770d0002b009000202390003243d'
, 'BEE2/FPGA2/vacc_subsys_U_U_2_BRAM': '0000d57300014d5c0002374600026eb4'
, 'BEE2/FPGA2/vacc_subsys_U_U_1_BRAM': '00026a29000277ad000681bb000300a4'
, 'BEE2/FPGA2/vacc_subsys_U_U_0_BRAM': '0019b43c0003b1320007fabb00040ce1'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_3_BRAM': '0001297c00010dff0001c1a500016b86'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_2_BRAM': '000186170002edbb000228800003b775'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_1_BRAM': '0000ca4300013e890001a1ef000246e0'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_0_BRAM': 'ffe5732f0000f2e40000ff220002251c'
, 'BEE2/FPGA2/vacc_subsys_I_I_3_BRAM': '000268a70003cfaf00052744000613d8'
, 'BEE2/FPGA2/vacc_subsys_I_I_2_BRAM': '0003c70c0004688500036e95000401cc'
, 'BEE2/FPGA2/vacc_subsys_I_I_1_BRAM': '001a56f6000c78db00067d380003c690'
, 'BEE2/FPGA2/vacc_subsys_I_I_0_BRAM': '002878110002decf0007cc24000846f0'
, 'BEE2/FPGA2/ten_GbE': '626567696e0a096d6163203d2031303a'
, 'BEE2/FPGA2/SCALE_V': '07333333'
, 'BEE2/FPGA2/SCALE_U': '07333333'
, 'BEE2/FPGA2/SCALE_Q': '07333333'
, 'BEE2/FPGA2/SCALE_I': '07333333'
, 'BEE2/FPGA2/OFFSET_V': '00000000'
, 'BEE2/FPGA2/OFFSET_U': '00000000'
, 'BEE2/FPGA2/OFFSET_Q': '00000000'
, 'BEE2/FPGA2/OFFSET_I': '00000000'
, 'BEE2/FPGA2/GUPPi_PIPES_ARM': '00000000'
, 'BEE2/FPGA2/DEST_PORT': '0000c350'
, 'BEE2/FPGA2/DEST_IP': '0a110007'
, 'BEE2/FPGA2/DC_P1_BINS_3_BRAM': 'ffe7ffecfff90026fff3ffe2fffd0008'
, 'BEE2/FPGA2/DC_P1_BINS_2_BRAM': 'ffc90002ffe5fff20012ffc9ffea0012'
, 'BEE2/FPGA2/DC_P1_BINS_1_BRAM': 'ffcffffeffd7000bffd2fff8000d0008'
, 'BEE2/FPGA2/DC_P1_BINS_0_BRAM': 'f197fffdffd4ffda0012001affdcfff8'
, 'BEE2/FPGA2/DC_P0_BINS_3_BRAM': '0008ffd2ffde000cfffa000700060007'
, 'BEE2/FPGA2/DC_P0_BINS_2_BRAM': 'ffd4ffdfffdcffedffe5fffdffd00018'
, 'BEE2/FPGA2/DC_P0_BINS_1_BRAM': 'fff2ffcaffe30002ffe6ffebffd9000e'
, 'BEE2/FPGA2/DC_P0_BINS_0_BRAM': 'f92cfffeffe40001ffeafff4fff4000d'
, 'BEE2/FPGA2/DC_BINS_EN': '00000001'
, 'BEE2/FPGA2/ACC_LENGTH': '0000000f'
, 'BEE2/FPGA1/SAMP_CMD': '00000000'
, 'BEE2/FPGA1/LE_CNTRL': '00000000'
, 'BEE2/FPGA1/FFT_SHIFT': 'aaaaaaaa'
, 'BEE2/FPGA1/DC_STATUS_BRAM': '00000002000000020000000200000002'
, 'BEE2/FPGA1/DC_SAMP_EN': '00000001'
, 'BEE2/FPGA1/DC_LO_SAMP_BRAM': 'f61410f0fc1e12d810ece214fa0818f0'
, 'BEE2/FPGA1/DC_HI_SAMP_BRAM': 'fc10f2fef4f60e06fafe0ef406f40af6'
, 'BEE2/FPGA1/DC_BINS_EN': '00000001'
, 'BEE2/FPGA1/DC_BINS_3_BRAM': '0008ffd2ffde000cfffa000700060007'
, 'BEE2/FPGA1/DC_BINS_2_BRAM': 'ffd4ffdfffdcffedffe5fffdffd00018'
, 'BEE2/FPGA1/DC_BINS_1_BRAM': 'fff2ffcaffe30002ffe6ffebffd9000e'
, 'BEE2/FPGA1/DC_BINS_0_BRAM': 'f92cfffeffe40001ffeafff4fff4000d'
, 'BEE2/FPGA3/SAMP_CMD': '00000000'
, 'BEE2/FPGA3/LE_CNTRL': '00000000'
, 'BEE2/FPGA3/FFT_SHIFT': 'aaaaaaaa'
, 'BEE2/FPGA3/DC_STATUS_BRAM': '00000002000000020000000200000002'
, 'BEE2/FPGA3/DC_SAMP_EN': '00000001'
, 'BEE2/FPGA3/DC_LO_SAMP_BRAM': 'fc0a04e41efad6fa1af8f002100a0cf4'
, 'BEE2/FPGA3/DC_HI_SAMP_BRAM': '000400060e0804f60ceefcf0f806eee8'
, 'BEE2/FPGA3/DC_BINS_EN': '00000001'
, 'BEE2/FPGA3/DC_BINS_3_BRAM': 'ffe7ffecfff90026fff3ffe2fffd0008'
, 'BEE2/FPGA3/DC_BINS_2_BRAM': 'ffc90002ffe5fff20012ffc9ffea0012'
, 'BEE2/FPGA3/DC_BINS_1_BRAM': 'ffcffffeffd7000bffd2fff8000d0008'
, 'BEE2/FPGA3/DC_BINS_0_BRAM': 'f197fffdffd4ffda0012001affdcfff8'
}

profiles = {
  'BEE2/b2_GOUT_U2_4K_800_A_NR_fpga2_2008_Sep_15_1400.bof': states['running']
, 'BEE2/b2_GDSP_U1_4K_800_A_XA_fpga1_2008_Jul_30_1356.bof': states['running']
, 'BEE2/b2_GDSP_U3_4K_800_A_XA_fpga3_2008_Jul_30_1414.bof': states['running']
, 'BEE2/bGOUT_1SFA_D14_fpga2_2009_Feb_05_1529.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_BP_fpga3_2009_Feb_17_1458.bof': states['available']
, 'BEE2/bGDSP_U1_8K_248_A_00_fpga1_2008_Oct_22_1407.bof': states['available']
, 'BEE2/bGDSP_U3_8K_248_A_00_fpga3_2008_Oct_22_1427.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_BP_fpga1_2009_Feb_17_1429.bof': states['available']
}
