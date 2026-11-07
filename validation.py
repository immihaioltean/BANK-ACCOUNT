from datetime import date

def valid_date(date_trans:list):
    """
    Check if the date is valid for the transaction (considering it took place after 1900)
    :param date_trans(list) - [day,month,year]
    :return: True if the date is valid, False otherwise
    """
    if date_trans[2] < 1900 or date_trans[2] > date.today().year:
        raise ValueError("Please enter a valid date (day/month/year)")
    elif date_trans[1] < 1 or date_trans[1] > 12:
        raise ValueError("Please enter a valid date (day/month/year)")
    else:
        if date_trans[1] < 8 and date_trans[1] % 2 and (date_trans[0] > 31 or date_trans[0] < 1):
            raise ValueError("Please enter a valid date (day/month/year)")
        elif date_trans[1] == 2:
            if date_trans[2] % 4 == 0 and date_trans[2] % 100 or date_trans[2] % 400 == 0:
                if date_trans[0] < 0 or date_trans[0] > 29:
                    raise ValueError("Please enter a valid date (day/month/year)")
            elif date_trans[0] < 0 or date_trans[0] > 28:
                raise ValueError("Please enter a valid date (day/month/year)")
        elif ((3 < date_trans[1] < 7 or 8 < date_trans[1] < 12) and date_trans[1] % 2 == 0
              and (date_trans[0] < 0 or date_trans[0] > 30)):
            raise ValueError("Please enter a valid date (day/month/year)")
    return True

def validate_date_input(data:str):
    data=data.strip()
    if not 9<=len(data)<=10:
        raise ValueError("Please enter a valid date (day/month/year)")
    for i in data:
        if not i.isdigit() and i!="." and i!="/":
            raise ValueError("Please enter a valid date (day/month/year)")

def validate_type(type:str):
    if type!="deposit" and type!="withdrawal":
        raise NameError("Please enter either 'deposit' or 'withdrawal'")

def validate_sum(input_sum:float):
    if input_sum<=0:
        raise ValueError("Please enter a positive number")