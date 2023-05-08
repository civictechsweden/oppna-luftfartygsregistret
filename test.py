import json
import luftfartygsregistret as lfr
from services.writer import Writer
from services.downloader import Downloader
from services.parser import Parser


# # aircraft_list = lfr.get_aircraft_list()
# aircraft_list = ['SE-BEB', 'SE-BEC', 'SE-BCL']

# print(Parser.parse_aircraft_list(Downloader().fetch_aircraft_list_with_code(0).result().content))

with open('register.json') as file_json:
   register = json.load(file_json)

register_light = [lfr.remove_anonymous_owners(aircraft) for aircraft in
register]

Writer.write_csv(register_light, 'register.csv')
