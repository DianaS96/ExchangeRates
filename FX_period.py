# Import Dynamics of the official exchange rates
import csv

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import pandas as pd
from datetime import datetime

# Function check_date() check whether input date is correct. If date is invalid, you should enter the date again
def check_date():
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
    date_range(valid_start_date, valid_end_date)

def date_range(start, end):
    start = datetime(start.tm_year, start.tm_mon, start.tm_mday)
    end = datetime(end.tm_year, end.tm_mon, end.tm_mday)
    daterange = pd.date_range(start, end)
    # for date in daterange:
    #      print(date.strftime("%d.%m.%Y"))
    get_data(daterange, start, end)

def get_data(daterange, start, end):
    count = 0
    for date in daterange:
        url = "https://www.cbr.ru/currency_base/daily/" + "?UniDbQuery.Posted=True&UniDbQuery.To=" + str(date)[8:11].strip() + "." + str(date)[5:7] + "." + str(date)[:4]
        # Adding headers (names of the currencies) to csv file
        if count == 0:
            header = list()
            header.append("Дата")
            r = requests.get(url=url)
            soup = BeautifulSoup(r.text, "html.parser")
            data = soup.find_all('table')[0].find_all('tr')[1:]
            for item in data:
                title = item.find_all("td")[1]
                header.append(title.text)

            with open(f"FX from {str(start)[:9]} to {str(end)[:9]}.csv", "w", encoding="UTF-8-sig", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)

        # Adding FX for each currency for each date from the given range
        fx_list = list()
        fx_list.append(date)
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, "html.parser")
        data = soup.find_all('table')[0].find_all('tr')[1:]
        for item in data:
            fx = item.find_all("td")[4]
            fx_list.append(fx.text)

        with open(f"FX from {str(start)[:9]} to {str(end)[:9]}.csv", "a", encoding="UTF-8-sig", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fx_list)

        count += 1
