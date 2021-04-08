# Controller.py
from Model import Model
from view import View


class Controller:
    """ Controller. """

    def __init__(self):
        """ Constructor. """
        self.model = Model()
        self.view = View(self)

    def main(self):
        """ Main control function. """
        self.view.main()

    def on_button_click(self, caption):
        """ Controls the behavior of the button. """
        result = self.model.calculate(caption)
        self.view.value_var.set(result)


if __name__ == "__main__":
    calculator = Controller()
    calculator.main()
