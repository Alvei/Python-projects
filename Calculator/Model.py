# Model.py


class Model:
    def __init__(self):
        """ Constructor. """
        self.previous_value = ""
        self.value = ""
        self.operator = ""

    def calculate(self, caption):
        """ Does the calculation. """
        # print(f"In Caculate method.")
        if caption == "C":  # Clear
            self.value = ""

        elif caption == "+/-":
            self.value = self.value[1:] if self.value[0] == "-" else "-" + self.value

        elif caption == "%":
            # Convert the string to either a float or int
            value = float(self.value) if "." in self.value else int(self.value)
            self.value = str(value / 100)

        elif caption == "=":
            self.value = str(self._evaluate())

        elif caption == ".":
            if not caption in self.value:  # Check that there is not already a decimal
                self.value += caption

        elif isinstance(caption, int):  # Case of all integers
            self.value += str(caption)  # Remains left justify

        else:  # Operators
            if self.value:  # Check to see there is already a value
                self.operator = caption
                self.previous_value = self.value
                self.value = ""  # Clear the display
        return self.value

    def _evaluate(self):
        """ Helper function to evaluate the operation between two instance variable. """
        print(f"evaluate {self.operator}")
        return eval(self.previous_value + self.operator + self.value)
