import csv
import os


class CSVWriter:
    def __init__(self, file_name, field_names):
        self._file_name = file_name
        if not os.path.exists(self._file_name):
            self.write(field_names)

    def write(self, data):
        with open(self._file_name, mode='a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)


class CSVReader:
    def __init__(self, file_name):
        self._file_name = file_name

    def read(self):
        data = []
        with open(self._file_name, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
        return data
