from forex_python.converter import CurrencyRates
from datetime import datetime
import json
import os

HISTORY_PATH = os.path.join(os.path.dirname(__file__), 'history.json')
DATE_FORMAT = '%d.%m.%Y'


def get_history():
    c = CurrencyRates()
    if os.path.exists(HISTORY_PATH):
        transactions = json.load(open(HISTORY_PATH))
        for transaction in transactions:
            source_curr = transaction['source']
            dest_curr = transaction['dest']
            value_curr = transaction['value']
            date = datetime.strptime(transaction['date'], DATE_FORMAT)
            rate = c.get_rate(source_curr, dest_curr, date)
            get = c.convert(source_curr, dest_curr, float(value_curr), date)
            print('Конвертировал {} {} в {} по курсу {} и получил {} {}'.format(
                value_curr, source_curr, rate, dest_curr, get, dest_curr))
    else:
        print("File {} doesn't exits".format(HISTORY_PATH))


def main():
    c = CurrencyRates()
    while True:
        print('Source currency = ', end='')
        source_curr = input()
        print('Destination currency = ', end='')
        dest_curr = input()
        print('Value = ', end='')
        value_curr = input()
        print('Date (optional) = ', end='')
        date = input()

        if not date:
            date = datetime.today().strftime(DATE_FORMAT)

        if os.path.exists(HISTORY_PATH):
            transactions = json.load(open(HISTORY_PATH))
        else:
            transactions = []

        transactions.append(
            {'source': source_curr, 'dest': dest_curr, 'value': value_curr, 'date': date})

        with open(os.path.join(HISTORY_PATH), "w+") as f:
            json.dump(transactions, f, indent=4)

        date = datetime.strptime(date, DATE_FORMAT)

        try:
            print(c.convert(source_curr, dest_curr, float(value_curr), date))
        except:
            print('Wrong input. Try again:')


if __name__ == "__main__":
    main()
