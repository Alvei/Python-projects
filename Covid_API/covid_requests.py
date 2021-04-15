""" Covid_requests.py
    Uses api.covid19api.com
    Programmed using functional programing
"""

import requests
from datetime import date, timedelta


def check_requests(response):
    """ Convenience function for error checking. """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"\nA HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"\ An Error Connecting: {errh}")
    except requests.exceptions.Timeout as errt:
        print(f"\n A Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"\nAn unknown Error: {err}")
    else:
        print(f"Succesful request")


def get_requests_return_json(endpoint: str, params=None):
    """ Get requests on endpoint and return json. """
    print(f"\nStarting the request")
    response = requests.get(endpoint, params=params, timeout=3)
    check_requests(response)
    return response.json()


today = date.today()
yesterday = today - timedelta(days=1)

country = "Canada"
# country = "United States of America"
# Could use status [confirmed, death, recovered]
endpoint = f"https://api.covid19api.com/country/{country}/status/confirmed"
params = {"from": str(yesterday), "to": str(today)}
response = get_requests_return_json(endpoint, params)

# Extract value from dict with key "Cases", default is zero case, then sum()
total_confirmed = sum([day.get("Cases", 0) for day in response])
print(f"Total confirmed Covid-19 cases in {country}: {total_confirmed:,}")

# Get summary
endpoint = f"https://api.covid19api.com/summary"
response = get_requests_return_json(endpoint)
countries = response["Global"]
print(f"\nGlobal Summary")
print("=" * 15)
for key, value in countries.items():
    if key != "Date":
        print(f"{key}:\t{value:,}")

# Check a few countries
countries = response["Countries"]
print(f"\n{len(countries)} countries")
chosen_countries = [
    "Canada",
    "France",
    "United States of America",
    "United Kingdom",
    "Korea",
]
for country in countries:
    if country["Country"] in chosen_countries:
        print("\n")
        for key, value in country.items():
            if not (key in ["ID", "CountryCode", "Slug", "Date", "Premium"]):
                print(f"{key}:\t{value}")


# Get list of countries
# endpoint = f"https://api.covid19api.com/countries"
# response = get_requests_return_json(endpoint)
# for item in response:
#     print(item)
