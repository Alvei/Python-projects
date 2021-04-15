# API_requests.py
import requests


def check_requests(response):
    """ Convenience function for error checking for a requests call. """
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


class APIData:
    """ Gets data from the end points and convert into list. """

    def __init__(self, endpoint: str, params=None):
        """ Constructor. """
        self.endpoint = endpoint  # https location of API end point
        self.params = params  # payload to add to the requests
        self.parse_data = None  # data to be stored in the form of a list

    def get_requests_return_json(self):
        """ Get requests on endpoint and return json. """
        print(f"\nStarting the request")
        response = requests.get(self.endpoint, params=self.params, timeout=3)
        check_requests(response)
        self.parse_data = response.json()

