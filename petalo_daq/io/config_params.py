def reverse_range_inclusive(start, end):
    """
    Returns an inverse range (step -1) including BOTH extremes.
    This breaks the python convention but makes it easier to copy the datasheet.

    Parameters:
    start (int): Start number
    end (int): End number

    Returns:
    range function from start to end decreasing by 1 from start to end.
    """
    return range(start, end-1, -1)


def range_inclusive(start, end):
    """
    Returns a range (step 1) including BOTH extremes.
    This breaks the python convention but makes it easier to copy the datasheet.

    Parameters:
    start (int): Start number
    end (int): End number

    Returns:
    range function from start to end increasing by 1 from start to end.
    """
    return range(start, end+1)


# Dictionary with all the fields for some configuration word and the
# corresponding bit ranges

global_config_fields = {
    "tx_nlinks"         : reverse_range_inclusive(1, 0),
    "tx_ddr"            : reverse_range_inclusive(2, 2),
    "tx_mode"           : reverse_range_inclusive(4, 3),
    "debug_mode"        : reverse_range_inclusive(5, 5),
    "veto_mode"         : reverse_range_inclusive(11, 6),
    "tdc_clk_div"       : reverse_range_inclusive(12, 12),
    "r_clk_en"          : reverse_range_inclusive(15, 13),
    # 17, 16 are unused
    "stop_ramp_en"      : reverse_range_inclusive(19, 18),
    "counter_en"        : reverse_range_inclusive(20, 20),
    "counter_period"    : reverse_range_inclusive(23, 21),
    "tac_refresh_en"    : reverse_range_inclusive(24, 24),
    "tac_refresh_period": reverse_range_inclusive(28, 25),
    "data_clk_div"      : reverse_range_inclusive(30, 29),
    # 31 unused
    "fetp_enable"       : reverse_range_inclusive(32, 32),
    "input_polarity"    : reverse_range_inclusive(33, 33),
    "attenuator_ls"     : range_inclusive(34, 39),
    "v_ref_diff_bias_ig": range_inclusive(40, 45),
    "v_cal_ref_ig"      : range_inclusive(46, 50),
    "fe_postamp_t"      : range_inclusive(51, 55),
    "fe_postamp_e"      : range_inclusive(56, 60),
    "v_cal_tp_top"      : range_inclusive(61, 65),
    "v_cal_diff_bias_ig": range_inclusive(66, 70),
    "v_att_diff_bias_ig": range_inclusive(71, 76),
    "v_integ_ref_ig"    : range_inclusive(77, 82),
    "imirror_bias_top"  : range_inclusive(83, 87),
    "tdc_comp_bias"     : range_inclusive(88, 92),
    "tdc_i_lsb"         : range_inclusive(93, 97),
    "disc_lsb_t1"       : range_inclusive(98, 103),
    "fe_ib2"            : [176, 104, 105, 106, 107, 108],
    "vdifffoldcas"      : range_inclusive(109, 114),
    "disc_vcas"         : range_inclusive(115, 118),
    "disc_lsb_e"        : range_inclusive(119, 124),
    "tdc_i_ref"         : range_inclusive(125, 129),
    "tdc_comp_vcas"     : range_inclusive(130, 133),
    "fe_ib2_x2"         : range_inclusive(134, 134),
    "main_global_dac"   : range_inclusive(135, 139),
    "fe_ib1"            : range_inclusive(140, 145),
    "disc_ib"           : range_inclusive(146, 151),
    "disc_lsb_t2"       : range_inclusive(152, 157),
    "tdc_tac_vcas_p"    : range_inclusive(158, 162),
    "tdc_tac_vcas_n"    : range_inclusive(163, 166),
    "adebug_out_mode"   : range_inclusive(167, 168),
    "tdc_global_dac"    : range_inclusive(169, 174),
    "adebug_buffer"     : range_inclusive(175, 175),
    # 2 bits unused
    "disc_sf_bias"      : range_inclusive(178, 183)
}


channel_config_fields = {
    "trigger_mode_1"    : reverse_range_inclusive(1, 0),
    "debug_mode"        : reverse_range_inclusive(3, 2),
    "sync_chain_length" : reverse_range_inclusive(5, 4),
    "dead_time"         : reverse_range_inclusive(11, 6),
    "counter_mode"      : reverse_range_inclusive(15, 12),
    "tac_max_age"       : reverse_range_inclusive(20, 16),
    "tac_min_age"       : reverse_range_inclusive(25, 21),
    "trigger_mode_2_t"  : reverse_range_inclusive(27, 26),
    "trigger_mode_2_e"  : reverse_range_inclusive(30, 28),
    "trigger_mode_2_q"  : reverse_range_inclusive(32, 31),
    "trigger_mode_2_b"  : reverse_range_inclusive(35, 33),
    "branch_en_eq"      : reverse_range_inclusive(36, 36),
    "branch_en_t"       : reverse_range_inclusive(37, 37),
    "qdc_mode"          : reverse_range_inclusive(38, 38),
    "trigger_b_latched" : reverse_range_inclusive(39, 39),
    "min_intg_time"     : reverse_range_inclusive(46, 40),
    "max_intg_time"     : reverse_range_inclusive(53, 47),
    "output_en"         : reverse_range_inclusive(55, 54),
    "qtx2_en"           : reverse_range_inclusive(56, 56),
    "baseline_t"        : reverse_range_inclusive(62, 57),
    "vth_t1"            : reverse_range_inclusive(68, 63),
    "vth_t2"            : reverse_range_inclusive(74, 69),
    "vth_e"             : reverse_range_inclusive(80, 75),
    "baseline_e"        : reverse_range_inclusive(83, 81),
    "fe_delay"          : [84, 88, 87, 85, 86],
    "postamp_gain_t"    : range_inclusive(89, 90),
    "postamp_gain_e"    : range_inclusive(91, 92),
    "postamp_sh_e"      : reverse_range_inclusive(94, 93),
    "intg_en"           : reverse_range_inclusive(95, 95),
    "intg_signal_en"    : reverse_range_inclusive(96, 96),
    "att"               : reverse_range_inclusive(99, 97),
    "tdc_current_t"     : reverse_range_inclusive(103, 100),
    "tdc_current_e"     : reverse_range_inclusive(107, 104),
    "fe_tp_en"          : reverse_range_inclusive(109, 108),
    #"ch63_obuf_msb"     : reverse_range_inclusive(110, 111),
    "integ_source_sw"   : reverse_range_inclusive(112, 111),
    "t1_hysteresis"     : reverse_range_inclusive(117, 115),
    "t2_hysteresis"     : reverse_range_inclusive(120, 118),
    "e_hysteresis"      : reverse_range_inclusive(123, 121),
    "hysteresis_en_n"   : reverse_range_inclusive(124, 124)

}

temperature_config_fields = {
    "Temp_Time"           : reverse_range_inclusive(31, 12),
    "Temp_CH_Sel"         : reverse_range_inclusive(11, 8),
    "Temp_RD_Control_EN2" : reverse_range_inclusive( 7, 7),
    "Temp_RD_Control_IM"  : reverse_range_inclusive( 6, 6),
    "Temp_RD_Control_FA"  : reverse_range_inclusive( 5, 5),
    "Temp_RD_Control_FB"  : reverse_range_inclusive( 4, 4),
    "Temp_RD_Control_SPD" : reverse_range_inclusive( 3, 3),
    "Temp_RD_Control_SGL" : reverse_range_inclusive( 2, 2),
    "Temp_Start"          : reverse_range_inclusive( 1, 1),
    "Temp_RST"            : reverse_range_inclusive( 0, 0),
}

power_control_fields = {
    "PWR_GStart"         : reverse_range_inclusive(31, 31),
    "PWR_Start"          : reverse_range_inclusive(30, 30),
    "PWR_RST"            : reverse_range_inclusive(29, 29),
    "PWR_18DIS"          : reverse_range_inclusive(18, 18),
    "PWR_25EN"           : reverse_range_inclusive(17, 16),
    "PWR_TOFPET_VCCEN"   : reverse_range_inclusive(15,  8),
    "PWR_TOFPET_VCC25EN" : reverse_range_inclusive( 7,  0),
}

power_status_fields = {
    "PWR_STATUS_CONF_DONE"        : reverse_range_inclusive(31, 31),
    "PWR_STATUS_CONF_ON"          : reverse_range_inclusive(30, 30),
    "PWR_STATUS_18DIS"            : reverse_range_inclusive(18, 18),
    "PWR_STATUS_25EN_1"           : reverse_range_inclusive(17, 17),
    "PWR_STATUS_25EN_2"           : reverse_range_inclusive(16, 16),
    "PWR_STATUS_TOFPET_VCCEN_7"   : reverse_range_inclusive(15, 15),
    "PWR_STATUS_TOFPET_VCCEN_6"   : reverse_range_inclusive(14, 14),
    "PWR_STATUS_TOFPET_VCCEN_5"   : reverse_range_inclusive(13, 13),
    "PWR_STATUS_TOFPET_VCCEN_4"   : reverse_range_inclusive(12, 12),
    "PWR_STATUS_TOFPET_VCCEN_3"   : reverse_range_inclusive(11, 11),
    "PWR_STATUS_TOFPET_VCCEN_2"   : reverse_range_inclusive(10, 10),
    "PWR_STATUS_TOFPET_VCCEN_1"   : reverse_range_inclusive( 9,  9),
    "PWR_STATUS_TOFPET_VCCEN_0"   : reverse_range_inclusive( 8,  8),
    "PWR_STATUS_TOFPET_VCC25EN_7" : reverse_range_inclusive( 7,  7),
    "PWR_STATUS_TOFPET_VCC25EN_6" : reverse_range_inclusive( 6,  6),
    "PWR_STATUS_TOFPET_VCC25EN_5" : reverse_range_inclusive( 5,  5),
    "PWR_STATUS_TOFPET_VCC25EN_4" : reverse_range_inclusive( 4,  4),
    "PWR_STATUS_TOFPET_VCC25EN_3" : reverse_range_inclusive( 3,  3),
    "PWR_STATUS_TOFPET_VCC25EN_2" : reverse_range_inclusive( 2,  2),
    "PWR_STATUS_TOFPET_VCC25EN_1" : reverse_range_inclusive( 1,  1),
    "PWR_STATUS_TOFPET_VCC25EN_0" : reverse_range_inclusive( 0,  0),
}

clock_status_fields = {
    "CLK_STAT_1"              : reverse_range_inclusive(15, 15),
    "CLK_STAT_0"              : reverse_range_inclusive(14, 14),
    "CLK_SEL_1"               : reverse_range_inclusive(13, 13),
    "CLK_SEL_0"               : reverse_range_inclusive(12, 12),
    "CLK_CONF_DONE"           : reverse_range_inclusive(11, 11),
    "CLK_CONF_ON"             : reverse_range_inclusive(10, 10),
    "CLK_REG_PROG_DONE"       : reverse_range_inclusive( 9,  9),
    "CLK_REG_PROG_READY"      : reverse_range_inclusive( 8,  8),
    "CLK_CONF_REG_PROG_VALUE" : reverse_range_inclusive( 7,  0),
}

link_status_fields = {
    "LINK_STATUS_IDL_ready"  : reverse_range_inclusive(16, 16),
    "LINK_STATUS_ALIGNED_7"  : reverse_range_inclusive(15, 15),
    "LINK_STATUS_ALIGNED_6"  : reverse_range_inclusive(14, 14),
    "LINK_STATUS_ALIGNED_5"  : reverse_range_inclusive(13, 13),
    "LINK_STATUS_ALIGNED_4"  : reverse_range_inclusive(12, 12),
    "LINK_STATUS_ALIGNED_3"  : reverse_range_inclusive(11, 11),
    "LINK_STATUS_ALIGNED_2"  : reverse_range_inclusive(10, 10),
    "LINK_STATUS_ALIGNED_1"  : reverse_range_inclusive( 9,  9),
    "LINK_STATUS_ALIGNED_0"  : reverse_range_inclusive( 8,  8),
    "LINK_STATUS_ALIGNING_7" : reverse_range_inclusive( 7, 7),
    "LINK_STATUS_ALIGNING_6" : reverse_range_inclusive( 6, 6),
    "LINK_STATUS_ALIGNING_5" : reverse_range_inclusive( 5, 5),
    "LINK_STATUS_ALIGNING_4" : reverse_range_inclusive( 4, 4),
    "LINK_STATUS_ALIGNING_3" : reverse_range_inclusive( 3, 3),
    "LINK_STATUS_ALIGNING_2" : reverse_range_inclusive( 2, 2),
    "LINK_STATUS_ALIGNING_1" : reverse_range_inclusive( 1, 1),
    "LINK_STATUS_ALIGNING_0" : reverse_range_inclusive( 0, 0),
}


run_control_fields = {
    "RUN_MODE"       : reverse_range_inclusive(29, 28),
    "RUN_THR_ON"     : reverse_range_inclusive(27, 27),
    "RUN_Throughput" : reverse_range_inclusive(26, 16),
    "RUN_Event"      : reverse_range_inclusive(15,  0),
}

run_status_fields = {
    "RUN_MODE" : reverse_range_inclusive(2, 1),
    "ACQ_ON"   : reverse_range_inclusive(0 ,0),
}

clock_control_fields = {
    "CLK_Start" : reverse_range_inclusive(30, 30),
    "CLK_RST"   : reverse_range_inclusive(29, 29),
}

lmk_control_fields = {
    "LMK_WREN"      : reverse_range_inclusive(15, 15),
    "LMK_REG_ADD"   : reverse_range_inclusive(14,  8),
    "LMK_REG_VALUE" : reverse_range_inclusive( 7,  0),
}

tofpet_config_fields = {
    "TOFPET_CONF_START" : reverse_range_inclusive(31, 31),
    "TOFPET_VERIFY"     : reverse_range_inclusive(30, 30),
    "TOFPET_ERROR_RST"  : reverse_range_inclusive(29, 29),
    "TOFPET_CONF_WR"    : reverse_range_inclusive(20, 20),
    "TOFPET_CONF_ADDR"  : reverse_range_inclusive(16,  8),
    "TOFPET_MODE"       : reverse_range_inclusive( 7,  6),
    "TOFPET_CH_SEL"     : reverse_range_inclusive( 5,  0),
}

tofpet_status_fields =  {
    'TOFPET_STATUS_ERR_CRC_GL'     : reverse_range_inclusive(7, 7),
    'TOFPET_STATUS_ERR_CFG_GL'     : reverse_range_inclusive(6, 6),
    'TOFPET_STATUS_ERR_CRC_CH'     : reverse_range_inclusive(5, 5),
    'TOFPET_STATUS_ERR_CFG_CH'     : reverse_range_inclusive(4, 4),
    'TOFPET_STATUS_ERR_ACK_CREAD'  : reverse_range_inclusive(3, 3),
    'TOFPET_STATUS_ERR_ACK_CWRITE' : reverse_range_inclusive(2, 2),
    'TOFPET_STATUS_ERR_ACK_GREAD'  : reverse_range_inclusive(1, 1),
    'TOFPET_STATUS_ERR_ACK_GWRITE' : reverse_range_inclusive(0, 0),
}

link_control_fields = {
    'TOFPET_LINK_RST'     : reverse_range_inclusive(31, 31),
    'TOFPET_LINK_CONF'    : reverse_range_inclusive(30, 30),
    'TOFPET_LINK_BC'      : reverse_range_inclusive( 3,  3),
    'TOFPET_LINK_SEL_MUX' : reverse_range_inclusive( 2,  0),
}

tofpet_config_value_fields = {
    'TOPFET_CONF_VALUE' : reverse_range_inclusive(31, 0),
}

# 'checkBox_TOFPET_CONF_START'
# 'checkBox_TOFPET_VERIFY'
# 'checkBox_TOFPET_ERROR_RST'
# 'checkBox_TOFPET_CONF_WR'
# 'spinBox_TOFPET_CONF_ADDR'
# 'comboBox_TOFPET_MODE'
# 'comboBox_TOFPET_CH_SEL'
