import tkinter as tk
from tkinter import ttk, messagebox
from requests import get

BASE_URL = "https://free.currconv.com/"
API_KEY = "98423b19ea011970c913"


def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']
    data = list(data.items())
    data.sort()
    return data


def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()
    if len(data) == 0:
        messagebox.showerror("Error", "Invalid currencies.")
        return None
    rate = list(data.values())[0]
    return rate


def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return None
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount.")
        return None
    return rate * amount


def list_currencies():
    currencies = get_currencies()
    currency_list = "\n".join([f"{currency['id']} - {currency['currencyName']} - {currency.get('currencySymbol', '')}"
                               for _, currency in currencies])
    messagebox.showinfo("Currencies", currency_list)


def on_convert():
    currency1 = entry_currency1.get().upper()
    currency2 = entry_currency2.get().upper()
    amount = entry_amount.get()
    result = convert(currency1, currency2, amount)
    if result is not None:
        label_result.config(text=f"{amount} {currency1} is equal to {result:.2f} {currency2}")


def on_rate():
    currency1 = entry_currency1.get().upper()
    currency2 = entry_currency2.get().upper()
    rate = exchange_rate(currency1, currency2)
    if rate is not None:
        messagebox.showinfo("Exchange Rate", f"The exchange rate from {currency1} to {currency2} is {rate}")


# GUI setup
root = tk.Tk()
root.title("Currency Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Currency Converter", font=("Arial", 18)).grid(row=0, column=0, columnspan=2)

ttk.Label(frame, text="Base Currency:").grid(row=1, column=0, sticky=tk.W)
entry_currency1 = ttk.Entry(frame)
entry_currency1.grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Amount:").grid(row=2, column=0, sticky=tk.W)
entry_amount = ttk.Entry(frame)
entry_amount.grid(row=2, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Convert To:").grid(row=3, column=0, sticky=tk.W)
entry_currency2 = ttk.Entry(frame)
entry_currency2.grid(row=3, column=1, sticky=(tk.W, tk.E))

button_convert = ttk.Button(frame, text="Convert", command=on_convert)
button_convert.grid(row=4, column=0, sticky=tk.W)

button_rate = ttk.Button(frame, text="Rate", command=on_rate)
button_rate.grid(row=4, column=1, sticky=tk.E)

button_list = ttk.Button(frame, text="List Currencies", command=list_currencies)
button_list.grid(row=5, column=0, columnspan=2)

label_result = ttk.Label(frame, text="")
label_result.grid(row=6, column=0, columnspan=2)

# Padding configuration
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()