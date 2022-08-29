#import json
import luftfartygsregistret as lfr
from services.writer import Writer

print('Fetching all aircrafts in the register with their details')

register = lfr.get_aircrafts_with_details()

Writer.write_json(register, 'register.json')

#with open('register.json') as file_json:
#    register = json.load(file_json)

register_light = [lfr.remove_anonymous_owners(aircraft) for aircraft in register]

Writer.write_json(register, 'register_light.json')

Writer.write_csv(register_light, 'register.csv')

print('Fetched all aircrafts with their details')
