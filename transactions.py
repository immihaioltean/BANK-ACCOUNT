from datetime import date
from typing import TypedDict

from domain import (
    get_date,
    get_sum,
    get_type,
    set_date,
    set_sum,
    set_type
)

def valid_date(date_trans:list):
    """
    Check if the date is valid for the transaction (considering it took place after 1900)
    :param date_trans(list) - [day,month,year]
    :return: True if the date is valid, False otherwise
    """
    if date_trans[2] < 1900 or date_trans[2] > date.today().year:
        return False
    elif date_trans[1] < 1 or date_trans[1] > 12:
        return False
    else:
        if date_trans[1] < 8 and date_trans[1] % 2 and (date_trans[0] > 31 or date_trans[0] < 1):
            return False
        elif date_trans[1] == 2:
            if date_trans[2] % 4 == 0 and date_trans[2] % 100 or date_trans[2] % 400 == 0:
                if date_trans[0] < 0 or date_trans[0] > 29:
                    return False
            elif date_trans[0] < 0 or date_trans[0] > 28:
                return False
        elif ((3 < date_trans[1] < 7 or 8 < date_trans[1] < 12) and date_trans[1] % 2 == 0
              and (date_trans[0] < 0 or date_trans[0] > 30)):
            return False
    return True

def create_date_list(data:str):
    """
    :param data: string
    :return: a list with the given date [day,month,year]
    """
    data = data.strip().replace(".", " ").replace("/", " ").replace(",", " ").split()
    return [int(i) for i in data]

def create_new_transaction():
    """
    Add a new transaction to the list
    date (list) - [day,month,year]
    sum (float)
    type (str) - "deposit" or "withdrawal"
    :return: return None if the transaction is invalid or
             a dictionary with the transaction details (date,sum,type)
    """
    date_trans = input("Enter the date of the transaction (day/month/year): ")
    date_trans = create_date_list(date_trans)

    if valid_date(date_trans)==False:
        print("Invalid input. You have to enter a valid date!")
        return None

    print("The transaction took place on: ",end="")
    for i in date_trans:
        print(i,end=" ")
    print()

    sum_trans=float(input("Enter the sum of the transaction: "))
    if sum_trans<=0:
        print("Invalid input. You have to enter a valid sum!")
        return None
    else:
        print(f"The sum of the transaction is: {sum_trans}")

    type_trans=input("Enter the type of the transaction (deposit/withdrawal): ")
    if type_trans!="deposit" and type_trans!="withdrawal":
        print("Invalid input. Yoy have to enter a valid type!")
        return None
    else:
        print(f"Transaction added successfully!")

    return {"date":date_trans,"sum":sum_trans,"type":type_trans}

def add_transaction(transaction_list:list,transaction:dict):
    """
    :param transaction_list: list of transactions
    :param transaction: dict with the transaction details (date,sum,type)
    :return: transaction_list with the new transaction added
    """
    return transaction_list.append(transaction)

def transactions_sorted_by_date(transaction_list:list):
    """
    :param transaction_list (list)
    :return: the list of transactions sorted by date
    """
    transaction_list.sort(key=lambda transaction: transaction["date"][::-1])
    return transaction_list

def print_transactions(transaction_list:list):
    """
    :param transaction_list (list)
    :return: print the transactions sorted by date
    """
    index=1
    for transaction in transaction_list:
        print(f"{index}. Transaction took place on: ",end="")
        for data in transaction["date"]:
            print(data,end=" ")
        print(f"and it was a {transaction["type"]} of {transaction["sum"]}")
        index+=1

def read_update_transaction(transaction_list:list):
    update = input("Enter the date of the transaction you would like to update (day/month/year): ")
    update = create_date_list(update)
    index = -1
    length = len(transaction_list)
    pos = 0
    for transaction in range(length):
        if transaction_list[transaction]["date"] == update:
            index += 1
            pos = transaction
    if index < 0:
        print("No transaction found!")
        return None
    choice = 0
    if index > 0:
        print("Which transaction would you like to update?")
        for transaction in range(pos - index, pos + 1):
            print(f"{transaction}. Transaction took place on: ", end="")
            for data in transaction_list[transaction]["date"]:
                print(data, end=" ")
            print(f"and it was a {transaction_list[transaction]["type"]}"
                  f" of {transaction_list[transaction]["sum"]}")
        choice = int(input("Enter your choice: "))
        if not pos - index <= choice <= pos:
            print("Invalid choice!")
            return None
    if index > 0: index = choice
    print("What you would like to update? Enter sum for sum, type for type or both")
    choice = input("Enter your choice: ")
    new={}
    match choice:
        case "sum":
            new["sum"]=float(input("Enter the new sum: "))
        case "type":
            new["type"]=input("Enter the new type: ")
        case "both":
            new["sum"] = float(input("Enter the new sum: "))
            new["type"] = input("Enter the new type: ")
        case _:
            print("Invalid choice!")
            return None
    new["index"]=index
    new["choice"]=choice
    return new

class Update(TypedDict):
    index: int
    choice: str
    sum: float
    type: str

def update_transaction(transaction_list:list,new:Update):
    """
    Update an existent transaction
    :param transaction_list: list of transactions
    :param new: dict with choice,type,sum,index(if there is more than
                one transaction at a specific date, the user can choose
                which one to update)
    :return: the list of transactions updated
    """
    match new["choice"]:
        case "sum":
            transaction_list[new["index"]]["sum"] = new["sum"]
        case "type":
            transaction_list[new["index"]]["type"] = new["type"]
        case "both":
            transaction_list[new["index"]]["sum"] = new["sum"]
            transaction_list[new["index"]]["type"] = new["type"]
    return transaction_list

def copy_transactions(transaction_list:list):
    """
    Creates an independent copy of the transactions
    :param transaction_list: list of transactions
    :return: the independent copy of the transactions list
    """
    old_transactions = []
    for transactions in transaction_list:
        old_transactions.append({
            "date": list(transactions["date"]),
            "sum": transactions["sum"],
            "type": transactions["type"]
        })
    return old_transactions
