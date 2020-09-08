def nrange(start, end):
    r = [x for x in range(start, end) ]
    r.reverse()
    return r

# Dictionary with all the fields for some configuration word and the
# corresponding bit ranges

global_config_fields = {
    # TODO: Check ordering
    "tx_nlinks"         : slice(0, 2),
    "tx_ddr"            : slice(2, 3),
    "tx_mode"           : slice(3, 5),
    "debug_mode"        : slice(5, 6),
    "veto_mode"         : slice(6, 12),
    "tdc_clk_div"       : slice(12, 13),
    "r_clk_en"          : slice(13, 16),# bits 16..17 are ignored
    "stop_ramp_en"      : slice(18, 20),
    "counter_en"        : slice(20, 21),
    "counter_period"    : slice(21, 24),
    "tac_refresh_en"    : slice(24, 25),
    "tac_refresh_period": slice(25, 29),
    "data_clk_div"      : slice(29, 31),
    #  "unused_1"          : slice(31, 32),
    "fetp_enable"       : slice(32, 33),
    "input_polarity"    : slice(33, 34),
    "attenuator_ls"     : slice(34, 40),
    "v_ref_diff_bias_ig": slice(40, 46),
    "v_cal_ref_ig"      : slice(46, 51),
    "fe_postamp_t"      : slice(51, 56),
    "fe_postamp_e"      : slice(56, 61),
    "v_cal_tp_top"      : slice(61, 66),
    "v_cal_diff_bias_ig": slice(66, 71),
    "v_att_diff_bias_ig": slice(71, 77),
    "v_integ_ref_ig"    : slice(77, 83),
    "imirror_bias_top"  : slice(83, 88),
    "tdc_comp_bias"     : slice(88, 93),
    "tdc_i_lsb"         : slice(93, 98),
    "disc_lsb_t1"       : slice(98, 104),
    "fe_ib2"            : slice(104, 109), # cgate selection is "msb" for ib2
    "vdifffoldcas"      : slice(109, 115),
    "disc_vcas"         : slice(115, 119),
    "disc_lsb_e"        : slice(119, 125),
    "tdc_i_ref"         : slice(125, 130),
    "tdc_comp_vcas"     : slice(130, 134),
    "fe_ib2_x2"          : slice(134, 135),
    "main_global_dac"   : slice(135, 140),
    "fe_ib1"            : slice(140, 146),
    "disc_ib"           : slice(146, 152),
    "disc_lsb_t2"       : slice(152, 158),
    "tdc_tac_vcas_p"    : slice(158, 163),
    "tdc_tac_vcas_n"    : slice(163, 167),
    "adebug_out_mode"   : slice(167, 169),
    "tdc_global_dac"    : slice(169, 175),
    "adebug_buffer"     : slice(175, 176),
    # 2 bits unused
    "disc_sf_bias"      : slice(178, 184)
}


channel_config_fields = {
    "trigger_mode_1"    : slice(0, 2),
    "debug_mode"        : slice(2, 4),
    "sync_chain_length" : slice(4, 6),
    "dead_time"         : slice(6, 12),
    "counter_mode"      : slice(12, 16),
    "tac_max_age"       : slice(16, 21),
    "tac_min_age"       : slice(21, 26),
    "trigger_mode_2_t"  : slice(26, 28),
    "trigger_mode_2_e"  : slice(28, 31),
    "trigger_mode_2_q"  : slice(31, 33),
    "trigger_mode_2_b"  : slice(33, 36),
    "branch_en_eq"      : slice(36, 37),
    "branch_en_t"       : slice(37, 38),
    "qdc_mode"          : slice(38, 39),
    "trigger_b_latched" : slice(39, 40),
    "min_intg_time"     : slice(40, 47),
    "max_intg_time"     : slice(47, 54),
    "output_en"         : slice(54, 56),
    "qtx2_en"           : slice(56, 57),
    "baseline_t"        : slice(57, 63),
    "vth_t1"            : slice(63, 69),
    "vth_t2"            : slice(69, 75),
    "vth_e"             : slice(75, 81),
    "baseline_e"        : slice(81, 84),
    "fe_delay"          : slice(84, 89), #TODO: review order
    "postamp_gain_t"    : slice(89, 91),
    "postamp_gain_e"    : slice(91, 93),
    "postamp_sh_e"      : slice(93, 95),
    "intg_en"           : slice(95, 96),
    "intg_signal_en"    : slice(96, 97),
    "att"               : slice(97, 100),
    "tdc_current_t"     : slice(100, 104),
    "tdc_current_e"     : slice(104, 108),
    "fe_tp_en"          : slice(108, 110),
    #"ch63_obuf_msb"     : slice(110, 111),
    "integ_source_sw"   : slice(111,113),
    "t1_hysteresis"     : slice(115, 118),
    "t2_hysteresis"     : slice(118, 121),
    "e_hysteresis"      : slice(121, 124),
    "hysteresis_en_n"   : slice(124, 125)

}

