import json
import jsonlines

class WriteJSON:

    def __init__(self, should_save_json=False):
        self.objects_to_save = []
        self.should_save_json = should_save_json

    def add_object(self, new_object):
        if self.should_save_json:
            self.objects_to_save.append(new_object)

    def save_json(self, name):
        if self.should_save_json:
            a = {}
            a.update({"data": self.objects_to_save})
            data = json.dumps(a, ensure_ascii=False)
            file_name = name + '.json_lines'
            with jsonlines.open(file_name, mode='w') as writer:
                writer.write(data)