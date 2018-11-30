#!/usr/bin/python
from stocker import *
from threading import Thread
import csv
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import difflib

def main():
    print_intro()
    get_company()

def handle_company_input(company):
    if company.strip() in stock_dict.keys():
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

    if len(datasets) == 1:
        print("No results found. Would you like to search again? \n")
        ans = input("[Y]es or [n]\n")
        if ans[0].lower().strip() == 'y':
            print("What would you like to search? ")
            comp = input("Enter a company name: ")
            print(comp)
            perform_search(comp)
        else:
            exit()

    print (datasets[1:])
    search_stock_name()

def search_stock_name():
    ans = input("Now that you have seen the stocks, would you like to [e]nter the NASDAQ code,\n [s]earch again, or [q]uit?\n")
    if ans.lower().strip()[0] == 'q':
        exit()
    elif ans.lower().strip()[0] == 'e':
        ticker = input("Please enter the NASDAQ code: ")
        search_db(ticker)
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
        print("Do you want the stock for", ticker+ "?\n")
        ans = input("[Y]es or [n]o: ")
        if ans[0].lower().strip() == 'y':
            make_stock(ticker)
        else:
            print("Invalid command")
            search_db(ticker)
            # exit()

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



def manipulate_stock(company_stock):
    print("\n\n\n\n\n\nNow, I can offer some commands to you. ")
    print("'Graph' graphs the stock, 'buy and hold' will simulate you buying n shares on X date and "
    "holding them until Y date, 'model' will create a model that predicts the stock price for 30 days, "
    "'changepoint' willl graph the changepoints of the stock and 'predict n' will predict the price in n "
    "days. You can also use the 'help' command to access this list of commands and 'quit' to quit the application")
    stock_loop(company_stock)

def stock_loop(company_stock):
    ans = ""
    while(True):
        print("The current stock you loaded up is", company_stock.symbol)
        ans = input("What would you like to do? ")
        if not parse_input(ans):
            continue
        else:
            print("Valid")



def parse_input(ans):
    cmds = ['help', 'graph', 'buy and hold', 'model', 'changepoint', "quit"]

    if ans in cmds:
        ind = cmds.index(ans)
        switcher = {
            0: print_help,
            1: graph_stock,
            2: buy_and_hold_stock,
            3: model_stock,
            4: changepoint_stock,
            5: exit
        }
        func = switcher[ind]
        func()
        return True
    else:
        print("Invalid command. You might have meant:", difflib.get_close_matches(ans, cmds))
        return False

def print_help():
    help = ("Graph' graphs the stock, 'buy and hold' will simulate you buying n shares on X date and "
    "holding them until Y date, 'model' will create a model that predicts the stock price for 30 days, "
    "'changepoint' willl graph the changepoints of the stock and 'predict n' will predict the price in n "
    "days.")
    print(help)

def graph_stock():
    print("graph")
def buy_and_hold_stock():
    print("buy and hold")
def model_stock():
    print("nodel!")
def changepoint_stock():
    print("changepoint!")

if __name__ == '__main__':
    Thread(target = main).start()
    Thread(target = load_db).start()
