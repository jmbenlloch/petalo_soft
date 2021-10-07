from pymongo            import MongoClient
from bson.codec_options import TypeCodec
from bson.codec_options import TypeRegistry
from bson.codec_options import CodecOptions
from bitarray           import bitarray

from . worker import Worker
from subprocess import check_output

from datetime import datetime


class BitarrayCodec(TypeCodec):
    python_type = bitarray    # the Python type acted upon by this type codec
    bson_type   = str
    def transform_python(self, value):
        """Function that transforms a custom type value into a type
        that BSON can encode."""
        return "bitarray!" + value.to01()
    def transform_bson(self, value):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        result = value
        if value.startswith('bitarray!'):
            bits = value.split('!')[1]
            result = bitarray(bits)
        return result

bitarray_codec = BitarrayCodec()
type_registry  = TypeRegistry([bitarray_codec])
codec_options  = CodecOptions(type_registry=type_registry)

def store_in_mongodb(data):
    client = MongoClient()
    db     = client["petalo"]
    col = db.get_collection('configuration', codec_options=codec_options)
    col.insert_one(data)


def store_configuration_in_db(window):
    def fn(signals):
        global_config  = window.data_store.retrieve('global_config_mongo')
        channel_config = window.data_store.retrieve('channel_config')
        labels         = window.data_store.retrieve('labels')
        run_number     = get_run_number()
        data = {
            'run'            : int(run_number),
            'labels'         : labels,
            'start_time'     : datetime.now(),
            'global_config'  : {str(k) : v._asdict() for k, v in global_config.items()},
            'channel_config' : {str(asic) : {str(k) : v._asdict() for k, v in config.items()} \
                                for asic, config in channel_config.items()},
        }
        store_in_mongodb(data)

    worker = Worker(fn)
    window.threadpool.start(worker)


def get_run_number():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es cat /tmp/date_runnumber.txt'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
    return run_number



def mongodb_collection(col_name):
    client = MongoClient()
    db     = client["petalo"]
    col = db.get_collection(col_name)
    return col


def store_temperature(collection, tofpet_id, timestamp, temperature):
    data = {'tofpet_id'   : tofpet_id,
            'timestamp'   : timestamp,
            'temperature' : temperature}
    collection.insert_one(data)
