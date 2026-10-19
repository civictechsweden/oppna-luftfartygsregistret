import html
from selectolax.lexbor import LexborHTMLParser


class Parser(object):

    @staticmethod
    def parse_csrf_token(response):
        htmlData = html.unescape(response.decode("utf-8"))
        tree = LexborHTMLParser(htmlData)

        form = tree.css_first(
            'form[id="form0"] > input[name="__RequestVerificationToken"]'
        )

        return form.attributes["value"]

    @staticmethod
    def parse_aircraft_list(response):
        htmlData = html.unescape(response.decode("utf-8"))
        tree = LexborHTMLParser(htmlData)

        if "Runtime Error" in htmlData:
            print("Server error")
            return
        elif tree.css_first("p.help-block"):
            amount = tree.css_first("p.help-block").text().replace(" luftfartyg", "")
        else:
            amount = 1

            print("Parsed a list of 1 aircraft.")

            aircraft_details = Parser.parse_aircraft_details(response)

            return {aircraft_details["code"]: aircraft_details["Luftfartygstyp"]}

        print("Parsed a list of {} aircrafts.".format(amount))

        aircrafts = {}

        for tr in tree.css("tbody > tr"):
            regno = tr.css_first("a.open-aircraft").attributes["regno"]
            model = tr.css_first("td.col-md-7").text().strip()
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
        raw_text = response.decode("utf-8")
        raw_text = raw_text.replace("<br>", "")
        raw_text = raw_text.replace("<br />", "")

        htmlData = html.unescape(raw_text)
        tree = LexborHTMLParser(htmlData)

        if tree.css_first("h2 > strong"):
            code = tree.css_first("h2 > strong").text()
        else:
            print("Server error")
            return

        aircraft_result = {"code": code}

        # Lexbor inserts the implicit tbody that browsers use for bare table rows.
        trs = tree.css("table.table > tr, table.table > tbody > tr")

        for tr in trs:
            key = tr.css_first("td.col-md-3 > strong").text()
            value = tr.css_first("td.col-md-9").text()
            aircraft_result[key] = value if value else None

        owners = []

        tags = ["div.row.ts-row-align", "div.col-sm-12.col-xs-12", "div"]
        for div in tree.css(">".join(tags)):

            tag_list = list(div.iter(include_text=True))

            i = -1

            for tag in tag_list:
                if tag.tag == "label":
                    i += 1
                    owners.append(
                        {
                            "type": tag.text(),
                            "id": None,
                            "name": "ANONYMOUS",
                            "address": None,
                            "since": None,
                        }
                    )

                if tag.tag == "a":
                    owners[i]["id"] = int(tag.attributes["ownerid"])
                    owners[i]["name"] = tag.css_first("strong").text()

                if tag.is_text_node:
                    text = tag.text()

                    if text.strip() and "privatperson" not in text:
                        address, _, since = text.strip().partition("Från och med ")

                        address = " ".join(
                            line.strip() for line in address.split("\n") if line.strip()
                        )

                        owners[i]["address"] = address
                        owners[i]["since"] = since

        owners = sorted(
            owners, key=lambda d: d["id"] if d["id"] is not None else float("inf")
        )

        aircraft_result["owners"] = owners

        print("Parsed details of aircraft {}.".format(code))
        return aircraft_result

    def parse_aircrafts_details(responses):
        register = list(map(Parser.parse_aircraft_details, responses))
        register = [a for a in register if a is not None]
        return sorted(register, key=lambda d: d["code"])
