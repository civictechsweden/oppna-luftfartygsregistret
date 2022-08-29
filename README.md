# Öppna luftfartygsregistret

This python script can automatically fetch all or a predefined list of aircrafts registred in Sweden from the national aircraft register managed by Transportstyrelsen.

It exports the result as JSON or CSV. In JSON, there is a bigger file (`register.json` with all owner data, including those (unnammed) who are anonymous) and a "light" one (`register_light.json` with only non-anonymous owners). In CSV (`register.csv`), only the non-anonymous owners are kept and the aircrafts with several of them are represented on several lines.

On this repository, you can download the data directly. It is updated monthly by Github Actions on the 1st of every month at 1AM CET.

The register is updated continuously by Transportstyrelsen. The data made available by this hobby project might be outdated, or inaccurate.

License for the code is AGPL 3.0, license for the data is CC0 (but attribution is appreciated).

## Why?

In Sweden, the national aircraft register (luftfartygsregistret) is made publicly available through a rudimentary (as in old and non-user friendly) [search engine](https://sle-p.transportstyrelsen.se/extweb/sv-se/sokluftfartyg) by the national transport authority (Transportstyrelsen).

Unlike many other countries, the information isn't made available as open data (see for instance our neighbour [Finland](https://www.traficom.fi/sv/aktuellt/oppna-data?toggle=Luftfartyg)). Considering the Swedish government's poor motivation in opening its own data, the chance is small that this will happen in the near future.

Therefore, introducing Öppna luftfartygsregistret.

## Installation

- Install Python 3 on your machine if you don't already have it.

- Install the dependencies

```python
pip install -r requirements.txt
```

## Usage

- Import ***luftfartygsregistret*** and use one of its functions

```python
import luftfartygsregistret as lfr

# Getting a list of all planes in the register
aircraft_list = lfr.get_aircraft_list()

# Getting a list of all planes with 'R' in their
# registration code(registreringsbeteckning) in the register
aircraft_list_rh = lfr.get_aircraft_list('R')

# Getting details of a plane, here SE-RHJ, the private jet of billionnaire Göran Berglund
aircraft_details = lfr.get_aircraft('RHJ')

# Getting a list with the details of all planes in the register
all_aircrafts_with_details = lfr.get_aircrafts_with_details()
```

## Might be of interest

- This really good investigation by Dagens ETC: [Så flyger Sveriges förmögna med privatjet](https://www.etc.se/feature/saa-flyger-sveriges-foermoegna-med-privatjet).
- The [Wikipedia article](https://sv.wikipedia.org/wiki/Luftfartygsregistret) about the Swedish aircraft register. One can for instance learn that all private jets start with **SE-D** or **SE-R**.
