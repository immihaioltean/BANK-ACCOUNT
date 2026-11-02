def get_date(transactions:dict):
    return transactions["date"]

def get_sum(transactions:dict):
    return transactions["sum"]

def get_type(transactions:dict):
    return transactions["type"]

# def create_transaction(date,summ,type):
#     return dict(date=date,sum=summ,type=type)

def set_date(transactions,date):
    transactions["date"] = date

def set_sum(transactions,summ):
    transactions["sum"] = summ

def set_type(transactions,type):
    transactions["type"] = type