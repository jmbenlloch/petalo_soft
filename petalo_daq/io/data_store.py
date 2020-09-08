import json
from json import JSONEncoder
from bitarray import bitarray

class DataStore():
    """
    Class to centralize all the status data for the application.
    By keeping everything at the same place it is simpler to load configuration files
    and to export a given configuration.
    """
    data = {}

    def insert(self, name, value):
        """
        Function to store some particular variable with its corresponding value

        Parameters:
        name (string): Variable name
        value (Object): Value associated to "name"
        """
        if name in self.data:
            print(f"There is already a variable named {name}")
        self.data[name] = value
        print(name, value)

    def retrieve(self, name):
        """
        Function to get the value of some variable

        Parameters:
        name (string): Variable name

        Returns:
        Object: Value associated to "name".
        """
        return self.data[name]

    def export_to_json(self, fname):
        """
        Function to export all the variables stored to a json file

        Parameters:
        fname (string): Output file path
        """
        with open(fname, 'w') as fd:
            json.dump(self.data, fd, indent=2, separators=(',', ': '), cls=DataStoreJsonEncoder)




class DataStoreJsonEncoder(JSONEncoder):
    """
    JSON encoder for bitarray
    """

    def default(self, object):
        if isinstance(object, bitarray):
            return '{}'.format(object)
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)
