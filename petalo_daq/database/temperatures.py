from . worker import Worker
from ..windows.general import read_temperature

from subprocess import check_output

from datetime import datetime
import schedule
import time


def start_periodic_tasks(window):
    def fn(signals):
        schedule.every(2).seconds.do(read_temperature(window))

        while True:
            schedule.run_pending()
            time.sleep(1)

    worker = Worker(fn)
    window.threadpool_tasks.start(worker)

