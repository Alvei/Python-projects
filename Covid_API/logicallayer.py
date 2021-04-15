# commands.py
from abc import ABC, abstractclassmethod
from datetime import date, timedelta
from collections import OrderedDict
from typing import Callable
from API_requests import check_requests, APIData


API_HTTP = "https://api.covid19api.com/"

### Logical Layer
class Command(ABC):
    @abstractclassmethod
    def execute(cls, data):
        raise NotImplementedError("Command must implement execute method.")


class GetCountryDataCommand(Command):
    def execute(self, country: str):
        """ Get and represent country data. """
        today = date.today()
        yesterday = today - timedelta(days=1)

        # country = "United States of America"
        # Could use status [confirmed, death, recovered]
        endpoint = f"{API_HTTP}country/{country}/status/confirmed"
        params = {"from": str(yesterday), "to": str(today)}
        response = APIData(endpoint, params)
        response.get_requests_return_json()

        # Extract value from dict with key "Cases", default is zero case, then sum()
        total_confirmed = sum([day.get("Cases", 0) for day in response.parse_data])
        print(f"Total confirmed Covid-19 cases in {country}: {total_confirmed:,}")


class GetSummaryCommand(Command):
    def execute(self, data=None):
        endpoint = f"{API_HTTP}summary"
        response = APIData(endpoint)
        response.get_requests_return_json()
        countries = response.parse_data["Global"]
        print(f"\nGlobal Summary")
        print("=" * 15)
        for key, value in countries.items():
            if key != "Date":
                print(f"{key}:\t{value:,}")


class GetSomeCountriesCommand(Command):
    def execute(self, chosen_countries: list):
        endpoint = f"{API_HTTP}summary"
        response = APIData(endpoint)
        response.get_requests_return_json()

        # Check a few countries
        countries = response.parse_data["Countries"]
        print(f"\n{len(countries)} countries")

        for country in countries:
            if country["Country"] in chosen_countries:
                print("\n")
                for key, value in country.items():
                    if not (key in ["ID", "CountryCode", "Slug", "Date", "Premium"]):
                        print(f"{key}:\t{value}")

