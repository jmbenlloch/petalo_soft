def calibration_generator():
    for vth_t1 in range(0, 5):
        yield locals()

self.channels = [35, 36]
self.generator = calibration_generator()
