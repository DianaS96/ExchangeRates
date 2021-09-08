# Import Dynamics of the official exchange rates
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#
def check_curr():
    currency = {"USD": "R01235", "EUR": "R01239"}
    curr = input("Enter the currency (USD/EUR): ").upper()
    if curr.upper() in currency.keys():
        check_date(curr, currency.get(curr))
    else:
        print("Invalid currency. Try again")
        check_curr()

# Function check_date() check whether input date is correct. If date is invalid, you should enter the date again
def check_date(curr, curr_id):
    flag = 0
    today = time.localtime() # Current date

    while flag == 0:
        start_date = input("Enter start date (dd/mm/yyyy): ")
        end_date = input("Enter end date (dd/mm/yyyy): ")
        try:
            valid_start_date = time.strptime(start_date, '%d/%m/%Y')
            valid_end_date = time.strptime(end_date, '%d/%m/%Y')
            flag = 1
            if valid_start_date > today:
                if (valid_start_date.tm_year == today.tm_year and valid_start_date.tm_mon == today.tm_mon and valid_start_date.tm_mday == (today.tm_mday + 1)):
                    flag = 1
                else:
                    flag = 0
                    print(f"This date ({valid_start_date}) hasn't come yet!")
            if valid_end_date > today:
                if (valid_end_date.tm_year == today.tm_year and valid_end_date.tm_mon == today.tm_mon and valid_end_date.tm_mday == (today.tm_mday + 1)):
                    flag = 1
                else:
                    flag = 0
                    print(f"This date ({valid_end_date}) hasn't come yet!")
            if valid_end_date < valid_start_date:
                flag = 0
                print("Ooooops, start_date should be earlier than end_date!")
        except ValueError:
            print("Invalid date")
        get_data(valid_start_date, valid_end_date, curr, curr_id)

# Function get_data gets input from cbr website
def get_data(start_date, end_date, curr, curr_id):
    list_data = list()
    list_header = ["Дата", "Единиц", "Курс"]
    url = "https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ="\
          + curr_id + "&UniDbQuery.From=" + f'{int(start_date.tm_mday):02}' + "." + f'{int(start_date.tm_mon):02}' + "." + str(start_date.tm_year) \
    + "&UniDbQuery.To=" + f'{int(end_date.tm_mday):02}' + "." + f'{int(end_date.tm_mon):02}' + "." + str(end_date.tm_year)

    resp = requests.get(url)
    tree = BeautifulSoup(resp.content, "html.parser")

    data = tree.find_all('table')[0].find_all('tr')[2:]
    for elem in data:
        sub_table = list()
        for sub_elem in elem:
            try:
                sub_table.append(sub_elem.get_text())
            except:
                continue
        list_data.append(sub_table)
    df = pd.DataFrame(data=list_data, columns=list_header)

    # Write data in a csv file
    sdate = str(start_date.tm_mday) + "." + str(start_date.tm_mon) + "." + str(start_date.tm_year)
    edate = str(end_date.tm_mday) + "." + str(end_date.tm_mon) + "." + str(end_date.tm_year)
    df.to_csv(f"Курсы {curr} с {sdate} по {edate}.csv", encoding='utf-8-sig')