import pandas as pd
import json


class Writer(object):
    @staticmethod
    def write_json(dict, filename):
        with open(filename, 'w') as fp:
            json_string = json.dumps(dict, ensure_ascii=False,
                                     indent=4).encode('utf-8')
            fp.write(json_string.decode())

    def write_csv(dict, filename):
        aircraft_columns = list(dict[0].keys())[:-1]
        owner_columns = [f'owner.{column}' for column in ['type', 'id', 'name', 'address', 'since']]

        for aircraft in dict:
            if aircraft['owners'] == []:
                aircraft['owners'].append({
                "type": "",
                "id": None,
                "name": "",
                "address": "",
                "since": ""
            })

        df = pd.json_normalize(dict,
                               record_path = ['owners'],
                               record_prefix = "owner.",
                               meta = aircraft_columns,
                               errors = 'ignore')

        if df.empty:
            df = pd.json_normalize(dict)
            df = df[aircraft_columns]
            df[owner_columns] = ''
        else:
            df = df[aircraft_columns + owner_columns]

        df.to_csv(filename)
