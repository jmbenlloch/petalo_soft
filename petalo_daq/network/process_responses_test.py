import numpy as np

from .. network.process_responses import temperature_conversion_1
from .. network.process_responses import temperature_conversion_1_celsius
from .. network.process_responses import temperature_conversion_2


def test_temperature_conversion_1():
    samples = np.random.uniform(0.5, 2.5, 1000)

    for temperature in samples:
        value_temp = np.round((temperature - 1.65) * 2**23 / 1.65).astype(np.int32)
        value      = (value_temp << 5) | 0xE000001F
        temp_converted = temperature_conversion_1(value)

        np.testing.assert_almost_equal(temperature, temp_converted, decimal=4)


def test_temperature_conversion_1_celsius():
    # TODO add hypothesis
    # TODO define range of operation
    samples = np.random.uniform(-50, 150, 300)

    for temperature in samples:
        voltage = 1777.3 - (10.888 * (temperature-30)) - (0.00347 * (temperature-30)**2)
        temp_converted = temperature_conversion_1_celsius(voltage/1000)
        print(temperature, voltage, temp_converted)
        np.testing.assert_almost_equal(temperature, temp_converted, decimal=4)



def test_temperature_conversion_2():
    # TODO add hypothesis
    # TODO define range of operation
    samples = np.random.uniform(0, 0.8, 100)

    for temperature in samples:
        value_temp = np.round((temperature + 273) * 1570 * 32 / 3.3).astype(np.int32)
        value      = value_temp | 0xF0000000
        temp_converted = temperature_conversion_2(value)

        np.testing.assert_almost_equal(temperature, temp_converted, decimal=4)
