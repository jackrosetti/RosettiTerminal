#!/usr/bin/python
from stocker import Stocker
from threading import Thread
import csv
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

def main():
    print_intro()
    get_company()

def handle_company_input(company):
    if company in stock_dict.keys():
        print("Do you want the stock for", company, "which has the NASDAQ code:", stock_dict[company]+"?")
        ans = input("[Y]es or [n]o: ")
        if ans[0].lower().strip() == 'y':
            make_stock(stock_dict[company])
        else:
            exit()
    else:
        print("Could not find that company in the NASDAQ database. Would you like to find the closest results?")
        ans = input("[Y]es or [N]o?\n")
        if ans.strip().lower() == 'y':
            perform_search(company)

        elif ans.strip().lower() == 'n':
            thanos_car = ("Would you like to [c]ontinue or [q]uit?")
            if thanos_car.lower().strip() == 'c':
                get_company()
            elif thanos_car.lower().strip() == 'q':
                exit()
        else:
            print("Not a valid command")

def perform_search(company):
    url = 'https://www.nasdaq.com/symbol/?Load=true&Search='+company

    text_soup = BeautifulSoup(urlopen(url).read(),features="lxml") #read in
    table = text_soup.find("div", attrs={"class":"genTable"})
    datasets = []
    for row in table.find_all("tr"):
        dataset = list(td.get_text() for td in row.find_all("td"))
        datasets.append(dataset)

    if "[]" in datasets:
        datasets.remove("[]")
        datasets.remove("[[")
        datasets.remove("]]")
    print (datasets[1:])
    search_stock_name()

def search_stock_name():
    ans = ("Now that you have seen the stocks, would you like to [e]nter the NASDAQ code, [s]earch again, or [q]uit?\n")
    if ans.lower().strip()[0] == 'q':
        exit()
    elif ans.lower().strip()[0] == 'e':
        ticker = input("Please enter the NASDAQ code: ")
        search_db(ticker.upper().strip())
    elif ans.lower().strip()[0] == 's':
        comp = input("Which company do you want to look up? \n")
        perform_search(comp)

def print_intro():
    print("Welcome to the Rosetti Terminal -- a knockoff Bloomberg terminal!")
    # print("Commands are 'help,' 'stock history,' and 'quit.' ")
    return

def search_db(t):
    ticker = t.upper().strip()
    if ticker in stock_dict.values():
        print("Do you want the stock for", stock_dict[ticker], "which has the NASDAQ code:",ticker+"?\n")
        ans = input("[Y]es or [n]o: ")
        if ans[0].lower().strip() == 'y':
            make_stock(ticker)
        else:
            exit()


def dichotomy(text_to_print, func1, func2):
    if text_to_print != None:
        print(text_to_print)
    ans = input("[Y]es or [n]")
    if ans[0].lower().strip() == 'y':
        func1()
    else:
        func2()

def get_company():
    print("To begin, please enter a company to get its stock ticker!")
    ans = input("Company: ")
    handle_company_input(ans)

def load_db():
    global stock_dict
    stock_dict = {row[1] : row[0] for _, row in pd.read_csv("companylist.csv").iterrows()}
    return

def make_stock(company):
    company_stock = Stocker(company)
    manipulate_stock(company_stock)

commands = ("Graph' graphs the stock, 'buy and hold' will simulate you buying n shares on X date and \n"
"holding them until Y date, 'model' will create a model that predicts the stock price for 30 days, \n"
"'changepoint' willl graph the changepoints of the stock and 'predict n' will predict the price in n\n"
"days.")

def manipulate_stock(company_stock):
    print("Now, I can offer some commands to you. ")
    print("'Graph' graphs the stock, 'buy and hold' will simulate you buying n shares on X date and \n"
    "holding them until Y date, 'model' will create a model that predicts the stock price for 30 days, \n"
    "'changepoint' willl graph the changepoints of the stock and 'predict n' will predict the price in n\n"
    "days. You can also use the 'help' command to access this list of commands. ")
    stock_loop()

def stock_loop():
    while(True):
        


if __name__ == '__main__':
    Thread(target = main).start()
    Thread(target = load_db).start()
