# Model.py


class Model:
    def __init__(self):
        """ Constructor. """
        self.value = ""

    def calculate(self, caption):
        """ Does the calculation. """
        if caption == "C":
            self.value = ""
        if caption == "+/-":
            self.value = self.value[1:] if self.value[0] == "-" else "-" + self.value

        elif isinstance(caption, int):
            self.value += str(caption)  # Remains left justify

        return self.value
