#!/usr/bin/env python

""" Use Option class to bind a name to a command in the logical layer.
    Presentation Layer.
"""
import os
from collections import OrderedDict
from typing import Dict, Optional, Callable, List, Union

import commands  # Import logical layer


def print_bookmarks(bookmarks: List) -> None:
    """ Prints the bookmarks. """
    for bookmark in bookmarks:
        print("\t".join(str(field) if field else "" for field in bookmark))


def format_bookmark(bookmark):
    """ XXX """
    return "\t".join(str(field) if field else "" for field in bookmark)


class Option:
    """Pattern: Hooks each menu option up to the command in the logical layer
    that it should trigger.
    """

    def __init__(
        self, name: str, command, prep_call: Callable = None, success_message="{result}"
    ) -> None:
        """Initialize the menu option with its key attributes.
        PARAMETERS:
            name: Name of the option
            command: An instance of the command to execute when .execute() is used
            prep_call: Optional preparation steps to call before executing the command
        """
        self.name = name
        self.command = command  # It is an instance of object from the logical layer
        self.prep_call = (
            prep_call  # Function used to gather data from users for specific command
        )
        self.success_message = success_message

    def _handle_message(self, message: Union[str, List]) -> None:
        """ Print the result of executing the command. """
        if isinstance(message, list):
            print_bookmarks(message)
        else:
            print(message)

    def choose(self):
        """ Will be called when the option chosen by the user. It should
            1- Run the preparation step if any
            2- Pass the return value from prep step to specified command.execute()
            3- Print the result of the execution 
            Either the success msg or bookmark results.
        """
        # message: contains the result of the command.execute().
        # It can be run with optional data from prep step
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data)

        formatted_result = ""

        if isinstance(result, list):
            for bookmark in result:
                formatted_result += "\n" + format_bookmark(bookmark)
        else:
            formated_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

    def __str__(self):
        """ Overload printing to allow printing the command name. """
        return self.name


def clear_screen() -> None:
    """ Clear screen function that works on windows NT and other OS. """
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)


def print_options(options: Dict) -> None:
    """ Print the dictionary of options. """
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice: str, options: Dict) -> bool:
    """ Check to see that choice is in options. """
    return choice in options or choice.upper() in options


def get_option_choice(options) -> Option:
    """Get valid user input from the various options provided.
    PARAMETERS: Ordered Dictionary of options
    RETURN: Option instance/object associated with the key input
    """
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> Optional[str]:
    """Get input from users. Default behavior is requiring a valid input.
    PARAMETERS:
      label: string to be printed when asking for user input
      required: if input is optional, specify False
    OUTPUTS:
      value: returns a string that was gathered from users or None
    """

    # OR is used to convert False to None to be used in while loop
    # 'A' OR None => 'A', False OR None => None
    value = input(f"{label}: ") or None

    # Loop if an input is required and value is currently None
    while required and not value:
        value = input(f"{label}: ") or None

    return value


def get_new_bookmark_data() -> Dict:
    """ Get the bookmark data from user. """
    return {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False),
    }


def get_bookmark_id_for_deletion() -> Optional[str]:
    """ Get ID to delete. """
    return get_user_input("Enter a bookmark ID to delete ")


def get_github_import_options() -> dict:
    """ Get info on github request. """
    return {
        "github_username": get_user_input("GitHub username"),
        "preserve_timestamps": get_user_input(  #
            "Preserve timestamps [Y/n]", required=False
        )
        in {"Y", "y", None},
    }


def get_new_bookmark_info() -> dict:
    """ Allows editing of bookmarks. """
    bookmark_id = get_user_input("Enter a bookmark ID to edit")
    field = get_user_input("Choose a value to edit (title, URL, notes)")
    new_value = get_user_input(f"Enter the new value for {field}")
    return {
        "id": bookmark_id,
        "update": {field: new_value},
    }


def loop():
    """ Main loop for the program. """
    clear_screen()

    # Initiate an object as the value for each key:value pair
    options = OrderedDict(
        {
            "A": Option(
                "Add a bookmark",
                commands.AddBookmarkCommand(),
                prep_call=get_new_bookmark_data,
                success_message="Bookmark added!",
            ),
            "B": Option("List bookmarks by date", commands.ListBookmarksCommand(),),
            "T": Option(
                "List bookmarks by title",
                commands.ListBookmarksCommand(order_by="title"),
            ),
            "E": Option(
                "Edit a bookmark",
                commands.EditBookmarkCommand(),
                prep_call=get_new_bookmark_info,
                success_message="Bookmark updated!",
            ),
            "D": Option(
                "Delete a bookmark",
                commands.DeleteBookmarkCommand(),
                prep_call=get_bookmark_id_for_deletion,
                success_message="Bookmark deleted!",
            ),
            "G": Option(
                "Import GitHub stars",
                commands.ImportGitHubStarsCommand(),
                prep_call=get_github_import_options,
                success_message="Imported {result} bookmarks from starred repos!",
            ),
            "Q": Option("Quit", commands.QuitCommand()),
        }
    )

    print_options(options)

    chosen_option = get_option_choice(options)  # Create an instance of Option
    clear_screen()
    chosen_option.choose()

    _ = input("Press ENTER to return to menu ")


if __name__ == "__main__":
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()


def for_listings_only():
    """ Options listing. """
    options = {
        "A": Option("Add a bookmark", commands.AddBookmarkCommand()),
        "G": Option(
            "Import GitHub stars",
            commands.ImportGitHubStarsCommand(),
            prep_call=get_github_import_options,
        ),
        "B": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option(
            "List bookmarks by title", commands.ListBookmarksCommand(order_by="title")
        ),
        "D": Option("Delete a bookmark", commands.DeleteBookmarkCommand()),
        "Q": Option("Quit", commands.QuitCommand()),
    }
    print_options(options)
