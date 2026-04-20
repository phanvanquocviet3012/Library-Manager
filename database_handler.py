import json
import os
from models import Book, Reader, Transaction

class DatabaseHandler:
    def __init__(self, file_path="data/library_data.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def save(self, books, readers, transactions, settings):
        data = {
            "books": {k: v.to_dict() for k, v in books.items()},
            "readers": {k: v.to_dict() for k, v in readers.items()},
            "transactions": [t.to_dict() for t in transactions],
            "settings": settings
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        default_settings = {"max_books": 5, "fine_per_day": 5000}
        if not os.path.exists(self.file_path): 
            return {}, {}, [], default_settings
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                books = {k: Book(**v) for k, v in data.get("books", {}).items()}
                readers = {k: Reader(**v) for k, v in data.get("readers", {}).items()}
                transactions = [Transaction(**t) for t in data.get("transactions", [])]
                settings = data.get("settings", default_settings)
                return books, readers, transactions, settings
        except Exception:
            return {}, {}, [], default_settings