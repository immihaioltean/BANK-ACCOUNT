from transactions import (valid_date,
    transactions_sorted_by_date,
    create_date_list
)
from search import (get_transaction_bigger_than_a_threshold,
    trans_before_a_given_date,
    get_transaction_by_type
)
from reports import (transactions_sum_given_type,
    transactions_type_ascending_order_by_sum,
    account_balance_at_given_date
)
from delete import (delete_transactions_for_specified_date,
    delete_transactions_for_given_period,
    delete_transactions_of_given_type,
    delete_transactions_with_lower_sums_by_given_type
)
def test_valid_date():
    table_test=[
        ([28,3,2017],True),
        ([29,2,2019],False),
        ([29,2,2020],True),
    ]
    for date_trans,result in table_test:
        assert valid_date(date_trans)==result

def test_create_date_list():
    table_test=[
        ("23.10.2024",[23,10,2024]),
        ("23,05/2005",[23,5,2005]),
        ("   14.12,2000   ",[14,12,2000])
    ]
    for string,date_list in table_test:
        assert create_date_list(string)==date_list

def test_get_transaction_bigger_than_a_threshold():
    table_test=[
        ([{"date":[23,10,2010],"sum":50,"type":"deposit"}],30,
         [{"date":[23,10,2010],"sum":50,"type":"deposit"}]),
        ([{"date":[18,9,2020],"sum":100,"type":"deposit"}],2000,[])
    ]
    for start,input_sum,result in table_test:
        assert get_transaction_bigger_than_a_threshold(start,input_sum)==result

def test_trans_before_a_given_date():
    table_test=[
        ([{"date":[23,10,2020],"sum":50,"type":"deposit"}],[28,12,2024],300,[]),
        ([{"date": [23, 10, 2020], "sum": 500, "type": "deposit"}], [28, 12, 2024], 300,
         [{"date": [23, 10, 2020], "sum": 500, "type": "deposit"}]),
        ([{"date": [28, 9, 2020], "sum": 1000, "type": "deposit"}], [28, 12, 2018], 300, [])
    ]
    for transaction_list,given_date,given_sum,result in table_test:
        assert trans_before_a_given_date(transaction_list,given_date,given_sum)==result

def test_get_transaction_by_type():
    table_test=[
        ([{"date":[23,5,2007],"sum":30,"type":"deposit"},
          {"date":[28,11,2022],"sum":40,"type":"withdrawal"},
          {"date":[19,10,2025],"sum":20,"type":"deposit"}],
         "deposit",
         [{"date":[23,5,2007],"sum":30,"type":"deposit"},
          {"date":[19,10,2025],"sum":20,"type":"deposit"}]),
        ([{"date":[23,5,2007],"sum":40,"type":"withdrawal"}],"deposit",[]),
        ([{"date": [28, 10, 2015], "sum": 30, "type": "deposit"}], "withdrawal", [])
    ]
    for strat,type_trans,result in table_test:
        assert get_transaction_by_type(strat,type_trans)==result

def test_transactions_sum_given_type():
    table_test=[
        ([{"date":[21,10,2011],"sum":100,"type":"deposit"},
          {"date":[18,12,2023],"sum":400,"type":"deposit"},
          {"date":[19,11,2001],"sum":500,"type":"deposit"}],"deposit",1000),
        ([{"date": [21, 10, 2011], "sum": 100, "type": "deposit"},
          {"date": [18, 12, 2023], "sum": 400, "type": "deposit"},
          {"date": [19, 11, 2001], "sum": 500, "type": "withdrawal"}], "deposit", 500),
        ([{"date": [21, 10, 2011], "sum": 100, "type": "deposit"},
          {"date": [19, 11, 2001], "sum": 300, "type": "withdrawal"}], "withdrawal", 300),
        ([{"date": [19, 11, 2001], "sum": 500, "type": "withdrawal"}], "deposit", 0),
        ([{"date": [19, 11, 2001], "sum": 37.91, "type": "deposit"}], "deposit", 37.91)
    ]
    for start,type,result in table_test:
        assert transactions_sum_given_type(start,type)==result

def test_transactions_sorted_by_date():
    table_test=[
        ([{"date":[21,10,2011],"sum":100,"type":"deposit"},
          {"date":[12,11,2008],"sum":500,"type":"deposit"},
          {"date":[21,11,2011],"sum":1000,"type":"deposit"}],
         [{"date":[12,11,2008],"sum":500,"type":"deposit"},
          {"date":[21,10,2011],"sum":100,"type":"deposit"},
          {"date":[21,11,2011],"sum":1000,"type":"deposit"}])
    ]
    for start,result in table_test:
        assert transactions_sorted_by_date(start)==result

def test_delete_transactions_for_specified_date():
    table_test=[
        ([{"date":[21,10,2011],"sum":100,"type":"deposit"},
          {"date":[21,10,2011],"sum":400,"type":"deposit"},
          {"date":[19,11,2001],"sum":500,"type":"deposit"}],
         [21,10,2011],
         [{"date":[19,11,2001],"sum":500,"type":"deposit"}]),
        ([{"date":[21,10,2011],"sum":100,"type":"deposit"},
          {"date":[21,10,2011],"sum":400,"type":"deposit"},
          {"date":[21,10,2011],"sum":500,"type":"deposit"}],[21,10,2011],[])
    ]
    for start,given_date,result in table_test:
        assert delete_transactions_for_specified_date(start,given_date)==result

def test_delete_transactions_for_given_period():
    table_test=[
        ([{"date": [21, 10, 2011], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2011], "sum": 400, "type": "deposit"},
          {"date": [21, 10, 2011], "sum": 500, "type": "deposit"}],
         [21, 10, 2011], [23,4,2026],[]),
        ([{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"},
          {"date": [21, 10, 2013], "sum": 500, "type": "deposit"}],
         [21, 10, 2008],[24,12,2016], [{"date": [21, 10, 2017], "sum": 400, "type": "deposit"}]),
        ([{"date":[23,10,2020],"sum":50,"type":"deposit"}],
         [12,5,2014],[23,10,2018],
         [{"date":[23,10,2020],"sum":50,"type":"deposit"}])
    ]
    for start,date1,date2,result in table_test:
        assert delete_transactions_for_given_period(start,date1,date2)==result

def test_delete_transactions_of_given_type():
    table_test=[
        ([{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}],"deposit",[]),
        ([{"date": [21, 10, 2008], "sum": 100, "type": "withdrawal"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}],"withdrawal",
         [{"date": [21, 10, 2017], "sum": 400, "type": "deposit"}])
    ]
    for start,given_type,result in table_test:
        assert delete_transactions_of_given_type(start,given_type)==result

def test_delete_transactions_with_lower_sums_by_given_type():
    table_test=[
        ([{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}],500, "deposit", []),
        ([{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}], 500, "withdrawal",
         [{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}]),
        ([{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}],50,"deposit",
         [{"date": [21, 10, 2008], "sum": 100, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 400, "type": "deposit"}]
         )
    ]
    for start,given_sum,given_type,result in table_test:
        assert delete_transactions_with_lower_sums_by_given_type(start,given_sum,given_type)==result

def test_transactions_type_ascending_order_by_sum():
    table_test=[
        ([{"date": [21, 10, 2008], "sum": 400, "type": "deposit"},
          {"date": [21, 10, 2017], "sum": 100, "type": "deposit"}],"deposit",
         [{"date": [21, 10, 2017], "sum": 100, "type": "deposit"},
           {"date": [21, 10, 2008], "sum": 400, "type": "deposit"}]),
        ([{"date":[23,10,2020],"sum":50,"type":"withdrawal"}],"deposit",[]),
        ([{"date":[21,10,2011],"sum":600,"type":"withdrawal"},
          {"date":[21,10,2011],"sum":500,"type":"withdrawal"},
          {"date":[19,11,2001],"sum":100,"type":"deposit"}],"withdrawal",
         [{"date":[21,10,2011],"sum":500,"type":"withdrawal"},
          {"date":[21,10,2011],"sum":600,"type":"withdrawal"}])
    ]
    for start,type,result in table_test:
        assert transactions_type_ascending_order_by_sum(start,type)==result

def test_account_balance_at_given_date():
    table_test=[
        ([{"date":[12,11,2008],"sum":500,"type":"withdrawal"},
          {"date":[21,10,2011],"sum":100,"type":"deposit"},
          {"date":[31,12,2020],"sum":1000,"type":"deposit"}],[15,3,2015],-400),
        ([{"date":[31,12,2020],"sum":1000,"type":"deposit"}],[14,3,2010],0),
        ([{"date":[31,12,2020],"sum":1000,"type":"deposit"}],[16,6,2025],1000)
    ]
    for start,given_date,result in table_test:
        assert account_balance_at_given_date(start,given_date)==result

def run_all_tests():
    test_valid_date()
    test_create_date_list()
    test_transactions_sorted_by_date()
    test_delete_transactions_for_specified_date()
    test_delete_transactions_for_given_period()
    test_delete_transactions_of_given_type()
    test_get_transaction_bigger_than_a_threshold()
    test_trans_before_a_given_date()
    test_get_transaction_by_type()
    test_transactions_sum_given_type()
    test_account_balance_at_given_date()
    test_transactions_type_ascending_order_by_sum()
    test_delete_transactions_with_lower_sums_by_given_type()