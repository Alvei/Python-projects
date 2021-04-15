""" Covid_requests.py
    Uses api.covid19api.com
"""
from collections import OrderedDict
from typing import Callable
from logicallayer import *

### Presentation Layer ###
def print_options(options: dict) -> None:
    """ Print all the options in a menu. """
    for shortcut, option in options.items():
        print(f"{shortcut}: {option}")


class Option:
    """ Wrapper for options in a menu. """

    def __init__(self, name: str, command: Callable, data=None):
        self.name = name  # Name of the command
        self.command = command  # Command to be executed
        self.data = data  # Data to pass to the command to execute

    def choose(self):
        """ Execute the commmand. """
        # print(f"In Choose {self.command} data: {self.data}")
        self.command.execute(self.data) if self.data else self.command.execute()

    def __str__(self):
        """ Overload operator to use with print_options(). """
        return self.name


def option_choice_is_valid(choice: str, options: dict) -> bool:
    return choice.upper() in options


def get_option(options: dict) -> str:
    """ Get input from user on which option they want to pursue. """
    choice = input("Choose an Option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid Choice")
        choice = input("Choose and Option: ")

    # Go through the dictionary to find the command
    chosen_option = options[choice.upper()]

    # Update the data as required
    if chosen_option.name == "Country":
        chosen_option.data = input("\nSelect country: ")

    elif chosen_option.name == "Display some preselected countries":
        chosen_option.data = [
            "Canada",
            "France",
            "United States of America",
            "United Kingdom",
            "Korea",
        ]
    return chosen_option


if __name__ == "__main__":
    chosen_countries = []
    country = "France"

    options = OrderedDict(
        {
            "C": Option("Country", GetCountryDataCommand(), country,),
            "G": Option("Global Summary", GetSummaryCommand(),),
            "L": Option(
                "Display some preselected countries",
                GetSomeCountriesCommand(),
                chosen_countries,
            ),
        }
    )

    print_options(options)
    choice = get_option(options)  # Returns a command
    choice.choose()


# # Get list of countries
# # endpoint = f"https://api.covid19api.com/countries"
# # response = get_requests_return_json(endpoint)
# # for item in response:
# #     print(item)
