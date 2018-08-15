import json


def read(conf='config.json'):
    try:
        with open(conf) as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        return False


def write(data, conf='config.json'):
    try:
        with open(conf, 'w') as json_file:
            json_file.write(json.dumps(data))
    except Exception:
        return False


def read_db(path):
    try:
        with open(path) as json_file:
            a = json_file
            return a
            pass
    except Exception:
        return False
