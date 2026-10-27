def save_undo_stack():
    undo_stack.append((transaction_list, account_balance["balance"]))

def undo():
    pass