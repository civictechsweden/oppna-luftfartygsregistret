from concurrent.futures import as_completed
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from urllib3.util import Retry

URL = 'https://sle-p.transportstyrelsen.se/extweb/sv-se/sokluftfartyg'

def params(code=''):
        if not code:
            code = ''
        return {
                    'Type MIME': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'selection': 'regno',
                    'regno': code,
                    'owner': '',
                    'part': '',
                    'item': '',
                    'X-Requested-With': 'XMLHttpRequest'
                }

class Downloader(object):

    def __init__(self):
        adapter = HTTPAdapter(max_retries=Retry(total=10, backoff_factor=0.1))

        self.s = FuturesSession(max_workers=30)
        self.s.mount('https://', adapter)

    def fetch_aircrafts_with_code(self, code=''):
        if not code:
            print(f'Fetching all aircrafts')
        else:
            print(f'Fetching aircraft(s) for code {code}')

        future = self.s.post(URL, data=params(code))
        future.code = code
        return future

    def fetch_all_aircrafts(self):
        return Downloader.fetch_aircrafts_with_code()

    def fetch_aircrafts_with_details(self, codes):
        futures = [self.fetch_aircrafts_with_code(code) for code in codes]

        i = 0
        for future in as_completed(futures):
            i += 1
            print(f'Fetched aircraft details of {future.code} ({i}/{len(futures)})')

        return [future.result().content for future in futures]
