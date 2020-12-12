import json


class JsonWriter:
    def __init__(self, file_name):
        self._file_name = file_name

    def write(self, data, mode='w'):
        if type(data) is not dict:
            data = data.__dict__
        with open(self._file_name, mode) as json_file:
            json.dump(data, json_file, indent=4)

    def update(self, index, key, value):
        with open(self._file_name, 'r+') as json_file:
            data = json.load(json_file)
            data[index][key] = value
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()


class JsonReader:
    def __init__(self, path):
        self._file = open(path)

    def read(self):
        return json.load(self._file)

    def close(self):
        self._file.close()
