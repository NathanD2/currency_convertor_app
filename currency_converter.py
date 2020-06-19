"""
A basic temperature conversion application.

During development, I exercised my experience with python. I also experimented with the use of classes and python's
built-in module Tkinter to build my first GUI.

Currency data taken from API from https://api.exchangeratesapi.io/latest.

Nathan Dong, Student
https://github.com/NathanD2/currency_convertor_app
"""
import tkinter as tk
import requests
import json


class App:
    """ A class for a currency converter app."""
    def __init__(self, currency_data: dict):
        """ Instantiates an currency conversion app object.

        :precondition: currency_data as a dictionary with a key of "rates".
        :param currency_data: a dictionary
        """
        # Creates a list of all countries with available currency rate data.
        countries = []
        for country in currency_data['rates'].keys():
            countries.append(country)
        countries.sort()    # Countries appear in alphabetical order.

        # Print list of countries.
        print(countries)

        # Store country currency rate data
        self.currency_data = currency_data

        # App root/master.
        self.root = tk.Tk()
        # App canvas.
        self.canvas = tk.Canvas(self.root, height=500, width=800, bg="#464D5A")

        # Attaches to root/master
        self.canvas.pack()

        # Title Frame
        self.frame_title = tk.Frame(self.root)
        self.frame_title.place(relwidth=0.96, relheight=0.16, relx=0.02, rely=0.02)
        self.title = tk.Label(self.frame_title, text="Currency Converter!", font=("Helvetica", 20))
        self.title.pack()

        # Frame main
        self.frame_main = tk.Frame(self.root)
        self.frame_main.place(relwidth=0.96, relheight=0.78, relx=0.02, rely=0.2)

        # Drop-down Option Menu for Country options.
        self.variable_1 = tk.StringVar(self.frame_main)     # Monitors selected variables from Option Menu.
        self.variable_1.set("Select Country")  # default value
        self.t1 = tk.OptionMenu(self.frame_main, self.variable_1, *countries)

        self.variable_2 = tk.StringVar(self.frame_main)
        self.variable_2.set("Select Country")  # default value
        self.t2 = tk.OptionMenu(self.frame_main, self.variable_2, *countries)
        # Appends both Option Menus to application via grid method.
        self.t1.grid(row=0, column=0, padx=50, pady=50)
        self.t2.grid(row=0, column=2, padx=50, pady=50)

        # Input boxes (2)
        self.e1 = tk.Entry(self.frame_main)
        self.e2 = tk.Entry(self.frame_main)
        self.e2.config(state="disabled")    # Result currency textbox/entry can't be changed by user.
        self.e1.grid(row=1, column=0)
        self.e2.grid(row=1, column=2)

        # Conversion button
        self.convert_btn = tk.Button(self.frame_main, text="Convert", font=("Helvetica", 15), height=1, width=10,
                                     command=self.convert)
        self.convert_btn.grid(row=1, column=1, padx=50)

        # Status messages
        self.status_1 = tk.Label(self.frame_main, text="", font=("Helvetica", 15))
        self.status_2 = tk.Label(self.frame_main, text="", font=("Helvetica", 15))
        self.status_1.grid(row=2, column=0, padx=50)
        self.status_2.grid(row=2, column=2, padx=50)

    def start(self):
        """  Starts application.

        :return:
        """
        print("Application is running")

        # Opens GUI
        self.root.mainloop()

        print("Application has closed.")

    def get_entry_1(self) -> str:
        """ Retrieves input for entry 1 (left).

        :return: input for entry 1 as a string.
        """
        return self.e1.get()

    def get_entry_2(self) -> str:
        """ Retrieves input for entry 2 (right).

        :return: input for entry 2 as a string.
        """
        return self.e2.get()

    def convert(self):
        """ Calculates equivalent currency value to another currency.

        :return: None
        """
        # Bool to determine if both country selections are valid.
        countries_valid = True

        print("Entry 1 : " + self.get_entry_1())

        # Changes status message text
        try:
            amount_1 = float(self.get_entry_1())
            self.status_1['text'] = ""
        except ValueError:
            print("Amount 1 is NAN")
            self.status_1['text'] = "- Not a valid number"
            return

        # Retrieve user selected countries from OptionMenu.
        print("Attempt to retrieve country selection")
        print(self.variable_1.get())
        print(self.variable_2.get())

        # Checks for valid choices from Option Menus.
        if self.variable_1.get() == "Select Country":
            self.status_1['text'] += "\n- Select a country"
            countries_valid = False
        if self.variable_2.get() == "Select Country":
            self.status_2['text'] += "\n- Select a country"
            countries_valid = False

        # Ensures both countries are valid selections.
        if countries_valid is False:
            return

        # Continue if all fields are valid to convert currency
        currency_rate_1 = self.currency_data['rates'][self.variable_1.get()]
        currency_rate_2 = self.currency_data['rates'][self.variable_2.get()]
        print(currency_rate_1)
        print(currency_rate_2)

        # Calculates equivalent currency amount from entry 1 to entry 2.
        result_sum = round(((float(self.get_entry_1()) / currency_rate_1) * currency_rate_2), 5)

        # Changes entry 2 text.
        self.e2.config(state="normal")
        self.e2.delete(0, "end")
        value_entry_2 = str(round(result_sum, 2))
        self.e2.insert(0, value_entry_2)
        self.e2.config(state="disabled")

        # Normalize entry 1 text.
        value_entry_1 = round(float(self.get_entry_1()), 2)
        self.e1.delete(0, "end")
        self.e1.insert(0, str(value_entry_1))


def fetch_api_data(url: str) -> dict:
    """ Fetch data from api call.

    :precondition: url as a valid api url for currency rates.
    :param url: a string
    :return: currency rate data as a dictionary.
    """
    res = requests.get(url)
    res.raise_for_status()

    data = json.loads(res.text)

    return data


def show_data(e1, e2):
    """ Prints app entry data.

    :param e1: a string
    :param e2: a string
    :return:
    """
    print("e1 data : " + e1)
    print("e2 data : " + e2)


def main():
    """ Main program function."""
    # Fetch currency rate data.
    currency_data = fetch_api_data("https://api.exchangeratesapi.io/latest")

    # Create temperature app object.
    app = App(currency_data)
    # Start app.
    app.start()


if __name__ == "__main__":
    """ Executes main function if module is executed."""
    main()
