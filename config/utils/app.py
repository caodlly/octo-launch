import json
from pathlib import Path
import os


class App:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self._json_file = os.path.join(self.BASE_DIR, "config/app.json")
        self._data = None
        self.read_file()

    def read_file(self):
        with open(self._json_file) as file:
            self._data = json.load(file)

    def __getattr__(self, query):
        data = self._data
        query = query.split("__")
        for q in query:
            data = data.get(q, None)
        return data
