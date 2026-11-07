import os
from typing import TypedDict
from service import (
    create_date_list,
    add_transaction,
    update_transaction,
    transactions_sorted_by_date,
    print_transactions,
    copy_transactions,
    get_transaction_bigger_than_a_threshold,
    trans_before_a_given_date,
    get_transaction_by_type,
    transactions_sum_given_type,
    account_balance_at_given_date,
    transactions_type_ascending_order_by_sum,
    delete_transactions_for_specified_date,
    delete_transactions_for_given_period,
    delete_transactions_of_given_type,
    delete_transactions_with_lower_sums_by_given_type,
    save_state,
    perform_undo
)

from validation import (
    valid_date,
    validate_date_input,
    validate_sum,
    validate_type
)

from domain import (
    create_transaction,
    get_date,
    get_sum,
    get_type
)

def clear_screen():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system("clear")

class AppState(TypedDict):
    transactions: list
    undo_stack: list

def read_valid_date(message):
    while True:
        try:
            given_date = input(message)
            validate_date_input(given_date)
            given_date = create_date_list(given_date)
            valid_date(given_date)
            return given_date
        except ValueError as e:
            print(f"Invalid value. {e}")

def read_valid_sum(message):
    while True:
        try:
            given_sum = float(input(message))
            validate_sum(given_sum)
            return given_sum
        except ValueError as e:
            print(f"Invalid value. {e}")

def read_valid_type(message):
    while True:
        try:
            given_type = input(message)
            validate_type(given_type)
            return given_type
        except NameError as e:
            print(f"Invalid type. {e}")

def read_transaction():
    date = read_valid_date("Enter the date of the transaction (day/month/year):")
    summ = read_valid_sum("Enter the sum of the transaction:")
    type = read_valid_type("Enter the type of transaction (deposit/withdrawal):")
    return create_transaction(date,summ,type)

def read_update_transaction(transaction_list:list):
    update = read_valid_date("Enter the date of the transaction you would like to update (day/month/year): ")
    index = -1
    length = len(transaction_list)
    pos = 0
    for transaction in range(length):
        if get_date(transaction_list[transaction]) == update:
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
            for data in get_date(transaction_list[transaction]):
                print(data, end=" ")
            print(f"and it was a {get_type(transaction_list[transaction])}"
                  f" of {get_sum(transaction_list[transaction])}")
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

def print_delete_menu():
    print("""
            1. Delete transactions by a specified date
            2. Delete transactions for a given time period
            3. Delete transactions of a given type
            4. Delete transactions by type with sums lower than a given amount
            0. Return to main menu
    """)

def delete_menu(app_state:AppState):
    while True:
        clear_screen()
        print_delete_menu()
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                given_date = read_valid_date("Enter a date: ")
                save_state(app_state["undo_stack"],app_state["transactions"])
                delete_transactions_for_specified_date(app_state["transactions"],given_date)
                input("Press enter to continue")
            case "2":
                date1 = read_valid_date("Enter a date: ")
                date2 = read_valid_date("Enter a date: ")
                if date1[::-1] > date2[::-1] :
                    print("Invalid date! You have to enter a valid time period!")
                else:
                    save_state(app_state["undo_stack"], app_state["transactions"])
                    delete_transactions_for_given_period(app_state["transactions"],date1,date2)
                input("Press enter to continue")
            case "3":
                given_type = read_valid_type("Enter the type of transactions(deposit/withdrawal): ")
                save_state(app_state["undo_stack"], app_state["transactions"])
                delete_transactions_of_given_type(app_state["transactions"],given_type)
                input("Press enter to continue")
            case "4":
                given_type = read_valid_type("Enter the type of transactions(deposit/withdrawal): ")
                given_sum = read_valid_sum("Enter a sum: ")
                save_state(app_state["undo_stack"], app_state["transactions"])
                delete_transactions_with_lower_sums_by_given_type(app_state["transactions"],given_sum,given_type)
                input("Press enter to continue")
            case "0":
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")

def print_search_menu():
    print("""
            1. Print all transactions with bigger sums than a given sum
            2. Print all transactions before a given date with bigger sums than a given sum
            3. Print all transactions of a given type
            0. Return to main menu
     """)

def search_menu(app_state:AppState):
    while True:
        clear_screen()
        print_search_menu()
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                summ = read_valid_sum("Enter a sum: ")
                print(get_transaction_bigger_than_a_threshold(app_state["transactions"],summ))
                input("Press enter to continue")
            case "2":
                given_date = read_valid_date("Enter a date: ")
                given_sum = read_valid_sum("Enter a sum: ")
                print(trans_before_a_given_date(app_state["transactions"],given_date,given_sum))
                input("Press enter to continue")
            case "3":
                type = read_valid_type("Enter the type of transaction: ")
                print(get_transaction_by_type(app_state["transactions"], type))
                input("Press enter to continue")
            case "0":
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")

def print_reports_menu():
    print("""
            1. Total sum of transactions of a given type
            2. Account balance at a given date
            3. Print all transaction of a given type in ascending order
            0. Return to main menu
    """)

def reports_menu(app_state:AppState):
    while True:
        clear_screen()
        print_reports_menu()
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                type = read_valid_type("Enter the type of the transactions: ")
                print(transactions_sum_given_type(app_state["transactions"],type))
                input("Press enter to continue")
            case "2":
                given_date = read_valid_date("Enter a date: ")
                print(account_balance_at_given_date(app_state["transactions"],given_date))
                input("Press enter to continue")
            case "3":
                given_type = read_valid_type("Enter the type of transactions (deposit/withdrawal): ")
                print(transactions_type_ascending_order_by_sum(app_state["transactions"],given_type))
                input("Press enter to continue")
            case "0":
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")

def print_main_menu():
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

def main():
    app_state: AppState={
        "transactions":[],
        "undo_stack":[],
    }
    while True:
        clear_screen()
        print_main_menu()
        choice=input("Enter your choice: ")
        match choice:
            case "1":
                save_state(app_state["undo_stack"], app_state["transactions"])
                transaction = read_transaction()
                add_transaction(app_state["transactions"],transaction)
                transactions_sorted_by_date(app_state["transactions"])
                input("Press enter to continue")
            case "2":
                delete_menu(app_state)
            case "3":
                search_menu(app_state)
            case "4":
                reports_menu(app_state)
            case "5":
                if not app_state["undo_stack"]:
                    print("Nothing to undo!")
                else:
                    perform_undo(app_state["undo_stack"], app_state["transactions"])
                    print("Undo done successfully!")
                input("Press enter to continue")
            case "6":
                print_transactions(app_state["transactions"])
                input("Press enter to continue")
            case "7":
                up_date = read_update_transaction(app_state["transactions"])
                if up_date:
                    app_state["undo_stack"].append(copy_transactions(app_state["transactions"]))
                    update_transaction(app_state["transactions"],up_date)
                    print("Transaction updated successfully!")
                input("Press enter to continue")
            case "0":
                print("Thank you for using this program! Have a good day!")
                break
            case _:
                print("Invalid choice!")
                input("Press enter to continue")
