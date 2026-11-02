def save_state(undo_stack:list,transaction_list:list):
    transactions=[t.copy() for t in transaction_list]
    undo_stack.append(transactions)

def perform_undo(undo_stack:list,transaction_list:list):
    if not undo_stack:
        return None
    transaction_list[:]=undo_stack.pop()
    return transaction_list
