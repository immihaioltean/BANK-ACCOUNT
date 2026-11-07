from typing import TypedDict

from domain import (
    get_date,
    get_sum,
    get_type,
    create_transaction,
    set_date,
    set_sum,
    set_type
)

from validation import (
    valid_date,
    validate_sum
)


def create_date_list(data:str):
    """
    :param data: string
    :return: a list with the given date [day,month,year]
    """
    data = data.strip().replace(".", " ").replace("/", " ").replace(",", " ").split()
    return [int(i) for i in data]

def add_transaction(transactions:list,transaction:dict):
    """
    :param transactions: list of transactions
    :param transaction: dict with the transaction details (date,sum,type)
    :return: transaction_list with the new transaction added
    """
    transactions.append(transaction)

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

def get_transaction_bigger_than_a_threshold(transaction_list:list,summ:float):
    """
    :param transaction_list (list)
    :param summ (float)
    :return: a list with all the transactions bigger than the input sum
    """
    return [transaction for transaction in transaction_list if transaction["sum"]>summ]

def trans_before_a_given_date(transaction_list:list,given_date:list,summ:float|int):
    """
    :param transaction_list - list of transactions
    :param given_date - list of numbers with the given date (day/month/year)
    :param summ (float|int) - the threshold given by the user
    :return: a list of transactions which are made before a
             given date with bigger sums than a given sum
    """
    result=[]
    input_date=given_date[::-1]
    for transaction in transaction_list:
        current_transaction=transaction["date"][::-1]
        if transaction["sum"]>summ and current_transaction<input_date:
            result.append(transaction)
    return result

def get_transaction_by_type(trans_list:list,type_trans:str):
    """
    :param trans_list (list) - list of transactions
    :param type_trans (str) - type of transaction
    :return: a list of transactions with a given type
    """
    return [transaction for transaction in trans_list if transaction["type"]==type_trans]

def transactions_sum_given_type(transaction_list:list,type:str):
    """
    :param transaction_list (list)
    :param type (string)
    :return: sum of all transactions of a given type as a float
    """
    summ=0.0
    for transaction in transaction_list:
        if transaction["type"]==type:
            summ+=transaction["sum"]
    return summ

def transactions_type_ascending_order_by_sum(transaction_list:list,given_type:str):
    """
    :param transaction_list: list of transactions
    :param given_type: string
    :return: list of transactions of a given type in ascending order by sum
    """
    new_list=[transaction for transaction in transaction_list if transaction["type"]==given_type]
    new_list.sort(key=lambda transaction: transaction["sum"])
    return new_list

def account_balance_at_given_date(transaction_list:list,given_date:list):
    """
    :param transaction_list: list of transactions
    :param given_date: list [day,month,year]
    :return: account balance at a given date
    """
    summ=0.0
    for transaction in transaction_list:
        if transaction["date"][::-1]<=given_date[::-1]:
            if transaction["type"]=="deposit":
                summ+=transaction["sum"]
            else:
                summ-=transaction["sum"]
    return summ

def delete_transactions_for_specified_date(transaction_list:list,given_date:list):
    new_list=[]
    for transaction in transaction_list:
        if transaction["date"]!=given_date:
            new_list.append(transaction)
    transaction_list[:]=new_list
    return transaction_list

def delete_transactions_for_given_period(transaction_list:list,start_date:list,finish_date:list):
    new_list=[]
    for transaction in transaction_list:
        if not start_date[::-1]<=transaction["date"][::-1]<=finish_date[::-1]:
            new_list.append(transaction)
    transaction_list[:] = new_list
    return transaction_list

def delete_transactions_of_given_type(transaction_list:list,given_type:str):
    new_list=[]
    for transaction in transaction_list:
        if transaction["type"]!=given_type:
            new_list.append(transaction)
    transaction_list[:]=new_list
    return transaction_list

def delete_transactions_with_lower_sums_by_given_type(transaction_list:list,given_sum:float|int,given_type:str):
    new_list=[]
    for transaction in transaction_list:
        if transaction["sum"]>given_sum or transaction["type"]!=given_type:
            new_list.append(transaction)
    transaction_list[:]=new_list
    return transaction_list

def save_state(undo_stack:list,transaction_list:list):
    transactions=[t.copy() for t in transaction_list]
    undo_stack.append(transactions)

def perform_undo(undo_stack:list,transaction_list:list):
    if not undo_stack:
        return None
        #raise ValueError("Nothing to undo")
    transaction_list[:]=undo_stack.pop()
    return transaction_list
