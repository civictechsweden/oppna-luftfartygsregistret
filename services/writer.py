import pandas as pd
import json


class Writer(object):
    @staticmethod
    def normalize_aircraft_keys(aircraft):
        """Convert Swedish keys to English machine-friendly keys."""
        key_mapping = {
            "code": "reg",
            "Avregistrerad": "dereg_date",
            "Orsak": "dereg_reason",
            "Land": "export_country",
            "Luftfartygstyp": "type",
            "Tillverkningsnummer": "msn",
            "Tillverkningsår": "built_year",
            "Max startvikt (kg)": "mtow_kg",
            "Luftvärdighetshandling giltig t.o.m.": "airworthiness_valid",
            "Registreringsdatum": "reg_date",
        }

        normalized = {}
        for key, value in aircraft.items():
            new_key = key_mapping.get(key, key)
            normalized[new_key] = value

        return normalized

    @staticmethod
    def write_json(data, filename):
        # Handle both single aircraft dict and list of aircraft dicts
        if isinstance(data, dict):
            data = [data]

        # Normalize keys for each aircraft
        normalized_data = [Writer.normalize_aircraft_keys(aircraft) for aircraft in data]

        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(normalized_data, fp, ensure_ascii=False, indent=4)

    def write_csv(register, filename):
        aircraft_columns = [
            "reg",
            "dereg_date",
            "dereg_reason",
            "export_country",
            "type",
            "msn",
            "built_year",
            "mtow_kg",
            "airworthiness_valid",
            "reg_date",
            "owners_amount",
        ]

        owner_columns = [
            f"owner.{column}" for column in ["type", "id", "name", "address", "since"]
        ]

        for aircraft in register:
            if aircraft["owners"] == []:
                aircraft["owners"].append(
                    {"type": "", "id": None, "name": "", "address": "", "since": ""}
                )

        df = pd.json_normalize(
            register,
            record_path=["owners"],
            record_prefix="owner.",
            meta=aircraft_columns,
            errors="ignore",
        )

        if df.empty:
            df = pd.json_normalize(register)
            df = df[aircraft_columns]
            df[owner_columns] = ""
        else:
            df = df[aircraft_columns + owner_columns]

        df.to_csv(filename, index=False)
