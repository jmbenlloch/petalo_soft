def print_progress(window):
    def fn(status):
        # Limit size
        text = window.plainTextEdit_calibrationLog.toPlainText()
        nlines = len(text.split('\n'))
        if nlines > 300:
            window.plainTextEdit_calibrationLog.clear()

        window.plainTextEdit_calibrationLog.insertPlainText(status)
    return fn


