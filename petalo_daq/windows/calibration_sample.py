def calibration_generator():
    for vth_t1 in range(0, 5):
        yield locals()

self.channels = [35, 36]
self.generator = calibration_generator()


def calibration_generator():
    vth_t1 = 62
    vth_t2 = 62
    trigger_mode_2_b = 0 # T1
    counter_mode = 6 # Count number of cycles during which trigger_B is active
    for baseline_t in range(0, 62):
        yield locals()

self.channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
self.generator = calibration_generator()

