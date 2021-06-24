from . worker import Worker

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


def start_periodic_tasks(window):
    def fn():
        stop_periodic_tasks(window)()
        temp_period = window.spinBox_TempMonitor_period.value()
        temp_min    = window.spinBox_TempMonitor_min.value()
        temp_max    = window.spinBox_TempMonitor_max.value()

        tofpets_to_monitor = np.where([
            window.checkBox_TempMonitor_0.isChecked(),
            window.checkBox_TempMonitor_1.isChecked(),
            window.checkBox_TempMonitor_2.isChecked(),
            window.checkBox_TempMonitor_3.isChecked(),
            window.checkBox_TempMonitor_4.isChecked(),
            window.checkBox_TempMonitor_5.isChecked(),
            window.checkBox_TempMonitor_6.isChecked(),
            window.checkBox_TempMonitor_7.isChecked(),
        ])[0]


        print(temp_period, temp_min, temp_max)
        window.periodic_worker = Worker(period=temp_period, min=temp_min, max=temp_max,
                                        tofpets=tofpets_to_monitor, window=window)
        window.periodic_worker.signals.alert.connect(show_popup)
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


def show_popup(message):
    print(message)
    msg = QMessageBox()
    msg.setWindowTitle("Temperature alert!")
    msg.setText(message)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setInformativeText("The power regulator for that TOFPET has been turn off")
    msg.exec_()

