
#  @fixture(scope='session')
#  def database_connection():
#      conn, cursor = db.mysql_connect('localhost', 'root', 'root', 'petalo')
#      return conn, cursor
#
#  @mark.skip(reason="TBD")
#  def test_start_run(qtbot, database_connection):
#      window = MyApp()
#      qtbot.mouseClick(window.pushButton_reg_glob, QtCore.Qt.LeftButton)
#      qtbot.mouseClick(window.pushButton_reg_ch  , QtCore.Qt.LeftButton)
#      qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
#
#      print('\n\n\n\n run number:')
#      print(db.get_latest_run_number(database_connection[1]))
#      assert 0


# Check save to json
# Check load from json
# Check save to database

# define one config word and all the associated fields

@fixture()
def global_config():
    values = {
        'word' : '100000 00000 1 010011 11 0111 01101 110000 010011 111011 10111 1 0010 10010 101000 1110 110110 110000 111010 10011 00100 10111 111011 100011 00000 00001 10100 10111 11111 111001 101111 1 0 0 00 1001 1 110 0 00 00 110 1 000000 0 10 1 10',
        'fields' : {
            "tx_nlinks"         : '10',
            "tx_ddr"            : '1',
            "tx_mode"           : '10',
            "debug_mode"        : '0',
            "veto_mode"         : '000000',
            "tdc_clk_div"       : '1',
            "r_clk_en"          : '110',
            "stop_ramp_en"      : '00',
            "counter_en"        : '0',
            "counter_period"    : '110',
            "tac_refresh_en"    : '1',
            "tac_refresh_period": '1001',
            "data_clk_div"      : '00',
            "fetp_enable"       : '0',
            "input_polarity"    : '1',
            "attenuator_ls"     : '101111',
            "v_ref_diff_bias_ig": '111001',
            "v_cal_ref_ig"      : '11111',
            "fe_postamp_t"      : '10111',
            "fe_postamp_e"      : '10100',
            "v_cal_tp_top"      : '00001',
            "v_cal_diff_bias_ig": '00000',
            "v_att_diff_bias_ig": '100011',
            "v_integ_ref_ig"    : '111011',
            "imirror_bias_top"  : '10111',
            "tdc_comp_bias"     : '00100',
            "tdc_i_lsb"         : '10011',
            "disc_lsb_t1"       : '111010',
            "fe_ib2"            : '110000',
            "vdifffoldcas"      : '110110',
            "disc_vcas"         : '1110',
            "disc_lsb_e"        : '101000',
            "tdc_i_ref"         : '10010',
            "tdc_comp_vcas"     : '0010',
            "fe_ib2_x2"         : '1',
            "main_global_dac"   : '10111',
            "fe_ib1"            : '111011',
            "disc_ib"           : '010011',
            "disc_lsb_t2"       : '110000',
            "tdc_tac_vcas_p"    : '1101',
            "tdc_tac_vcas_n"    : '11',
            "adebug_out_mode"   : '010011',
            "tdc_global_dac"    : '1',
            "adebug_buffer"     : '00000',
            "disc_sf_bias"      : '100000',
        }
    }
    return values
