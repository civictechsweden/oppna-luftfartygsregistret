from string import ascii_lowercase

from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

from services.parser import Parser

URL = "https://etjanster-luftfart.transportstyrelsen.se/sv-se/sokluftfartyg"


class Downloader(object):

    def __init__(self):
        self.s = FuturesSession(max_workers=30)
        self.csrf_token = self.get_csrf_token()

    def params(self, code=""):
        return {
            "Type MIME": "application/x-www-form-urlencoded; charset=UTF-8",
            "selection": "regno",
            "regno": code,
            "owner": "",
            "part": "",
            "item": "",
            "X-Requested-With": "XMLHttpRequest",
            "__RequestVerificationToken": self.csrf_token,
        }

    def get_csrf_token(self):
        return Parser.parse_csrf_token(self.s.get(URL).result().content)

    def fetch_aircraft_list_with_code(self, code):

        print(f"Fetching aircraft(s) for code {code}")

        future = self.s.post(URL, data=self.params(code))
        future.code = code
        return future

    def fetch_aircraft_list(self):
        print("Fetching all aircrafts")

        alphabet = list(range(0, 10)) + list(ascii_lowercase)

        futures = [self.fetch_aircraft_list_with_code(letter) for letter in alphabet]

        i = 0
        for future in as_completed(futures):
            i += 1
            print(
                f"Fetched aircrafts starting with letter {future.code} ({i}/{len(futures)})"
            )

        return [future.result().content for future in futures]

    def fetch_aircrafts_with_details(self, codes):
        futures = [self.fetch_aircraft_list_with_code(code) for code in codes]

        i = 0
        for future in as_completed(futures):
            i += 1
            print(f"Fetched aircraft details of {future.code} ({i}/{len(futures)})")

        return [future.result().content for future in futures]
