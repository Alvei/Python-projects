# pattern_command.py
from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    """ The Command interface declares a method for executing a command. """

    @abstractmethod
    def execute(self) -> None:
        """ Abstract excute method. """


class SimpleCommand(Command):
    """ Some commands can implement simple operations on their own. """

    def __init__(self, payload: str) -> None:
        self._payload = payload

    def execute(self) -> None:
        """ Overide the execute method. """
        print(
            f"SimpleCommand: See, I can do simple things like printing"
            f"({self._payload})"
        )


class ComplexCommand(Command):
    """ However, some commands can delegate more complex operations to other
        objects, called "receivers."
    """

    def __init__(self, my_receiver: Receiver, var_a: str, var_b: str) -> None:
        """ Complex commands can accept one or several receiver objects along with
            any context data via the constructor. """

        self._receiver = my_receiver
        self._var_a = var_a
        self._var_b = var_b

    def execute(self) -> None:
        """ Commands can delegate to any methods of a receiver. """

        print(
            "ComplexCommand: Complex stuff should be done by a receiver object", end=""
        )
        self._receiver.do_something(self._var_a)
        self._receiver.do_something_else(self._var_b)


class Receiver:
    """ The Receiver classes contain some important business logic. They know how to
    perform all kinds of operations, associated with carrying out a request. In
    fact, any class may serve as a Receiver. """

    @classmethod
    def do_something(cls, var_a: str) -> None:
        """ First biz logic. """
        print(f"\nReceiver: Working on ({var_a}.)", end="")

    @classmethod
    def do_something_else(cls, var_b: str) -> None:
        """ Second biz logic"""
        print(f"\nReceiver: Also working on ({var_b}.)", end="")


class Invoker:
    """ The Invoker is associated with one or several commands. It sends a request
        to the command. """

    _on_start = None
    _on_finish = None

    """ Initialize commands. """

    def set_on_start(self, command: Command) -> None:
        """ Command to execute at beginning. """
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        """ Command to execute when finishing. """
        self._on_finish = command

    def do_something_important(self) -> None:
        """ The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a command.
        """

        print("\nInvoker: Does anybody want something done before I begin?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("\nInvoker: ...doing something really important...")

        print("\nInvoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


if __name__ == "__main__":

    invoker = Invoker()
    receiver = Receiver()

    # Simple command does not use the receiver
    invoker.set_on_start(SimpleCommand("Say Hi!"))

    invoker.set_on_finish(ComplexCommand(receiver, "Send email", "Save report"))

    invoker.do_something_important()
