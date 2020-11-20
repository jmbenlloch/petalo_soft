from bitarray import bitarray

# Dictionaries with GUI field names as keys. The values has the following structure:
#  'default' :  Defalt value for the field
#  'values'  : Dictionary with possible values.
#      Keys are the index,
#       'text'  is the label for the GUI,
#       'value' is the actual internal value for that parameter.


general_data = {
    'SpinBox_Buffer' : {
        'default' : 5,
    },
    'SpinBox_Pretrigger' : {
        'default' : 250,
    },
    'SpinBox_Triggers' : {
        'default' : 100,
    }
}

global_data = {
    'comboBox_tx_nlinks' : {
        'default' : 2,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '1 link activate'},
            1 : {'value': bitarray('01'),
                 'text' : '2 links activate'},
            2 : {'value': bitarray('10'),
                 'text' : '4 links activate'},
        },
    },

    'comboBox_tx_ddr' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : 'Links operate in SDR mode (1 bit per CLK period)'},
            1 : {'value': bitarray('1'),
                 'text' : 'Links operate in DDR mode (2 bits per CLK period)'},
        },
    },

    'comboBox_tx_mode' : {
        'default' : 2,
        'values' : {
        0 : {'value': bitarray('00'),
             'text' : 'Receiver training pattern 0b00'},
        1 : {'value': bitarray('01'),
             'text' : 'Receiver training pattern 0b01'},
        2 : {'value': bitarray('10'),
             'text' : 'Normal data transmission'},
        },
    },

    'comboBox_veto_mode' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('000000'),
                 'text' : 'Normal operation'},
            1 : {'value': bitarray('000001'),
                 'text' : 'Triggering is inhibited for all channels when input SS is active.'},
            2 : {'value': bitarray('000010'),
                 'text' : 'Triggering is inhibited for all channels when input TEST_PULSE is active.'},
            3 : {'value': bitarray('000011'),
                 'text' : 'Triggering is inhibited for all channels when either input SS or TEST_PULSE is active.'},
        },
    },

    'comboBox_tdc_clk_div' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : 'DIV value 1'},
            1 : {'value': bitarray('1'),
                 'text' : 'DIV value 2'},
        },
    },

    'comboBox_counter_period' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('000'),
                 'text' : 'any (Counter disable)'},
            1 : {'value': bitarray('000'),
                 'text' : '0x0 (2^10 TDC_CLK cycles.)'},
            2 : {'value': bitarray('001'),
                 'text' : '0x1 (2^12 TDC_CLK cycles.)'},
            3 : {'value': bitarray('010'),
                 'text' : '0x2 (2^14 TDC_CLK cycles.)'},
            4 : {'value': bitarray('011'),
                 'text' : '0x3 (2^16 TDC_CLK cycles.)'},
            5 : {'value': bitarray('100'),
                 'text' : '0x4 (2^18 TDC_CLK cycles.)'},
            6 : {'value': bitarray('101'),
                 'text' : '0x5 (2^20 TDC_CLK cycles.)'},
            7 : {'value': bitarray('110'),
                 'text' : '0x6 (2^22 TDC_CLK cycles.)'},
            8 : {'value': bitarray('111'),
                 'text' : '0x7 (2^24 TDC_CLK cycles.)'},
        },
    },

    'comboBox_tac_refresh_period' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1001'),
                 'text' : '0b1001'},
        },
    },

    'comboBox_data_clk_div' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '0b00'},
        },
    },

    'comboBox_input_polarity' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1'),
                 'text' : '0b1'},
        },
    },

    'comboBox_disc_vcas' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1110'),
                 'text' : '0b1110'},
        },
    },

    'comboBox_disc_lsb_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('101000'),
                 'text' : '0b101000'},
        },
    },

    'comboBox_tdc_i_ref' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('10010'),
                 'text' : '0b10010'},
        },
    },

    'comboBox_tdc_comp_vcas' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0010'),
                 'text' : '0b0010'},
        },
    },

    'comboBox_fe_ib2_x2' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1'),
                 'text' : '0b1'},
        },
    },

    'comboBox_main_global_dac' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('10111'),
                 'text' : '0b10111'},
        },
    },

    'comboBox_fe_ib1' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('111011'),
                 'text' : '0b111011'},
        },
    },

    'comboBox_disc_ib' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('010011'),
                 'text' : '0b010011'},
        },
    },

    'comboBox_disc_lsb_t2' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('110000'),
                 'text' : '0b110000'},
        },
    },

    'comboBox_tdc_tac_vcas_p' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('01101'),
                 'text' : '0b01101'},
        },
    },

    'comboBox_tdc_tac_vcas_n' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0111'),
                 'text' : '0b0111'},
        },
    },

    'comboBox_adebug_out_mode' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('11'),
                 'text' : '0b11'},
        },
    },

    'comboBox_tdc_global_dac' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('010011'),
                 'text' : '0b010011'},
        },
    },

    'comboBox_adebug_buffer' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1'),
                 'text' : '0b1'},
        },
    },

    'comboBox_disc_sf_bias' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('100000'),
                 'text' : '0b100000'},
        },
    },

    'comboBox_attenuator_ls' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('101111'),
                 'text' : '0b101111'},
        },
    },

    'comboBox_v_ref_diff_bias_ig' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('111001'),
                 'text' : '0b111001'},
        },
    },

    'comboBox_v_cal_ref_ig' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('11111'),
                 'text' : '0b11111'},
        },
    },

    'comboBox_fe_postamp_t' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('10111'),
                 'text' : '0b10111'},
        },
    },

    'comboBox_fe_postamp_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('10100'),
                 'text' : '0b10100'},
        },
    },

    'comboBox_v_cal_tp_top' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00001'),
                 'text' : '0b00001'},
        },
    },

    'comboBox_v_cal_diff_bias_ig' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00000'),
                 'text' : '0b00000'},
        },
    },

    'comboBox_v_att_diff_bias_ig' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('100011'),
                 'text' : '0b100011'},
        },
    },

    'comboBox_v_integ_ref_ig' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('111011'),
                 'text' : '0b111011'},
        },
    },

    'comboBox_imirror_bias_top' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('10111'),
                 'text' : '0b10111'},
        },
    },

    'comboBox_tdc_comp_bias' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00100'),
                 'text' : '0b00100'},
        },
    },

    'comboBox_tdc_i_lsb' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('10011'),
                 'text' : '0b10011'},
        },
    },

    'comboBox_disc_lsb_t1' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('111010'),
                 'text' : '0b111010'},
        },
    },

    'comboBox_fe_ib2' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('110000'),
                 'text' : '0b110000'},
        },
    },

    'comboBox_vdifffoldcas' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('110110'),
                 'text' : '0b110110'},
        },
    },

    # Booleans
    'checkBox_debug_mode' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },

    'checkBox_r_clk_en' : {
        'default' : True,
        'values' : {
            False : {'value' : bitarray('000') },
            True  : {'value' : bitarray('110') },
        },
    },

    'checkBox_stop_ramp_en' : {
        'default' : True,
        'values' : {
            False : {'value' : bitarray('00') },
            True  : {'value' : bitarray('01') },
        },
    },

    'checkBox_counter_en' : {
        'default' : True,
        'values' : {
            False : {'value' : bitarray('1') },
            True  : {'value' : bitarray('0') },
        },
    },

    'checkBox_tac_refresh_en' : {
        'default' : True,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },

    'checkBox_fetp_enable' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
}

channel_data = {
    'comboBox_trigger_mode_1' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : 'Normal trigger using discriminators’ output.'},
            1 : {'value': bitarray('01'),
                 'text' : 'All discriminators are replaced by test_pulse.'},
            2 : {'value': bitarray('10'),
                 'text' : 'All discriminators are inverted.'},
            3 : {'value': bitarray('11'),
                 'text' : 'Channel disabled.'},
        },
    },

    'comboBox_debug_mode' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : 'Data'},
            1 : {'value': bitarray('00'),
                 'text' : '0'},
            2 : {'value': bitarray('10'),
                 'text' : "if tx1 (do_E) else if tx2 (do_T2) else if tx3 (do_T1')"},
            3 : {'value': bitarray('11'),
                 'text' : "if tx1 (Trigger_B) else if tx2 (Trigger_E) else if tx3 (Trigger_T')"},
        },
    },

    'comboBox_sync_chain_length' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '0b00'},
        },
    },

    'comboBox_dead_time' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('000000'),
                 'text' : '0b000000'},
        },
    },

    'comboBox_counter_mode' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0000'),
                 'text' : 'Never count. If count_en is 0b1, the transmitted value is always zero.'},
            1 : {'value': bitarray('0001'),
                 'text' : 'Always count. If count_en is 0b1, the transmitted value should be min {counting period, 2^24}−1'},
            2 : {'value': bitarray('0010'),
                 'text' : 'Count valid events.'},
            3 : {'value': bitarray('0011'),
                 'text' : 'Count invalid events.'},
            4 : {'value': bitarray('1000'),
                 'text' : 'Count all events.'},
            5 : {'value': bitarray('1100'),
                 'text' : 'Count numer of rising edges in trigger_B.'},
            6 : {'value': bitarray('1111'),
                 'text' : 'Count number of cycles during which trigger_B is active.'},
        },
    },

    'comboBox_tac_max_age' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('11110'),
                 'text' : '0b11110'},
        },
    },

    'comboBox_tac_min_age' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('01010'),
                 'text' : '0b01010'},
        },
    },

    'comboBox_trigger_mode_2_t' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : 'do_T 1’'},
            1 : {'value': bitarray('01'),
                 'text' : 'do_T1′ · do_T2 (nominal)'},
            2 : {'value': bitarray('10'),
                 'text' : 'do_T1′ · do_E'},
        },
    },

    'comboBox_trigger_mode_2_e' : {
        'default' : 2,
        'values' : {
            0 : {'value': bitarray('000'),
                 'text' : 'do_T1(negado)'},
            1 : {'value': bitarray('001'),
                 'text' : 'do_T2(negado)'},
            2 : {'value': bitarray('010'),
                 'text' : 'do_E (nominal)(negado)'},
            3 : {'value': bitarray('011'),
                 'text' : 'do_T1′ · do_T2 (negado)'},
            4 : {'value': bitarray('100'),
                 'text' : 'do_T1′ ·do_E (negado)'},
            5 : {'value': bitarray('101'),
                 'text' : 'do_T1′'},
            6 : {'value': bitarray('110'),
                 'text' : 'do_T2'},
            7 : {'value': bitarray('111'),
                 'text' : 'do_E'},
        },
    },

    'comboBox_trigger_mode_2_q' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : 'do_T 1’'},
            1 : {'value': bitarray('01'),
                 'text' : 'do_T2 (nominal)'},
            2 : {'value': bitarray('10'),
                 'text' : 'do_E'},
        },
    },

    'comboBox_trigger_mode_2_b' : {
        'default' : 5,
        'values' : {
            0 : {'value': bitarray('000'),
                 'text' : 'do_T1′'},
            1 : {'value': bitarray('001'),
                 'text' : 'do_T2'},
            2 : {'value': bitarray('010'),
                 'text' : 'do_E'},
            3 : {'value': bitarray('011'),
                 'text' : 'do_T1′do_T2'},
            4 : {'value': bitarray('100'),
                 'text' : 'do_T1′+do_E'},
            5 : {'value': bitarray('101'),
                 'text' : 'do_T1′ + do_T2 + do_E (nominal)'},
        },
    },

    'comboBox_branch_en_eq' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1'),
                 'text' : '0b1'},
        },
    },

    'comboBox_branch_en_t' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1'),
                 'text' : '0b1'},
        },
    },

    'comboBox_qdc_mode' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : 'Time and charge (QDC) mode.'},
            1 : {'value': bitarray('1'),
                 'text' : 'Dual time (ToT) mode.'},
        },
    },

    'comboBox_trigger_b_latched' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : '0b0'},
        },
    },

    'comboBox_min_intg_time' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0100010'),
                 'text' : '0b0100010'},
        },
    },

    'comboBox_max_intg_time' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0100010'),
                 'text' : '0b0100010'},
        },
    },

    'comboBox_output_en' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '0b00'},
        },
    },

    'comboBox_qtx2_en' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : '0b0'},
        },
    },

    'comboBox_baseline_t' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('111101'),
                 'text' : '0b111101'},
        },
    },

    'comboBox_vth_t1' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('111000'),
                 'text' : '0b111000'},
        },
    },

    'comboBox_vth_t2' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('101111'),
                 'text' : '0b101111'},
        },
    },

    'comboBox_vth_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('010011'),
                 'text' : '0b010011'},
        },
    },

    'comboBox_baseline_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('110'),
                 'text' : '0b110'},
        },
    },

    'comboBox_fe_delay' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('01101'),
                 'text' : '3 ns'},
            1 : {'value': bitarray('01110'),
                 'text' : '6 ns'},
            2 : {'value': bitarray('01111'),
                 'text' : '8 ns'},
            3 : {'value': bitarray('10000'),
                 'text' : 'Delay line bypassed'},
        },
    },

    'comboBox_postamp_gain_t' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '3000Ω (Transimpedance gain (T))'},
            1 : {'value': bitarray('10'),
                 'text' : '1500Ω  (Transimpedance gain (T))'},
            2 : {'value': bitarray('01'),
                 'text' : '750Ω  (Transimpedance gain (T))'},
            3 : {'value': bitarray('11'),
                 'text' : '375Ω  (Transimpedance gain (T))'},
        },
    },

    'comboBox_postamp_gain_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : ' 300Ω (Transimpedance gain (T))'},
            1 : {'value': bitarray('10'),
                 'text' : '150Ω  (Transimpedance gain (T))'},
            2 : {'value': bitarray('01'),
                 'text' : '75Ω  (Transimpedance gain (T))'},
            3 : {'value': bitarray('11'),
                 'text' : '38Ω  (Transimpedance gain (T))'},
        },
    },

    'comboBox_postamp_sh_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '0b00'},
        },
    },

    'comboBox_intg_en' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : 'Time and charge (QDC) mode.'},
            1 : {'value': bitarray('1'),
                 'text' : 'Dual time (ToT) mode.'},
        },
    },

    'comboBox_intg_signal_en' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0'),
                 'text' : 'Time and charge (QDC) mode.'},
            1 : {'value': bitarray('1'),
                 'text' : 'Dual time (ToT) mode.'},
        },
    },

    'comboBox_att' : {
        'default' : 1,
        'values' : {
            0 : {'value': bitarray('000'),
                 'text' : '1.00 (Integrator gain (GQ1))'},
            1 : {'value': bitarray('001'),
                 'text' : '0.32 (Integrator gain (GQ1))'},
            2 : {'value': bitarray('010'),
                 'text' : '1.82 (Integrator gain (GQ1))'},
            3 : {'value': bitarray('011'),
                 'text' : '0.60 (Integrator gain (GQ1))'},
            4 : {'value': bitarray('100'),
                 'text' : '1.65 (Integrator gain (GQ1))'},
            5 : {'value': bitarray('101'),
                 'text' : '0.47 (Integrator gain (GQ1))'},
            6 : {'value': bitarray('110'),
                 'text' : '2.25 (Integrator gain (GQ1))'},
            7 : {'value': bitarray('111'),
                 'text' : '0.65 (Integrator gain (GQ1))'},
        },
    },

    'comboBox_tdc_current_t' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0000'),
                 'text' : '0b0000'},
        },
    },

    'comboBox_tdc_current_e' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0000'),
                 'text' : '0b0000'},
        },
    },

    'comboBox_fe_tp_en' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '0b00'},
        },
    },

    'comboBox_integ_source_sw' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '1.00 (Integrator gain GQ2 and bias)'},
            1 : {'value': bitarray('01'),
                 'text' : '1.23 (Integrator gain GQ2 and bias)'},
            2 : {'value': bitarray('10'),
                 'text' : '1.47 (Integrator gain GQ2 and bias)'},
            3 : {'value': bitarray('11'),
                 'text' : '1.68 (Integrator gain GQ2 and bias)'},
        },
    },

    'comboBox_t1_hysteresis' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('010'),
                 'text' : '0b010'},
        },
    },

    'comboBox_t2_hysteresis' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('010'),
                 'text' : '0b010'},
        },
    },

    'comboBox_e_hysteresis' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('010'),
                 'text' : '0b010'},
        },
    },

    'comboBox_hysteresis_en_n' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('1'),
                 'text' : '0b1'},
        },
    },
}


temperature_data = {
    'checkBox_Temp_RST' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_Start' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_RD_Control_EN2' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_RD_Control_FA' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_RD_Control_SPD' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_RD_Control_IM' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_RD_Control_FB' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'checkBox_Temp_RD_Control_SGL' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    'spinBox_Temp_Time' : {
        'default' : 41943000,
    },
    'comboBox_Temp_CH_Sel' : {
        'default' : 0,
        'values' : {
            0 : {'value': bitarray('0000'),
                 'text' : 'CH 0'},
            1 : {'value': bitarray('0001'),
                 'text' : 'CH 1'},
            2 : {'value': bitarray('0010'),
                 'text' : 'CH 2'},
            3 : {'value': bitarray('0011'),
                 'text' : 'CH 3'},
            4 : {'value': bitarray('0100'),
                 'text' : 'CH 4'},
            5 : {'value': bitarray('0101'),
                 'text' : 'CH 5'},
            6 : {'value': bitarray('0110'),
                 'text' : 'CH 6'},
            7 : {'value': bitarray('0111'),
                 'text' : 'CH 7'},
            8 : {'value': bitarray('1000'),
                 'text' : 'CH 8'},
        },
    },
}


power_control_data = {
    "checkBox_PWR_GStart" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_Start" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_RST" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_18DIS" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_25EN" : {
        'default' : True,
        'values' : {
            False : {'value' : bitarray('00') },
            True  : {'value' : bitarray('11') },
        },
    },
    "checkBox_PWR_TOFPET_VCCEN" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('00000000') },
            True  : {'value' : bitarray('11111111') },
        },
    },
    "checkBox_PWR_TOFPET_VCC25EN" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('00000000') },
            True  : {'value' : bitarray('11111111') },
        },
    },
}

power_status_data = {
    "checkBox_PWR_STATUS_CONF_DONE" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_CONF_ON" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_18DIS" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_25EN_1" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_25EN_2" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_0" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_1" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_2" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_3" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_4" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_5" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_6" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCCEN_7" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_0" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_1" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_2" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_3" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_4" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_5" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_6" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
    "checkBox_PWR_STATUS_TOFPET_VCC25EN_7" : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
}
