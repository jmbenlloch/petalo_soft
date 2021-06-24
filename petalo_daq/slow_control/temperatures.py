from . worker import Worker


def start_periodic_tasks(window):
    def fn():
        stop_periodic_tasks(window)()
        temp_period = window.spinBox_TempMonitor_period.value()
        temp_limit  = window.spinBox_TempMonitor_alert.value()
        print(temp_period)
        window.periodic_worker = Worker(period=temp_period, threshold=temp_limit, window=window)
        window.threadpool_tasks.start(window.periodic_worker)
    return fn


def stop_periodic_tasks(window):
    def fn():
        try:
            window.periodic_worker.monitor = False
        except:
            print("No periodic worker running")
    return fn


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """

    window.pushButton_TempMonitor_start.clicked.connect(start_periodic_tasks(window))
    window.pushButton_TempMonitor_stop .clicked.connect(stop_periodic_tasks (window))
