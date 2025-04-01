import csv
from pathlib import Path
from pprint import pprint
from datetime import datetime, timedelta
import copy

def reconcile_accounts(transactions1: list, transactions2: list) -> list:
    dict_transactions1 = {}
    dict_transactions2 = {}

    # Inserting transaction in a dictionary with hash to avoid colision
    for transaction in transactions1:
        dict_transactions1[str(transaction)] = transaction
    for transaction in transactions2:
        dict_transactions2[str(transaction)] = transaction

    # Iterating over transactions
    for key, transaction in dict_transactions1.items():
        transaction_copy_minus_one_day = copy.deepcopy(transaction)
        transaction_copy_plus_one_day = copy.deepcopy(transaction)

        #Creating data variation
        data_minus_one_day = _parse_date(transaction[0]) - timedelta(days=1)
        data_plus_one_day = _parse_date(transaction[0]) + timedelta(days=1)

        transaction_copy_minus_one_day[0] = str(data_minus_one_day.strftime("%Y-%m-%d"))
        transaction_copy_plus_one_day[0] = str(data_plus_one_day.strftime("%Y-%m-%d"))

        search_key_minus_one_day = str(transaction_copy_minus_one_day)
        search_key_plus_one_day = str(transaction_copy_plus_one_day)

        #Covering cases with data minus one day matching
        if search_key_minus_one_day in dict_transactions2:
            if len(dict_transactions2[search_key_minus_one_day]) == 4:
                dict_transactions1[key].append('FOUND')
                dict_transactions2[search_key_minus_one_day].append('FOUND')
        #Covering exact match case
        if key in dict_transactions2:
            if len(dict_transactions2[key]) == 4 and len(dict_transactions1[key]) == 4:
                dict_transactions1[key].append('FOUND')
                dict_transactions2[key].append('FOUND')
        #Covering cases with data plus one day matching
        if search_key_plus_one_day in dict_transactions2:
            if len(dict_transactions2[search_key_plus_one_day]) == 4 and len(dict_transactions1[key]) == 4:
                dict_transactions1[key].append('FOUND')
                dict_transactions2[search_key_plus_one_day].append('FOUND')

        if len(dict_transactions1[key]) == 4:
            dict_transactions1[key].append('MISSING')

    for key, transaction in dict_transactions2.items():
        if len(transaction) == 4:
            dict_transactions2[key].append('MISSING')
    
    new_transactions1 = list(dict_transactions1.values())
    new_transactions2 = list(dict_transactions2.values())

    return new_transactions1, new_transactions2

def _parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")

if __name__ == "__main__":
    transactions1 = list(csv.reader(Path('transactions1.csv').open()))
    transactions2 = list(csv.reader(Path('transactions2.csv').open()))
    out1, out2 = reconcile_accounts(transactions1, transactions2)
    pprint(out1)
    pprint(out2)