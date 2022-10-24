from pathlib import Path
from jsonschema.validators import validate
from json import load
from os.path import join


def validate_json_schema(response, name):
    def validate_json(resp, schema_name):
        root_dir = Path(__file__).parent.parent
        json_schema_path = join(root_dir, 'json_schema', schema_name + '.json')
        with open(json_schema_path) as file:
            json_file = load(file)
        try:
            validate(instance=resp, schema=json_file)
            return True
        except Exception as e:
            raise e

    assert validate_json(resp=response, schema_name=name), 'Ответ API не соответствует JSON схеме'
