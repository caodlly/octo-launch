import json
from pathlib import Path
import os
import threading


class App:
    _instance = None
    _lock = threading.Lock()
    _data = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.setup()

    def setup(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self._json_file = os.path.join(self.BASE_DIR, "config/app.json")
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
