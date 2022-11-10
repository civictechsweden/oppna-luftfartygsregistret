import json
from services.downloader import Downloader
from services.parser import Parser

def get_aircraft_list(code=None, downloader=Downloader()):
    if code:
        return Parser.parse_aircraft_list(downloader.fetch_aircraft_list_with_code(code))

    return Parser.parse_aircraft_lists(downloader.fetch_aircraft_list())

def get_aircraft(code=None, downloader=Downloader()):
    return Parser.parse_aircraft_details(downloader.fetch_aircrafts_with_code(code).result().content)

def get_aircrafts_with_details_from_list(codes, downloader=Downloader()):
    return list(filter(None, Parser.parse_aircrafts_details(downloader.fetch_aircrafts_with_details(codes))))

def get_aircrafts_with_details_from_file(filename, downloader=Downloader()):
    with open(filename) as file_json:
        aircrafts = json.load(file_json)

    return get_aircrafts_with_details_from_list(aircrafts.keys(), downloader)

def get_aircrafts_with_details(code=None, downloader=Downloader()):
    aircrafts = get_aircraft_list(code, downloader)
    return get_aircrafts_with_details_from_list(list(aircrafts), downloader)

def remove_anonymous_owners(aircraft):
    if not aircraft or not 'owners' in aircraft:
        return aircraft

    non_anonymous_owners = []

    for owner in aircraft['owners']:
        if owner['type'] == 'Registrerad ägare' or owner[
                'type'] == 'Registrerad delägare':
            if owner['name'] != 'ANONYMOUS':
                non_anonymous_owners.append(owner)

    aircraft['owners_amount'] = len(aircraft['owners']) - 1
    aircraft.pop('owners', None)
    aircraft['owners'] = [
        dict(t) for t in {tuple(d.items())
                        for d in non_anonymous_owners}
    ]

    return aircraft


