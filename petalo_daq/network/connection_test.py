from PyQt5  import QtCore

from   time import sleep

from PETALO_v7                    import PetaloRunConfigurationGUI
from .. testing.utils             import close_connection


def test_connect_button(qtbot, petalo_test_server):
    window = PetaloRunConfigurationGUI(test_mode=True)
    close_connection(window)
    window.textBrowser.clear()

    window.textBrowser_Localhost    .setText('127.0.0.1')
    window.textBrowser_Petalo_server.setText('127.0.0.1')

    qtbot.mouseClick(window.pushButton_Connect, QtCore.Qt.LeftButton)
    assert window.checkBox_Connected.isChecked()
    close_connection(window)
    sleep(1)
