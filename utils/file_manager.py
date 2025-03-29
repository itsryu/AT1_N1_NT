import csv
import os

class FileManager:
    def __init__(self, filename, headers):
        self.filename = filename
        self.headers = headers
        self._create_file_if_not_exists()

    def _create_file_if_not_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def add_data(self, data):
        with open(self.filename, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(data)

    def load_data(self):
        data = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        return data

    def update_data(self, new_data):
        with open(self.filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(new_data)