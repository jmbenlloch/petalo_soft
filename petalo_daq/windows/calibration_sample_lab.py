##########
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

#######################################
# both baseline_t and T1

def calibration_generator():
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for vth in range(0, 63):
        for baseline_t in range(0, 63):
            for channel in channels:
                params = {
                        'channel' : channel,
                        'baseline_t' : baseline_t,
                        'vth_t1' : vth,
                        'vth_t2' : vth,
                        'trigger_mode_2_b' : 0, # T1
                        'counter_mode' : 6, # Count number of cycles during which trigger_B is active
                }
                yield params
            yield Calibration.config_done

self.generator = calibration_generator()

#######################################
# both baseline_t and T2

def calibration_generator():
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for vth in range(0, 63):
        for baseline_t in range(0, 63):
            for channel in channels:
                params = {
                        'channel' : channel,
                        'baseline_t' : baseline_t,
                        'vth_t1' : vth,
                        'vth_t2' : vth,
                        'trigger_mode_2_b' : 1, # T1
                        'counter_mode' : 6, # Count number of cycles during which trigger_B is active
                }
                yield params
            yield Calibration.config_done

self.generator = calibration_generator()

#######################################
# both baseline_e and E

def calibration_generator():
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for vth in range(0, 63):
        for baseline_e in range(0, 7):
            for channel in channels:
                params = {
                        'channel' : channel,
                        'baseline_e' : baseline_e,
                        'vth_e' : vth,
                        'trigger_mode_2_b' : 2, # E
                        'counter_mode' : 6, # Count number of cycles during which trigger_B is active
                }
                yield params
            yield Calibration.config_done

self.generator = calibration_generator()

#######################

def calibration_generator():
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for baseline_t in range(0, 63):
        for channel in channels:
            params = {
                'channel' : channel,
                'baseline_t' : baseline_t,
                'vth_t1' : 62,
                'vth_t2' : 62,
                'trigger_mode_2_b' : 1, # T2
                'counter_mode' : 6, # Count number of cycles during which trigger_B is active
            }
            yield params
        yield Calibration.config_done

self.generator = calibration_generator()

#######################

def calibration_generator():
    channels = [35,39,43,44,45,49,53,55,56,57,58,59,60,61,62,63]
    for vth_t1 in range(0, 63):
        for channel in channels:
            params = {
                'channel' : channel,
                'vth_t1' : vth_t1,
                'baseline_t' : 30,
                'vth_t2' : 62,
                'trigger_mode_2_b' : 0, # T1
                'counter_mode' : 6, # Count number of cycles during which trigger_B is active
            }
            yield params
        yield Calibration.config_done

self.generator = calibration_generator()

############################
# TPULSE
############################
def calibration_generator():
    for phase in range(0, 401, 20):
        for length in [0]:
            params = {
                'phase'  : phase,
                'length' : length,
            }
            yield params
            #  yield Calibration.config_done

self.generator = calibration_generator()

