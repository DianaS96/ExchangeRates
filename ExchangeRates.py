# Import official exchange rates on selected date from CBR.RU
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function check_date() check whether input date is correct. If date is invalid, you should enter the date again
def check_date():
    flag = 0
    today = time.localtime() # Current date

    while flag == 0:
        day = input("Enter day: ")
        month = input("Enter month: ")
        year = input("Enter year: ")
        date_inp = day + '/' + month + '/' + year # Concatenate day, month and year
        try:
            valid_date = time.strptime(date_inp, '%d/%m/%Y')
            flag = 1
            if valid_date > today:
                if (valid_date.tm_year == today.tm_year and valid_date.tm_mon == today.tm_mon and valid_date.tm_mday == (today.tm_mday + 1)):
                    flag = 1
                else:
                    flag = 1
                    print("This date hasn't come yet!")
        except ValueError:
            print("Invalid date")
        get_data(day, month, year, date_inp)

# Function get_data gets input from cbr website
def get_data(day, month, year, date_inp):
    list_data = list()
    list_header = []
    url = "https://www.cbr.ru/currency_base/daily/" + "?UniDbQuery.Posted=True&UniDbQuery.To=" + f'{int(day):02}' + "." + f'{int(month):02}' + "." + str(year)
    resp = requests.get(url)
    tree = BeautifulSoup(resp.content, "html.parser")
    #print(tree)
    #date = tree.find("button", {"class":"datepicker-filter_button"})

    # find table on the website
    header = tree.find_all('table')[0].find('tr')
#    print(header)
    for item in header:
        try:
            list_header.append(item.text)
        except:
            continue

    data = tree.find_all('table')[0].find_all('tr')[1:]
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
    df.to_csv((str("Курсы на " + str(date_inp).replace('/', '.')) + ".csv"), encoding='utf-8-sig')
