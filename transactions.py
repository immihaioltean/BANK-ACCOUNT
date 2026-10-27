from datetime import date

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

def add_new_transaction():
    """
    Add a new transaction to the list
    date (list) - [day,month,year]
    sum (float)
    type (str) - "deposit" or "withdrawal"
    :return: return None if the transaction is invalid or
             a dictionary with the transaction details (date,sum,type)
    """
    date_trans=input("Enter the date of the transaction (day/month/year): ")
    date_trans=date_trans.strip().replace("."," ").replace("/"," ").replace(","," ").split()
    date_trans=[int(str_date) for str_date in date_trans]

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
        if int(sum_trans)==float(sum_trans):
            sum_trans=int(sum_trans)
        print(f"The sum of the transaction is: {sum_trans}")

    type_trans=input("Enter the type of the transaction (deposit/withdrawal): ")
    if type_trans!="deposit" and type_trans!="withdrawal":
        print("Invalid input. Yoy have to enter a valid type!")
        return None
    else:
        print(f"Transaction added successfully!")

    return {"date":date_trans,"sum":sum_trans,"type":type_trans}

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

def update_transaction(transaction_list:list,update:list):
    index=-1
    length=len(transaction_list)
    pos=0
    for transaction in range(length):
        if transaction_list[transaction]["date"]==update:
            index+=1
            pos=transaction
    if index<0:
        print("No transaction found!")
        return None
    choice=0
    if index>0:
        print("Which transaction would you like to update?")
        for transaction in range(pos-index,pos+1):
            print(f"{transaction}. Transaction took place on: ", end="")
            for data in transaction_list[transaction]["date"]:
                print(data, end=" ")
            print(f"and it was a {transaction_list[transaction]["type"]}"
                  f" of {transaction_list[transaction]["sum"]}")
        choice=int(input("Enter your choice: "))
        if not pos-index<=choice<=pos:
            print("Invalid choice!")
            return None
    if index>0: index=choice
    print("What you would like to update? Enter sum for sum, type for type or both")
    choice=input("Enter your choice: ")
    match choice:
        case "sum":
            new_sum=float(input("Enter the new sum: "))
            #account_balance["balance"]+=new_sum-transaction_list[index]["sum"]
            transaction_list[index]["sum"]=new_sum
        case "type":
            new_type=input("Enter the new type: ")
            transaction_list[index]["type"]=new_type
        case "both":
            new_sum = float(input("Enter the new sum: "))
            transaction_list[index]["sum"] = new_sum
            new_type = input("Enter the new type: ")
            transaction_list[index]["type"] = new_type
        case _:
            print("Invalid choice!")
    print("Transaction updated successfully!")
    return transaction_list
