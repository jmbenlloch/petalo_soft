from pytest import fixture
import threading
import logging

from petalo_daq.daq.mock_server.petalo_server import PetaloMockServer

@fixture(scope='session')
def petalo_test_server():
    petalo_server = PetaloMockServer()
    petalo_server.logger.setLevel(level=logging.CRITICAL)
    thread = threading.Thread(target=petalo_server.run)
    thread.daemon = True
    thread.start()
    yield petalo_server
