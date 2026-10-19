from services.parser import Parser


def test_csrf_token_decodes_entities():
    page = b'<form id="form0"><input name="__RequestVerificationToken" value="a&amp;b"></form>'
    assert Parser.parse_csrf_token(page) == "a&b"


def test_aircraft_list_preserves_nested_text_and_swedish_characters():
    page = '''<p class="help-block">2 luftfartyg</p><table><tbody>
      <tr><td><a class="open-aircraft" regno="SE-ABC">SE-ABC</a></td>
          <td class="col-md-7"> Saab <strong>91</strong> Safir </td></tr>
      <tr><td><a class="open-aircraft" regno="SE-DEF">SE-DEF</a></td>
          <td class="col-md-7">Övningsflygplan</td></tr>
    </tbody></table>'''.encode()
    assert Parser.parse_aircraft_list(page) == {
        "SE-ABC": "Saab 91 Safir", "SE-DEF": "Övningsflygplan"
    }


DETAIL = '''<h2><strong>SE-ABC</strong></h2>
<table class="table"><tr><td class="col-md-3"><strong>Luftfartygstyp</strong></td>
  <td class="col-md-9">Saab <b>91</b></td></tr>
  <tr><td class="col-md-3"><strong>Anmärkning</strong></td><td class="col-md-9"></td></tr>
</table>
<div class="row ts-row-align"><div class="col-sm-12 col-xs-12"><div>
  <label>Ägare</label><a ownerid="2"><strong>Flyg &amp; Co</strong></a>
  Storgatan 1
  123 45 Örebro
  Från och med 2020-01-02
</div><div><label>Innehavare</label>privatperson</div></div></div>'''.encode()


def test_aircraft_details_preserve_table_rows_and_owners():
    assert Parser.parse_aircraft_details(DETAIL) == {
        "code": "SE-ABC", "Luftfartygstyp": "Saab 91", "Anmärkning": None,
        "owners": [
            {"type": "Ägare", "id": 2, "name": "Flyg & Co",
             "address": "Storgatan 1 123 45 Örebro", "since": "2020-01-02"},
            {"type": "Innehavare", "id": None, "name": "ANONYMOUS",
             "address": None, "since": None},
        ],
    }


def test_single_aircraft_list_uses_details_page():
    assert Parser.parse_aircraft_list(DETAIL) == {"SE-ABC": "Saab 91"}


def test_runtime_error_returns_none():
    assert Parser.parse_aircraft_list(b"<h1>Runtime Error</h1>") is None
    assert Parser.parse_aircraft_details(b"<h1>Runtime Error</h1>") is None
