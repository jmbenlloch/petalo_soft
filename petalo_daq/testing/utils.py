import re


def check_pattern_present_in_log(window, pattern, expected_matches, escape=True):
    if escape:
        pattern = re.escape(pattern)

    text = window.textBrowser.toPlainText()
    r = re.search(f'({pattern})', text, re.DOTALL)
    try:
        n_groups = len(r.groups())
    except AttributeError:
        n_groups = 0

    assert n_groups == expected_matches


def close_connection(window):
    end_connection_word = 0xfafafafa.to_bytes(length=4, byteorder='little')
    window.tx_queue.put(end_connection_word)
    window.tx_stopper.set()
    window.rx_stopper.set()
    window.thread_TXRX.join()
    #  window.rx_consumer.join()


