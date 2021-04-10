# View.py
import tkinter as tk
from tkinter import ttk  # Mdern look


class View(tk.Tk):
    """ View with inheritance. """

    PAD = 10
    MAX_BUTTONS_PER_ROW = 4

    button_captions = [
        "C",
        "+/-",
        "%",
        "/",
        7,
        8,
        9,
        "*",
        4,
        5,
        6,
        "-",
        1,
        2,
        3,
        "+",
        0,
        ".",
        "=",
    ]

    def __init__(self, controller):
        """ Constructor. """
        super().__init__()
        self.title("PyCalc1.0")

        self.controller = controller

        self.value_var = tk.StringVar()

        self.config(bg="black")  # Set background of outside window to black

        self._configure_button_styles()

        self._make_main_frame()
        self._make_label()
        self._make_buttons()
        self._center_window()

    def _configure_button_styles(self):
        style = ttk.Style()
        # print(style.theme_names()) # Used to get list of themes used on this computer
        # print(style.theme_use()) # Used to see which one is used

        style.theme_use("alt")

        # Style for numbers
        style.configure("N.TButton", foreground="white", background="gray")

        # Style for operators
        style.configure("O.TButton", foreground="white", background="orange")

        # Style for miscelleneous
        style.configure("M.TButton", background="white")

    def main(self):
        """ Main view function. """
        # print("In view main. ")
        self.mainloop()

    def _make_main_frame(self):
        """ Create the borders. """
        self.main_frm = ttk.Frame(self)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD)

    def _make_label(self):
        """ Create an label zone. """
        lbl = tk.Label(
            self.main_frm,  # Put the entry in the main_frm which is a class var
            anchor="e",  # To look like a calculator
            textvariable=self.value_var,
            bg="black",
            fg="white",
            font=("Ariel", 30),
        )
        lbl.pack(fill="x")

    def _make_entry(self):
        """ Create an entry zone. """
        ent = ttk.Entry(
            self.main_frm,  # Put the entry in the main_frm which is a class var
            justify="right",  # To look like a calculator
            textvariable=self.value_var,
            state="disable",  # To allow only adding numbers from buttons
        )
        ent.pack(fill="x")

    def _make_buttons(self):
        """ Create the calcultor buttons. """
        outer_frm = ttk.Frame(self.main_frm)
        outer_frm.pack()

        is_first_row = True
        buttons_in_row = 0

        for caption in self.button_captions:
            if is_first_row or buttons_in_row == self.MAX_BUTTONS_PER_ROW:
                frm = ttk.Frame(outer_frm)
                frm.pack(fill="x")
                is_first_row = False
                buttons_in_row = 0

            if isinstance(caption, int):
                style_prefix = "N"
            elif self._is_operator(caption):
                style_prefix = "O"
            else:
                style_prefix = "M"

            style_name = f"{style_prefix}.TButton"

            btn = ttk.Button(
                frm,  # Put in the frame frm
                text=caption,  # Include the following caption
                command=(
                    lambda button=caption: self.controller.on_button_click(button)
                ),  # Calls a common in the controller, lambda is used to pass a parameter caption
                style=style_name,
            )

            if caption == 0:  # Make zero button wider
                fill = "x"
                expand = 1
            else:
                fill = "none"
                expand = 0

            btn.pack(fill=fill, expand=expand, side="left")
            buttons_in_row += 1

    def _is_operator(self, button_caption: str) -> bool:
        """ Helper function to see if the button is an operator. """
        return button_caption in ["/", "*", "+", "-"]

    def _center_window(self) -> None:
        """ Position the window in the center. """
        self.update()  # Not sure why required?
        width = self.winfo_width()
        height = self.winfo_height()

        # Integer division b/c geometry method requires integer
        x_offset = (self.winfo_screenwidth() - width) // 2
        y_offset = (self.winfo_screenheight() - height) // 2

        # print(width, height, x_offset, y_offset)

        self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

