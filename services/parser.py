import html
from bs4 import BeautifulSoup


class Parser(object):

    @staticmethod
    def parse_csrf_token(response):
        htmlData = html.unescape(response.decode('utf-8'))
        soup = BeautifulSoup(htmlData, 'html.parser')

        form = soup.select_one('form[id="form0"] > input[name="__RequestVerificationToken"]')

        return form['value']

    @staticmethod
    def parse_aircraft_list(response):
        htmlData = html.unescape(response.decode('utf-8'))
        soup = BeautifulSoup(htmlData, 'html.parser')

        if 'Runtime Error' in htmlData:
            print('Server error')
            return
        elif soup.select_one('p.help-block'):
            amount = soup.select_one('p.help-block').text.replace(
            ' luftfartyg', '')
        else:
            amount = 1

            print('Parsed a list of 1 aircraft.')

            aircraft_details = Parser.parse_aircraft_details(response)

            return { aircraft_details['code']: aircraft_details['Luftfartygstyp'] }

        print('Parsed a list of {} aircrafts.'.format(amount))

        aircrafts = {}

        for tr in soup.select('tbody > tr'):
            regno = tr.select_one('a.open-aircraft')['regno']
            model = tr.select_one('td.col-md-7').text.strip()
            aircrafts[regno] = model

        return aircrafts

    @staticmethod
    def parse_aircraft_lists(responses):
        aircraft_list = {}

        for response in responses:
            aircraft_list |= Parser.parse_aircraft_list(response)

        return {key: value for key, value in sorted(aircraft_list.items())}


    @staticmethod
    def parse_aircraft_details(response):
        raw_text = response.decode('utf-8')
        raw_text = raw_text.replace('<br>', '')
        raw_text = raw_text.replace('<br />', '')

        htmlData = html.unescape(raw_text)
        soup = BeautifulSoup(htmlData, 'html.parser')

        if soup.select_one('h2 > strong'):
            code = soup.select_one('h2 > strong').text
        else:
            print('Server error')
            return

        aircraft_result = {'code': code}

        trs = soup.select('table.table > tr')

        for tr in trs:
            key = tr.select_one('td.col-md-3 > strong').text
            value = tr.select_one('td.col-md-9').text
            aircraft_result[key] = value if value else None

        owners = []

        for div in soup.select('>'.join(
            ['div.row.ts-row-align', 'div.col-sm-12.col-xs-12', 'div'])):

            tag_list = list(div.children)

            i = -1

            for tag in tag_list:
                if tag.name == 'label':
                    i += 1
                    owners.append({
                        'type': tag.text,
                        'id': None,
                        'name': 'ANONYMOUS',
                        'address': None,
                        'since': None
                    })

                if tag.name == 'a':
                    owners[i]['id'] = int(tag['ownerid'])
                    owners[i]['name'] = tag.select_one('strong').text

                if tag.name is None:
                    text = tag.text

                    if text.strip() and 'privatperson' not in text:
                        address, _, since = text.strip().partition(
                            'Från och med ')

                        address = ' '.join(line.strip()
                                           for line in address.split('\n')
                                           if line.strip())

                        owners[i]['address'] = address
                        owners[i]['since'] = since

        owners = sorted(owners, key=lambda d: d['id'] if d['id'] is not None else float('inf'))

        aircraft_result['owners'] = owners

        print('Parsed details of aircraft {}.'.format(code))
        return aircraft_result

    def parse_aircrafts_details(responses):
        register = list(map(Parser.parse_aircraft_details, responses))
        register = [a for a in register if a is not None]
        return sorted(register, key=lambda d: d['code'])
