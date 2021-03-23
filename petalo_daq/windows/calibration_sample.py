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



# Calibrate vth_t1

def calibration_generator():
    baseline_ts = {35: 46,
                   39: 62,
                   43: 34,
                   44: 62,
                   45: 39,
                   49: 45,
                   53: 62,
                   55: 45,
                   56: 36,
                   57: 62,
                   58: 62,
                   59: 62,
                   60: 62,
                   61: 41,
                   62: 43,
                   63: 50}
    baseline_ts = baseline_ts.values()
    vth_t1 = 62
    baseline_t = baseline_ts.pop(0)
    vth_t2 = 62
    trigger_mode_2_b = 0 # T1
    counter_mode = 6 # Count number of cycles during which trigger_B is active
    for vth_t1 in range(0, 62):
        yield locals()

self.channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
self.generator = calibration_generator()




##################

def calibration_generator():
    baseline_ts = {35: 46,
                   39: 62,
                   43: 34,
                   44: 62,
                   45: 39,
                   49: 45,
                   53: 62,
                   55: 45,
                   56: 36,
                   57: 62,
                   58: 62,
                   59: 62,
                   60: 62,
                   61: 41,
                   62: 43,
                   63: 50}
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for vth_t1 in range(0, 62):
        for channel in channels:
            params = {
                'channel' : channel,
                'vth_t1' : vth_t1,
                'baseline_t' : baseline_ts[channel],
                'vth_t2' : 62,
                'trigger_mode_2_b' : 0, # T1
                'counter_mode' : 6, # Count number of cycles during which trigger_B is active
            }
            yield params
        yield Calibration.config_done

self.generator = calibration_generator()


############

def calibration_generator():
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for baseline_t in range(0, 63):
        for channel in channels:
            params = {
                'channel' : channel,
                'baseline_t' : baseline_t,
                'vth_t1' : 62,
                'vth_t2' : 62,
                'trigger_mode_2_b' : 0, # T1
                'counter_mode' : 6, # Count number of cycles during which trigger_B is active
            }
            yield params
        yield Calibration.config_done

self.generator = calibration_generator()

