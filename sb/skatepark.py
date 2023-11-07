#skatepark.py
#By: Sam Schmitz
#the program that runs the stockBots connected to the server

from sb.stockServerV2 import sbServer
from sb.congressTrades import getTrades
import pyodbc
from datetime import datetime

class skatepark:

    def __init__(self, run=True):
        server = 'DESKTOP-T05LAAR\SBSERVER'
        database = 'CongressTrades'
        username = 'ss'
        password = 'SuperSoaker#295'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-T05LAAR\SBSERVER;DATABASE=CongressTrades;ENCRYPT=Optional;UID='+username+';PWD='+password+';')
        self.server = sbServer(cnxn, cnxn.cursor())
        if run == True: #if you are not going to run it you need to close the server
            self._run()

    def _run(self):
        print("Welcome to the skatepark")
        while True:
            print("Enter the name of the Bot you want to run or cancel")
            print("\t options: sb, ollie, kickflip, info, cancel")
            bot = input()
            if bot == "sb":
                print("enter the info for the fetch date:")
                print("year: ")
                y = int(input())
                print("month: ")
                m = int(input())
                print("day: ")
                d = int(input())
                date = datetime(y, m, d)
                self.sb(date)
            elif bot == "refresh":
                mems = []
                while True:
                    print("Enter a new member or n: ")
                    i = str(input())
                    if i == "n":
                        break
                    mems.append(i)
                if mems == []:
                    self.refresh()
                else:
                    self.refresh(mems)
                
            elif bot == "ollie":
                self.ollie()
            elif bot == "kickflip":
                self.kickflip()
            elif bot == "manual":
                self.manual()
            elif bot == "info":
                print("""sb: grabs the most recent trades from all members
                ollie: grabs trades from a selected member of congress
                kickflip: grabs trades from several mebers of congress (specified by the user)
                """)
            elif bot == "cancel":
                break
            else:
                print("Please select a valid option")
        self.server.close()

    def sb(self, date):
        trades = getTrades(date)
        self.server.add_trades(trades)

    def refresh(self, members=None):
        if members != None:
            self.server.refresh_server(members)
        else:
            self.server.refresh_server()

    def ollie(self):
        print("this function is not currently active. Please select another one")

    def kickflip(self):
        print("this function is not currently active. Please select another one")

    def manual(self):
        print("this function is not currently active. Please select another one")

if __name__ == "__main__":
    skatepark = skatepark()
