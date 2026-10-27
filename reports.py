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

def account_balance_at_given_date():
    pass