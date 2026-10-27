def delete_transactions_for_specified_date(transaction_list:list,given_date:list):
    #return [transaction for transaction in transaction_list if transaction_list["date"]!=given_date]
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
