""" light_switch.py
    https://en.wikipedia.org/wiki/Command_pattern
    https://sbcode.net/python/command/
    Command pattern is a design pattern in which an object is used to represent and
    encapsulate all the information needed to call a method at a later time.

    This information includes the method name, the object that owns the method and
    values for the method parameters.

    Using the command design pattern describes the following solution:
        - Define separate (command) objects that encapsulate a request.
        - Class delegates a request to a command object instead of implementing a particular
          request directly.
    Enables configuration of a class with a command object that is used to perform a request.
    Class is no longer coupled to a particular request and has no knowledge of how the
    request is carried out.

    INVOKER object should be kept away from specifics of what exactly happens when
    its methods are executed. This way, the same INVOKER object can be used to send
    commands to objects with similar interfaces.

    A COMMAND object knows about RECEIVER and invokes a method of the RECEIVER.
    Values for parameters of the RECEIVER method are stored in the COMMAND.
"""


class Switch:
    """ The INVOKER class does not implement the request but refers to the COMMAND interface.
        It receives messages from CLIENT and sends messages to RECEIVER.
        INVOKER does not know the specifics of the command and uses the .execute() method. """

    def __init__(self, flip_up_cmd, flip_down_cmd) -> None:
        """ Constructor. """
        self.__flip_up_command = flip_up_cmd  # Instantiate these COMMAND classes
        self.__flip_down_command = flip_down_cmd

    def flip_up(self) -> None:
        """ Calls the flip_up COMMAND. """
        self.__flip_up_command.execute()

    def flip_down(self) -> None:
        """ Calls the flip_down COMMAND. """
        self.__flip_down_command.execute()


class Light:
    """ The RECEIVER Class contains the instructions to execute when a corresponding
        COMMAND is given. Here it prints its state but it could control the light. """

    @classmethod
    def turn_on(cls) -> None:
        """ Turn the light on. """
        print("\tLight is ON")

    @classmethod
    def turn_off(cls) -> None:
        """ Turn the light off. """
        print("\tLight is OFF")


class Command:
    """ The COMMAND Abstract Class. """

    def __init__(self):
        """ Constructor. """

    def execute(self):
        """ Executes the command for the class. Will be overiden. """


class FlipUpCommand(Command):
    """ The COMMAND class for turning on the Light object.
        It uses an .excute() method that calls the RECEIVER object method.
        It is therefore knowledgeable about the RECEIVER method names. """

    def __init__(self, light: Light) -> None:
        """ Constructor. """
        Command.__init__(self)
        self.__light = light

    def execute(self) -> None:
        """ Executes the command for the class. """
        self.__light.turn_on()


class FlipDownCommand(Command):
    """ The COMMAND class for turning off the Light object.
        It uses an .excute() method that calls the RECEIVER object method. """

    def __init__(self, light: Light) -> None:
        """ Constructor. """
        Command.__init__(self)
        self.__light = light

    def execute(self) -> None:
        """ Executes the command for the class. """
        self.__light.turn_off()


class LightSwitch:
    """ The CLIENT Class.
        Its .switch() method is the INVOKER and takes a str parameter
        and knows about the commands. """

    def __init__(self) -> None:
        """ Constructor. """
        self.__lamp = Light()  # RECEIVER
        self.__switch_up = FlipUpCommand(self.__lamp)  # COMMAND
        self.__switch_down = FlipDownCommand(self.__lamp)  # COMMAND
        self.__switch = Switch(self.__switch_up, self.__switch_down)  # INVOKER

    def switch(self, cmd: str) -> None:
        """ Method that invokes the different commands. It knows about the parameters. """
        cmd = cmd.strip().upper()

        if cmd == "ON":
            self.__switch.flip_up()
        elif cmd == "OFF":
            self.__switch.flip_down()
        else:
            print('\tArgument "ON" or "OFF" is required.')


if __name__ == "__main__":
    my_light = LightSwitch()

    print("\n** Switch ON test.")
    my_light.switch("ON")

    print("\n** Switch OFF test")
    my_light.switch("OFF")

    print("\n** Invalid Command test")
    my_light.switch("****")
