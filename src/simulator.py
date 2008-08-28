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

###################################################################
parameters = {
  'BEE2/FPGA2/vacc_subsys_V_V_3_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_V_V_2_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_V_V_1_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_V_V_0_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_U_U_3_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_U_U_2_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_U_U_1_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_U_U_0_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_3_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_2_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_1_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_Q_Q_0_BRAM': 'ffffffffffffffffffffffffffffffff'
, 'BEE2/FPGA2/vacc_subsys_I_I_3_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/vacc_subsys_I_I_2_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/vacc_subsys_I_I_1_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/vacc_subsys_I_I_0_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/ten_GbE': '626567696e0a096d6163203d2030303a'
, 'BEE2/FPGA2/SCALE_V': '00010000'
, 'BEE2/FPGA2/SCALE_U': '00010000'
, 'BEE2/FPGA2/SCALE_Q': '00010000'
, 'BEE2/FPGA2/SCALE_I': '00010000'
, 'BEE2/FPGA2/OFFSET_V': '00000000'
, 'BEE2/FPGA2/OFFSET_U': '00000000'
, 'BEE2/FPGA2/OFFSET_Q': '00000000'
, 'BEE2/FPGA2/OFFSET_I': '00000000'
, 'BEE2/FPGA2/GUPPi_PIPES_ARM': '00000000'
, 'BEE2/FPGA2/DEST_PORT': '0000c350'
, 'BEE2/FPGA2/DEST_IP': 'c0a80307'
, 'BEE2/FPGA2/DC_P1_BINS_3_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P1_BINS_2_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P1_BINS_1_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P1_BINS_0_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P0_BINS_3_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P0_BINS_2_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P0_BINS_1_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_P0_BINS_0_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA2/DC_BINS_EN': '00000001'
, 'BEE2/FPGA2/ACC_LENGTH': '0000000f'
, 'BEE2/FPGA1/SAMP_CMD': '00000000'
, 'BEE2/FPGA1/LE_CNTRL': '00000000'
, 'BEE2/FPGA1/FFT_SHIFT': 'ffffffff'
, 'BEE2/FPGA1/DC_STATUS_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA1/DC_SAMP_EN': '00000001'
, 'BEE2/FPGA1/DC_LO_SAMP_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA1/DC_HI_SAMP_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA1/DC_BINS_EN': '00000001'
, 'BEE2/FPGA1/DC_BINS_3_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA1/DC_BINS_2_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA1/DC_BINS_1_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA1/DC_BINS_0_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/SAMP_CMD': '00000000'
, 'BEE2/FPGA3/LE_CNTRL': '00000000'
, 'BEE2/FPGA3/FFT_SHIFT': 'ffffffff'
, 'BEE2/FPGA3/DC_STATUS_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/DC_SAMP_EN': '00000001'
, 'BEE2/FPGA3/DC_LO_SAMP_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/DC_HI_SAMP_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/DC_BINS_EN': '00000001'
, 'BEE2/FPGA3/DC_BINS_3_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/DC_BINS_2_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/DC_BINS_1_BRAM': '00000000000000000000000000000000'
, 'BEE2/FPGA3/DC_BINS_0_BRAM': '00000000000000000000000000000000'
}

profiles = {
  'BEE2/b2_GOUT_U2_4K_800_A_03_fpga2_2008_Aug_20_1555.bof': states['running']
, 'BEE2/b2_GDSP_U1_4K_800_A_XA_fpga1_2008_Jul_30_1356.bof': states['running']
, 'BEE2/b2_GDSP_U3_4K_800_A_XA_fpga3_2008_Jul_30_1414.bof': states['running']
, 'BEE2/b2_GDSP_U1_4K_A_0_fpga1_2008_Jun_10_1446.bof': states['available']
, 'BEE2/b2go_200_24_fpga2_2008_Apr_30_1315.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_DE_fpga3_2008_Jul_22_1351.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_0_fpga2_2008_Jul_01_0916.bof': states['available']
, 'BEE2/b2_GOUT_4K_A_0_fpga2_2008_Jun_09_1010.bof': states['available']
, 'BEE2/bee2_guppi_output_User2_fpga2_2008_Feb_20_1002.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_0_fpga1_2008_Jul_02_1439.bof': states['available']
, 'BEE2/b2_XAUI_SYNC_101_fpga3_2008_Jul_14_1601.bof': states['available']
, 'BEE2/b2go_100_03_fpga2_2008_Apr_08_1457.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_PR_fpga3_2008_Jul_03_1017.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_01_fpga2_2008_Aug_14_1033.bof': states['available']
, 'BEE2/bee2_guppi_dsp_User3_4K_fpga3_2008_Mar_28_2113.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_0_fpga1_2008_Jun_30_1443.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_0_fpga2_2008_Jul_02_1125.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_0_fpga3_2008_Jun_30_1445.bof': states['available']
, 'BEE2/b2go_100_05_fpga2_2008_Apr_11_0856.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_A_0_fpga3_2008_Jun_18_1318.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_A_0_fpga1_2008_Jun_03_1359.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_PZ_fpga2_2008_Jul_04_1247.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_XR_fpga1_2008_Jul_16_0813.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_01_fpga2_2008_Aug_14_1420.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_PR_fpga1_2008_Jul_03_1016.bof': states['available']
, 'BEE2/bee_test_uni2_fpga4_2008_Apr_01_1722.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_RX2_fpga1_2008_Jul_24_1203.bof': states['available']
, 'BEE2/pipes_test_user3_fpga3_2008_May_05_1016.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_A_0_fpga1_2008_Jun_18_1318.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_S_fpga3_2008_Jul_02_2216.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_A_0_fpga1_2008_Jun_19_0940.bof': states['available']
, 'BEE2/b2go_100_08_BR_fpga2_2008_Apr_16_1855.bof': states['available']
, 'BEE2/b2_GOUT_4K_A_0_fpga2_2008_Jun_09_1745.bof': states['available']
, 'BEE2/pipes_test_user1_fpga1_2008_May_05_1015.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_DE_fpga2_2008_Aug_12_1708.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_A_0_fpga3_2008_Jun_03_1359.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_0_fpga2_2008_Jul_01_1318.bof': states['available']
, 'BEE2/bee2_guppi_dsp_user1_4k_02_fpga1_2008_May_12_1407.bof': states['available']
, 'BEE2/b2go_200_25_fpga2_2008_May_01_1357.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_S_fpga2_2008_Jul_02_2233.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_B_AB_fpga2_2008_Aug_11_1553.bof': states['available']
, 'BEE2/b2go_200_23_fpga2_2008_Apr_28_1642.bof': states['available']
, 'BEE2/bee2_guppi_dsp_User3_4K_02_fpga3_2008_May_12_1407.bof': states['available']
, 'BEE2/b2_GOUT_4K_A_0_fpga2_2008_Jun_03_1746.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_A_0_fpga3_2008_Jun_05_0911.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_AF_fpga1_2008_Jul_09_1817.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_DE_fpga2_2008_Aug_13_0857.bof': states['available']
, 'BEE2/pipes_test_user2_fpga2_2008_May_05_1016.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_DE_fpga1_2008_Jul_22_1349.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_RX_fpga3_2008_Jul_23_1624.bof': states['available']
, 'BEE2/b2_XAUI_SYNC_102_fpga3_2008_Jul_16_1303.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_AB_fpga2_2008_Aug_11_1539.bof': states['available']
, 'BEE2/b2_XAUI_SYNC_101_fpga1_2008_Jul_14_1601.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_XA_fpga3_2008_Jul_30_0843.bof': states['available']
, 'BEE2/b2go_200_26_fpga2_2008_May_01_1620.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_PR_fpga2_2008_Jul_04_1246.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_A_0_fpga1_2008_Jun_05_0910.bof': states['available']
, 'BEE2/b2_GDSP_U3_4k_800_A_AF_fpga3_2008_Jul_09_1817.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_A_0_fpga3_2008_Jun_19_1720.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_PR_fpga2_2008_Jul_07_1749.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_S_fpga1_2008_Jul_02_2215.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_0_fpga3_2008_Jul_02_1440.bof': states['available']
, 'BEE2/b2go_100_08_fpga2_2008_Apr_14_1448.bof': states['available']
, 'BEE2/bee2_guppi_dsp_User3_4K_fpga3_2008_Feb_20_1407.bof': states['available']
, 'BEE2/bee2_guppi_dsp_User1_4k_fpga1_2008_Mar_28_2110.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_DE_fpga2_2008_Aug_12_1129.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_0_fpga2_2008_Jul_02_1448.bof': states['available']
, 'BEE2/b2go_200_22_fpga2_2008_Apr_28_1155.bof': states['available']
, 'BEE2/b2_XAUI_SYNC_102_fpga1_2008_Jul_16_1303.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_PR_fpga3_2008_Jul_07_0835.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_DE_fpga2_2008_Aug_13_1239.bof': states['available']
, 'BEE2/b2_GOUT_4K_A_0_fpga2_2008_Jun_18_1713.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_RX_fpga1_2008_Jul_23_1624.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_XR_fpga3_2008_Jul_15_1629.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_PR_fpga2_2008_Jul_07_1449.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_DE_fpga2_2008_Aug_13_1513.bof': states['available']
, 'BEE2/b2GO_100_01_fpga2_2008_Apr_03_1430.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_02_fpga2_2008_Aug_19_1532.bof': states['available']
, 'BEE2/b2go_100_04_fpga2_2008_Apr_10_1059.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_AL_fpga1_2008_Jul_09_0959.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_PR_fpga2_2008_Aug_07_0953.bof': states['available']
, 'BEE2/b2_GDSP_U1_4K_800_A_XA_fpga1_2008_Jul_29_2104.bof': states['available']
, 'BEE2/b2go_100_08_BR_fpga2_2008_Apr_16_1455.bof': states['available']
, 'BEE2/b2go_200_28_fpga2_2008_May_05_1345.bof': states['available']
, 'BEE2/b2GO_100_fpga2_2008_Apr_02_1356.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_AL_fpga3_2008_Jul_09_1000.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_800_A_RX2_fpga3_2008_Jul_24_1203.bof': states['available']
, 'BEE2/bee2_guppi_dsp_User1_4K_fpga1_2008_Feb_20_1022.bof': states['available']
, 'BEE2/b2_GOUT_U2_4K_800_A_T_fpga2_2008_Jul_02_0837.bof': states['available']
, 'BEE2/b2_GDSP_U3_4K_A_0_fpga3_2008_Jun_09_1736.bof': states['available']
, 'BEE2/b2go_200_21_fpga2_2008_Apr_25_1518.bof': states['available']
, 'BEE2/b2go_200_27_fpga2_2008_May_02_1607.bof': states['available']
}

