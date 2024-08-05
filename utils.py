import json

class JSONHandler:
    def __init__(self, filename='response.json'):
        self.filename = filename

    def write_json(self, data):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Data successfully written to {self.filename}")
        except Exception as e:
            print(f"Error writing to JSON file: {e}")