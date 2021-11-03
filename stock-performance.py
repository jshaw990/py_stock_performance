import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib import style
import tkinter as tk
from tkinter import *
from tiingo import TiingoClient

all_tickers = []
dates_str = ''
tickers_str = ''
one_year = datetime.datetime.now() - relativedelta(years=1)
six_months = datetime.datetime.now() - relativedelta(months=6)
one_month = datetime.datetime.now() - relativedelta(months=1)
one_week = datetime.datetime.now() - relativedelta(weeks=1)
ticket_start = any


def stock_graph(ticker_input):
    style.use('fivethirtyeight')

    config = {}
    config['session'] = True
    # PLACE YOUR TIINGO API KEY WITHIN THE STRING BELOW
    config['api_key'] = ''
    client = TiingoClient(config)

    end = datetime.datetime.now()

    if str(var.get()) == 'One Week':
        ticker_start_date = one_week
        dates_str = 'One Week'
    elif str(var.get()) == 'One Month':
        ticker_start_date = one_month
        dates_str = 'One Month'
    elif str(var.get()) == 'Six Months':
        ticker_start_date = six_months
        dates_str = "Six Months"
    elif str(var.get()) == 'One Year':
        ticker_start_date = one_year
        dates_str = 'One Year'

    ticker = str(ticker_input)

    ticker = ticker.upper()

    all_tickers.append(ticker)

    stock_data = client.get_dataframe(
        ticker, frequency='daily', startDate=ticker_start_date, endDate=end)

    tickers_str = ', '.join(all_tickers)

    stock_data['high'].plot(label=ticker)
    plt.title(tickers_str+' Stock Performace Over '+dates_str)
    plt.legend()

    plt.draw()
    plt.show(block=False)


def button_bundle(text):
    ticker_input_data = text.get()
    stock_graph(ticker_input_data)


def radio_selection():
    selection = 'You have selected ' + str(var.get())
    date_label.config(text=selection)


root = tk.Tk()
root.title('Stock Performance')
date_label = Label(root)
# date_label.config(text = 'You selected One Month')
var = tk.StringVar(None, 'One Month')


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        root.geometry('400x200')

        ticker_label = tk.Label(root, text='Stock Ticker:')
        text = tk.StringVar()
        ticker_input = tk.Entry(root, textvariable=text)
        ticker_input.focus()

        radio0 = Radiobutton(root, text='One Week', variable=var,
                             value='One Week', command=radio_selection)
        radio0.pack()

        radio1 = Radiobutton(root, text='One Month', variable=var,
                             value='One Month', command=radio_selection)
        radio1.pack()

        radio2 = Radiobutton(root, text='Six Months', variable=var,
                             value='Six Months', command=radio_selection)
        radio2.pack()

        radio3 = Radiobutton(root, text='One Year', variable=var,
                             value='One Year', command=radio_selection)
        radio3.pack()

        ticker_label.pack()
        ticker_input.pack()

        plot_button = Button(master=root, command=lambda: button_bundle(
            text), height=2, width=10, text='Go')
        plot_button.pack()

        root.bind('<Return>', lambda x: button_bundle(text))

        date_label.pack()


app = Application(master=root)
app.mainloop()