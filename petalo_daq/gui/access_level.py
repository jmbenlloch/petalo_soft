# Dictionary where the key is a GUI field identifiers and the value
# another dictionary with the access level for each user.

user_access = {
    'SpinBox_Buffer' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'SpinBox_Pretrigger' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'SpinBox_Triggers' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'comboBox_tx_nlinks' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'comboBox_tx_ddr' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'comboBox_tx_mode' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'checkBox_debug_mode' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_veto_mode' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tdc_clk_div' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_r_clk_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_stop_ramp_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_counter_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_counter_period' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_tac_refresh_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tac_refresh_period' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_data_clk_div' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_fetp_enable' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_input_polarity' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_attenuator_ls' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_v_ref_diff_bias_ig' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_v_cal_ref_ig' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_fe_postamp_t' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_fe_postamp_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_v_cal_tp_top' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_v_cal_diff_bias_ig' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_v_att_diff_bias_ig' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_v_integ_ref_ig' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_imirror_bias_top' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_tdc_comp_bias' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_tdc_i_lsb' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_disc_lsb_t1' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_fe_ib2' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_vdifffoldcas' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_disc_vcas' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_disc_lsb_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_tdc_i_ref' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tdc_comp_vcas' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_fe_ib2_x2' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_main_global_dac' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_fe_ib1' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_disc_ib' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_disc_lsb_t2' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tdc_tac_vcas_p' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tdc_tac_vcas_n' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_adebug_out_mode' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_tdc_global_dac' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_adebug_buffer' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_disc_sf_bias' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_trigger_mode_1' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'comboBox_debug_mode' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_sync_chain_length' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_dead_time' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_counter_mode' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tac_max_age' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_tac_min_age' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_trigger_mode_2_t' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_trigger_mode_2_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_trigger_mode_2_q' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_trigger_mode_2_b' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_branch_en_eq' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_branch_en_t' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_qdc_mode' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_trigger_b_latched' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_min_intg_time' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_max_intg_time' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_output_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_qtx2_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_baseline_t' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_vth_t1' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_vth_t2' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_vth_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_baseline_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_fe_delay' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_postamp_gain_t' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_postamp_gain_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_postamp_sh_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_intg_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_intg_signal_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_att' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_tdc_current_t' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_tdc_current_e' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_fe_tp_en' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_integ_source_sw' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_t1_hysteresis' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_t2_hysteresis' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_e_hysteresis' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'comboBox_hysteresis_en_n' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_all_ch' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'spinBox_ch_number' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'checkBox_all_ASIC' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'spinBox_ASIC_n' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'checkBox_Temp_RST' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_Start' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_RD_Control_EN2' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_RD_Control_FA' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_RD_Control_SPD' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_RD_Control_IM' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_RD_Control_FB' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_Temp_RD_Control_SGL' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_Temp_Time' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'comboBox_Temp_CH_Sel' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    "checkBox_PWR_GStart" : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    "checkBox_PWR_Start" : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    "checkBox_PWR_RST" : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    "checkBox_PWR_18DIS"  : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'checkBox_PWR_25EN_1' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_25EN_2' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_0' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_1' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_2' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_3' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_4' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_5' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_6' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCCEN_7' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'checkBox_PWR_TOFPET_VCC25EN_0' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_1' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_2' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_3' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_4' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_5' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_6' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_PWR_TOFPET_VCC25EN_7' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'checkBox_PWR_STATUS_CONF_DONE' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_CONF_ON' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_18DIS' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_25EN_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_25EN_2' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_0' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_2' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_3' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_4' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_5' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_6' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCCEN_7' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_0' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_2' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_3' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_4' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_5' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_6' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_PWR_STATUS_TOFPET_VCC25EN_7' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },



    'checkBox_CLK_STAT_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_STAT_0' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_SEL_0' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_SEL_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_CONF_DONE' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_CONF_ON' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_REG_PROG_DONE' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_CLK_REG_PROG_READY' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'lineEdit_CLK_CONF_REG_PROG_VALUE' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },


    'checkBox_LINK_STATUS_IDL_ready' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_0' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_2' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_3' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_4' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_5' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_6' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNED_7' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_0' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_1' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_2' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_3' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_4' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_5' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_6' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LINK_STATUS_ALIGNING_7' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },


    'comboBox_RUN_MODE' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_RUN_THR_ON' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_RUN_Throughput' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_RUN_Event' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'checkBox_CLK_Start' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'checkBox_CLK_RST' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_CLK_locked' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_CLK_slave' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'checkBox_LMK_WREN' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_LMK_REG_ADD' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_LMK_REG_VALUE' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'checkBox_TOFPET_STATUS_ERR_CRC_GL' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_CFG_GL' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_CRC_CH' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_CFG_CH' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_ACK_CREAD' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_ACK_CWRITE' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_ACK_GREAD' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TOFPET_STATUS_ERR_ACK_GWRITE' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },


    'checkBox_TOFPET_LINK_RST' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_LINK_CONF' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_LINK_CONF_IODELAY' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_LINK_RST_IODELAY' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_LINK_BC' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_DDR' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_SYNC_RST' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_SYNC_RST_CONF' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_SYNC_RST_RUN' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_RST_CYCLES' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'comboBox_TOFPET_LINK_SEL_MUX' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'spinBox_TOPFET_CONF_VALUE' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },


    'checkBox_TOFPET_CONF_START' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_CONF_VERIFY' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_CONF_ERROR_RST' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'checkBox_TOFPET_CONF_WR' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_TOFPET_CONF_ADDR' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'comboBox_TOFPET_CONF_MODE' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },
    'spinBox_TOFPET_CONF_CH_SEL' : {
        'admin'   : True,
        'shifter' : True,
        'none'    : False,
    },

    'checkBox_LED_7' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LED_6' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LED_5' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LED_4' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_LED_3' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_Connected' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },

    'checkBox_Activate_done' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },

    'spinBox_TPULSE_Phase' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TPULSE_EvenOdd' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },
    'spinBox_TPULSE_Length_Up' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },
    'spinBox_TPULSE_Length_Down' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TPULSE_Continous' : {
        'admin'   : True,
        'shifter' : False,
        'none'    : False,
    },
    'spinBox_TPULSE_Phase_status' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TPULSE_Locked' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'spinBox_TPULSE_Length_Up_status' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'spinBox_TPULSE_Length_Down_status' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },
    'checkBox_TPULSE_Continous_status' : {
        'admin'   : False,
        'shifter' : False,
        'none'    : False,
    },

   'spinBox_TempMonitor_period' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'spinBox_TempMonitor_min' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'spinBox_TempMonitor_max' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },

   'checkBox_TempMonitor_0' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_1' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_2' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_3' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_4' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_5' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_6' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
   'checkBox_TempMonitor_7' : {
       'admin'   : True,
       'shifter' : False,
       'none'    : False,
   },
}

