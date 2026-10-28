import os
from typing import TypedDict
from transactions import (
    valid_date,
    create_date_list,
    add_new_transaction,
    read_update_transaction,
    update_transaction,
    transactions_sorted_by_date,
    print_transactions
)

from search import (
    get_transaction_bigger_than_a_threshold,
    trans_before_a_given_date,
    get_transaction_by_type
)

from reports import (
    transactions_sum_given_type,
    account_balance_at_given_date,
    transactions_type_ascending_order_by_sum
)

from delete import (
    delete_transactions_for_specified_date,
    delete_transactions_for_given_period,
    delete_transactions_of_given_type,
    delete_transactions_with_lower_sums_by_given_type
)

def clear_screen():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system("clear")

class AppState(TypedDict):
    transactions: list
    undo_stack: list
    balance: float

def delete_menu(app_state:AppState):
    while True:
        clear_screen()
        print("""
                1. Delete transactions by a specified date
                2. Delete transactions for a given time period
                3. Delete transactions of a given type
                4. Delete transactions by type with sums lower than a given amount
                0. Return to main menu
        """)
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                given_date = input("Enter a date: ")
                given_date = create_date_list(given_date)
                if not valid_date(given_date):
                    print("Invalid date! You have to enter a valid date!")
                else:
                    app_state["undo_stack"].append(list(app_state["transactions"]))
                    delete_transactions_for_specified_date(app_state["transactions"],given_date)
                input("Press enter to continue")
            case "2":
                date1 = input("Enter a date: ")
                date1 = create_date_list(date1)
                date2 = input("Enter a date: ")
                date2 = create_date_list(date2)
                if not (valid_date(date1) and valid_date(date2)):
                    print("Invalid date! You have to enter a valid time period!")
                else:
                    app_state["undo_stack"].append(list(app_state["transactions"]))
                    delete_transactions_for_given_period(app_state["transactions"],date1,date2)
                input("Press enter to continue")
            case "3":
                given_type=input("Enter the type of transactions(deposit/withdrawal): ")
                if given_type!="deposit" and given_type!="withdrawal":
                    print("Invalid input!")
                else:
                    app_state["undo_stack"].append(list(app_state["transactions"]))
                    delete_transactions_of_given_type(app_state["transactions"],given_type)
                input("Press enter to continue")
            case "4":
                given_type = input("Enter the type of transactions(deposit/withdrawal): ")
                if given_type != "deposit" and given_type != "withdrawal":
                    print("Invalid input!")
                else:
                    given_sum=float(input("Enter a sum: "))
                    if given_sum<=0:
                        print("Invalid input! The sum has to be a positive number")
                    else:
                        app_state["undo_stack"].append(list(app_state["transactions"]))
                        delete_transactions_with_lower_sums_by_given_type(app_state["transactions"],given_sum,given_type)
                input("Press enter to continue")
            case "0":
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")

def search_menu(app_state:AppState):
    while True:
        clear_screen()
        print("""
                1. Print all transactions with bigger sums than a given sum
                2. Print all transactions before a given date with bigger sums than a given sum
                3. Print all transactions of a given type
                0. Return to main menu
        """)
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                summ=float(input("Enter a sum: "))
                print(get_transaction_bigger_than_a_threshold(app_state["transactions"],summ))
                input("Press enter to continue")
            case "2":
                given_date=input("Enter a date: ")
                given_date= create_date_list(given_date)
                if not valid_date(given_date):
                    print("Invalid date! You have to enter a valid date!")
                else:
                    given_sum=float(input("Enter a sum: "))
                    if given_sum<=0:
                        print("Invalid input! You have to enter a valid sum!")
                    else:
                        print(trans_before_a_given_date(app_state["transactions"],given_date,given_sum))
                input("Press enter to continue")
            case "3":
                type = input("Enter the type of transaction: ")
                if type != "deposit" and type != "withdrawal":
                    print("Invalid input. Yoy have to enter a valid type (deposit/withdrawal)")
                else:
                    print(get_transaction_by_type(app_state["transactions"], type))
                input("Press enter to continue")
            case "0":
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")

def reports_menu(app_state:AppState):
    while True:
        clear_screen()
        print("""
                1. Total sum of transactions of a given type
                2. Account balance at a given date
                3. Print all transaction of a given type in ascending order
                0. Return to main menu
        """)
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                type=input("Enter the type of the transactions: ")
                if type != "deposit" and type != "withdrawal":
                    print("Invalid input. Yoy have to enter a valid type (deposit/withdrawal)")
                else:
                    print(transactions_sum_given_type(app_state["transactions"],type))
                input("Press enter to continue")
            case "2":
                given_date = input("Enter a date: ")
                given_date = create_date_list(given_date)
                if not valid_date(given_date):
                    print("Invalid date! You have to enter a valid date!")
                else:
                    print(account_balance_at_given_date(app_state["transactions"],given_date))
                input("Press enter to continue")
            case "3":
                given_type=input("Enter the type of transactions (deposit/withdrawal): ")
                if given_type != "deposit" and given_type != "withdrawal":
                    print("You have to enter a valid type!")
                else:
                    print(transactions_type_ascending_order_by_sum(app_state["transactions"],given_type))
                input("Press enter to continue")
            case "0":
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")

def main():
    app_state: AppState={
        "transactions":[],
        "undo_stack":[],
        "balance":0.0
    }
    while True:
        clear_screen()
        print("""
        1. Add transaction
        2. Delete
        3. Search
        4. Reports
        5. Undo
        6. Print transactions
        7. Update transaction
        0. Exit the program
        """)
        choice=input("Enter your choice: ")
        match choice:
            case "1":
                transaction=add_new_transaction()
                if transaction:
                    app_state["undo_stack"].append(list(app_state["transactions"]))
                    app_state["transactions"].append(transaction)
                    transactions_sorted_by_date(app_state["transactions"])
                    if transaction["type"]=="deposit":
                        app_state["balance"]+=transaction["sum"]
                    else:
                        app_state["balance"]-=transaction["sum"]
                input("Press enter to continue")
            case "2":
                delete_menu(app_state)
            case "3":
                search_menu(app_state)
            case "4":
                reports_menu(app_state)
            case "5":
                app_state["transactions"]=app_state["undo_stack"].pop()
                print("Undo done successfully!")
                input("Press enter to continue")
            case "6":
                print_transactions(app_state["transactions"])
                input("Press enter to continue")
            case "7":
                up_date=read_update_transaction(app_state["transactions"])
                if up_date:
                    old_transactions = []
                    for transactions in app_state["transactions"]:
                        old_transactions.append({
                            "date": list(transactions["date"]),
                            "sum": transactions["sum"],
                            "type": transactions["type"]
                        })
                    app_state["undo_stack"].append(old_transactions)
                    update_transaction(app_state["transactions"],up_date)
                    print("Transaction updated successfully!")
                input("Press enter to continue")
            case "0":
                print("Thank you for using this program! Have a good day!")
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")
