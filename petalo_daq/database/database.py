import pymysql
pymysql.install_as_MySQLdb()

def mysql_connect(host, user, password, database):
    connector = pymysql.connect(host, user, password, database)
    cursor    = connector.cursor()
    return connector, cursor

def get_latest_run_number(db_cursor):
    table = 'Runs'
    sql = 'SELECT * FROM {} ORDER BY run_number DESC LIMIT 1'.format(table)
    db_cursor.execute(sql)
    data = db_cursor.fetchone()
    run_number = 0
    if data:
        run_number = data[0]
    return run_number


def insert_run_number(connector, cursor, run_number):
    table = 'Runs'
    sql = 'INSERT INTO `{}` (`run_number`, `date`) VALUES ("{}", CURRENT_TIME()); '.format(table, run_number)
    cursor.execute(sql)
    connector.commit()


def insert_global_config(connector, cursor, run_number, daq_id, asic_id, global_bitarray, fields):
    # insert the whole configuration word
    sql = "INSERT INTO `GlobalConfiguration` (`run_number`, `daq_id`, `asic_id`, `param`, `value`) VALUES ('{}', '{}', '{}', '{}', '{}');"
    sql = sql.format(run_number, daq_id, asic_id, 'global_config', global_bitarray.to01())
    print(sql)
    cursor.execute(sql)
    connector.commit()

    #insert each field separately
    for field, bit_slice in fields.items():
        bits = global_bitarray[bit_slice]
        print(field, bit_slice, bits)

        sql = "INSERT INTO `GlobalConfiguration` (`run_number`, `daq_id`, `asic_id`, `param`, `value`) VALUES ('{}', '{}', '{}', '{}', '{}');"
        sql = sql.format(run_number, daq_id, asic_id, field, bits.to01())
        print(sql)
        cursor.execute(sql)
    connector.commit()


def insert_channel_config(connector, cursor, run_number, daq_id, asic_id, ch_id, channel_bitarray, fields):
    # insert the whole configuration word
    sql = "INSERT INTO `ChannelConfiguration` (`run_number`, `daq_id`, `asic_id`, `channel_id`, `param`, `value`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
    sql = sql.format(run_number, daq_id, asic_id, ch_id, 'channel_config', channel_bitarray.to01())
    print(sql)
    cursor.execute(sql)
    connector.commit()

    #insert each field separately
    for field, bit_slice in fields.items():
        bits = channel_bitarray[bit_slice]
        print(field, bit_slice, bits)

        sql = "INSERT INTO `ChannelConfiguration` (`run_number`, `daq_id`, `asic_id`, `channel_id`, `param`, `value`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
        sql = sql.format(run_number, daq_id, asic_id, ch_id, field, bits.to01())
        print(sql)
        cursor.execute(sql)
    connector.commit()
