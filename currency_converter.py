import tkinter as tk
import requests
import json


class App:
    def __init__(self, currency_data):
        # List of countries with currency rate data.
        countries = []
        for country in currency_data['rates'].keys():
            countries.append(country)

        print(countries)
        print(len(countries))

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

        # Country options
        self.variable_1 = tk.StringVar(self.frame_main)
        self.variable_1.set("Select Country")  # default value
        self.t1 = tk.OptionMenu(self.frame_main, self.variable_1, *countries, command=self.select_country_1)

        self.variable_2 = tk.StringVar(self.frame_main)
        self.variable_2.set("Select Country")  # default value
        self.t2 = tk.OptionMenu(self.frame_main, self.variable_2, *countries, command=self.select_country_2)

        self.t1.grid(row=0, column=0, padx=50, pady=50)
        self.t2.grid(row=0, column=2, padx=50, pady=50)

        # Input boxes
        self.e1 = tk.Entry(self.frame_main)
        self.e2 = tk.Entry(self.frame_main)
        self.e1.grid(row=1, column=0)
        self.e2.grid(row=1, column=2)

        # Conversion button
        self.convert_btn = tk.Button(self.frame_main, text="Convert", font=("Helvetica", 15), height=1, width=10,
                                     command=self.convert)
        self.convert_btn.grid(row=1, column=1, padx=50)

        self.country_1 = None
        self.country_2 = None

        # Status messages
        self.status_1 = tk.Label(self.frame_main, text="placeholder", font=("Helvetica", 15))
        self.status_2 = tk.Label(self.frame_main, text="placeholder", font=("Helvetica", 15))
        self.status_1.grid(row=2, column=0, padx=50)
        self.status_2.grid(row=2, column=2, padx=50)

    def start(self):
        print("Application is running")

        print(self.get_entry_1())
        print(self.get_entry_2())
        # Opens GUI
        tk.mainloop()
        print("Application has closed.")

    def get_entry_1(self):
        return self.e1.get()

    def get_entry_2(self):
        return self.e2.get()

    def select_country_1(self, selection):
        self.country_1 = selection
        # print("Country 1: " + self.country_1)
        return

    def select_country_2(self, selection):
        self.country_2 = selection
        # print("Country 2: " + self.country_2)
        return

    def convert(self):
        both_amounts_valid = True
        countries_valid = True

        print("Entry 1 : " + self.get_entry_1())
        print("Entry 2 : " + self.get_entry_2())
        # Changes status message text
        try:
            amount_1 = float(self.get_entry_1())
            self.status_1['text'] = ""
        except ValueError:
            print("Amount 1 is NAN")
            self.status_1['text'] = "- Not a valid number"
            both_amounts_valid = False

        try:
            amount_2 = float(self.get_entry_2())
            self.status_2['text'] = ""
        except ValueError:
            print("Amount 2 is NAN")
            self.status_2['text'] = "- Not a valid number"
            both_amounts_valid = False

        if both_amounts_valid is False:
            print("Amounts not valid")
            # return

        # Retrieve user selected countries from OptionMenu.
        print("Attempt to retrieve country selection")
        print(self.variable_1.get())
        print(self.variable_2.get())

        if self.variable_1.get() == "Select Country":
            self.status_1['text'] += "\n- Select a country"
            countries_valid = False

        if self.variable_2.get() == "Select Country":
            self.status_2['text'] += "\n- Select a country"
            countries_valid = False

        if countries_valid is False:
            return

        # Continue if all fields are valid to convert currency
        currency_rate_1 = self.currency_data['rates'][self.variable_1.get()]
        currency_rate_2 = self.currency_data['rates'][self.variable_2.get()]
        print(currency_rate_1)
        print(currency_rate_2)



def fetch_api_data(url):
    """ Fetch data from api call.

    :param url:
    :return:
    """
    res = requests.get(url)
    res.raise_for_status()

    data = json.loads(res.text)
    # print(data)
    return data


def show_data(e1, e2):
    print("e1 data : " + e1)
    print("e2 data : " + e2)


def main():
    # Fetch currency rate data.
    currency_data = fetch_api_data("https://api.exchangeratesapi.io/latest")
    app = App(currency_data)
    app.start()

    # root = tk.Tk()
    # canvas = tk.Canvas(root, height=500, width=800, bg="#464D5A")
    #
    # # Attaches to root/master
    # canvas.pack()
    #
    # # Title Frame
    # frame_title = tk.Frame(root)
    # frame_title.place(relwidth=0.96, relheight=0.16, relx=0.02, rely=0.02)
    # title = tk.Label(frame_title, text="Currency Converter!", font=("Helvetica", 20))
    # title.pack()
    #
    # # Frame main
    # frame_main = tk.Frame(root)
    # frame_main.place(relwidth=0.96, relheight=0.78, relx=0.02, rely=0.2)
    #
    # # Country options
    # variable_1 = tk.StringVar(frame_main)
    # variable_1.set("Select Country")  # default value
    # t1 = tk.OptionMenu(frame_main, variable_1, *countries)
    #
    # variable_2 = tk.StringVar(frame_main)
    # variable_2.set("Select Country")  # default value
    # t3 = tk.OptionMenu(frame_main, variable_2, *countries)
    #
    # t1.grid(row=0, column=0, padx=50, pady=50)
    # t3.grid(row=0, column=2, padx=50, pady=50)
    #
    # # Input boxes
    # e1 = tk.Entry(frame_main)
    # e2 = tk.Entry(frame_main)
    # e1.grid(row=1, column=0)
    # e2.grid(row=1, column=2)
    #
    # # Conversion button
    # convert_btn = tk.Button(frame_main, text="Get", font=("Helvetica", 15), height=1, width=10,
    #                         command=show_data(e1.get(), e2.get()))
    # convert_btn.grid(row=1, column=1, padx=50, pady=50)
    #
    # # Opens GUI
    # root.mainloop()


if __name__ == "__main__":
    main()
