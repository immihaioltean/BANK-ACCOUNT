from domain import (
    get_date,
    get_sum,
    get_type,
    set_date,
    set_sum,
    set_type
)

def create_date_list(data:str):
    """
    :param data: string
    :return: a list with the given date [day,month,year]
    """
    data = data.strip().replace(".", " ").replace("/", " ").split()
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
    transaction_list.sort(key=lambda transaction: get_date(transaction)[::-1])
    return transaction_list

def print_transactions(transaction_list:list):
    """
    :param transaction_list (list)
    :return: print the transactions sorted by date
    """
    index=1
    for transaction in transaction_list:
        print(f"{index}. Transaction took place on: ",end="")
        for data in get_date(transaction):
            print(data,end=" ")
        print(f"and it was a {get_type(transaction)} of {get_sum(transaction)}")
        index+=1

def update_transaction(transaction_list:list,new:dict):
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
            set_sum(transaction_list[new["index"]],new["sum"])
        case "type":
            set_type(transaction_list[new["index"]],new["type"])
        case "both":
            set_sum(transaction_list[new["index"]], new["sum"])
            set_type(transaction_list[new["index"]], new["type"])
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
            "date": list(get_date(transactions)),
            "sum": get_sum(transactions),
            "type": get_type(transactions)
        })
    return old_transactions

def get_transaction_bigger_than_a_threshold(transaction_list:list,summ:float):
    """
    :param transaction_list (list)
    :param summ (float)
    :return: a list with all the transactions bigger than the input sum
    """
    return [transaction for transaction in transaction_list if get_sum(transaction) > summ]

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
        current_transaction = get_date(transaction)[::-1]
        if get_sum(transaction) > summ and current_transaction<input_date:
            result.append(transaction)
    return result

def get_transaction_by_type(trans_list:list,type_trans:str):
    """
    :param trans_list (list) - list of transactions
    :param type_trans (str) - type of transaction
    :return: a list of transactions with a given type
    """
    return [transaction for transaction in trans_list if get_type(transaction) == type_trans]

def transactions_sum_given_type(transaction_list:list,type:str):
    """
    :param transaction_list (list)
    :param type (string)
    :return: sum of all transactions of a given type as a float
    """
    summ=0.0
    for transaction in transaction_list:
        if get_type(transaction) == type:
            summ+=get_sum(transaction)
    return summ

def transactions_type_ascending_order_by_sum(transaction_list:list,given_type:str):
    """
    :param transaction_list: list of transactions
    :param given_type: string
    :return: list of transactions of a given type in ascending order by sum
    """
    new_list=[transaction for transaction in transaction_list if get_type(transaction) == given_type]
    new_list.sort(key=lambda transaction: get_sum(transaction))
    return new_list

def account_balance_at_given_date(transaction_list:list,given_date:list):
    """
    :param transaction_list: list of transactions
    :param given_date: list [day,month,year]
    :return: account balance at a given date
    """
    summ=0.0
    for transaction in transaction_list:
        if get_date(transaction)[::-1] <= given_date[::-1]:
            if get_type(transaction) == "deposit":
                summ+=get_sum(transaction)
            else:
                summ-=get_sum(transaction)
    return summ

def delete_transactions_for_specified_date(transaction_list:list,given_date:list):
    new_list=[]
    for transaction in transaction_list:
        if get_date(transaction) != given_date:
            new_list.append(transaction)
    transaction_list[:]=new_list
    return transaction_list

def delete_transactions_for_given_period(transaction_list:list,start_date:list,finish_date:list):
    new_list=[]
    for transaction in transaction_list:
        if not start_date[::-1] <= get_date(transaction)[::-1] <= finish_date[::-1]:
            new_list.append(transaction)
    transaction_list[:] = new_list
    return transaction_list

def delete_transactions_of_given_type(transaction_list:list,given_type:str):
    new_list=[]
    for transaction in transaction_list:
        if get_type(transaction) != given_type:
            new_list.append(transaction)
    transaction_list[:]=new_list
    return transaction_list

def delete_transactions_with_lower_sums_by_given_type(transaction_list:list,given_sum:float|int,given_type:str):
    new_list=[]
    for transaction in transaction_list:
        if get_sum(transaction) > given_sum or get_type(transaction) != given_type:
            new_list.append(transaction)
    transaction_list[:] = new_list
    return transaction_list

def save_state(undo_stack:list,transaction_list:list):
    transactions=[t.copy() for t in transaction_list]
    undo_stack.append(transactions)

def perform_undo(undo_stack:list,transaction_list:list):
    if not undo_stack:
        return None
    transaction_list[:]=undo_stack.pop()
    return transaction_list
