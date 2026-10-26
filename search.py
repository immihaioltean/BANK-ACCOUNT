def get_transaction_bigger_than_a_threshold(transaction_list:list,summ:float|int):
    """
    :param transaction_list (list)
    :param summ (float)
    :return: a list with all the transactions bigger than the input sum
    """
    result=[]
    for transaction in transaction_list:
        if transaction["sum"]>summ:
            result.append(transaction)
    return result

def trans_before_a_given_date(transaction_list:list,given_date:list,summ:float|int):
    """
    :param transaction_list - list of transactions
    :param given_date - list of numbers with the given date (day/month/year)
    :param summ (float|int) - the threshold given by the user
    :return: a list of transactions which transactions are made
             before a given date with bigger sums than a given sum
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
    result=[]
    for transaction in trans_list:
        if transaction["type"]==type_trans:
            result.append(transaction)
    return result