from inilib import ini_config
from encryptlib import msgEnc
from dblib import db_method

accessFlag = False

def accessDependant(func):
    def wrapper(*args, **kwargs):
        if accessFlag:
            func(*args, **kwargs)
        else:
            print("Account Access Not Given")
    return wrapper

class access_acc:

    def access(bsb, accnum, userid, passwd):
        try:
            if ini_config.checkSec(bsb + " " + accnum) == True and ini_config.getValue(str(bsb + " " + accnum), "uid") == userid:
                global accessFlag
                accessFlag = True
                return True
            else:
                return False
        except KeyError:
            return False

    @accessDependant
    def getBalance(bsb, accnum):
        if ini_config.checkSec(bsb + " " + accnum) == True:
            return int(ini_config.getValue(str(bsb + " " + accnum), "bal"))

    @accessDependant
    def withdraw(bsb, accnum, amount):
        if ini_config.checkSec(bsb + " " + accnum) == True and int(ini_config.getValue(str(bsb + " " + accnum), "bal")) >= amount:
            camt = int(ini_config.getValue(str(bsb + " " + accnum), "bal"))
            ini_config.writeValue(str(bsb + " " + accnum), "bal", str(camt - amount))
            print("Withdrawn: $" + str(amount))
            print("Account Balance: $" + str(camt - amount))
        else:
            print("Invalid account details or amount")

    @accessDependant
    def deposit(bsb, accnum, amount):
        if ini_config.checkSec(bsb + " " + accnum) == True:
            camt = int(ini_config.getValue(str(bsb + " " + accnum), "bal"))
            ini_config.writeValue(str(bsb + " " + accnum), "bal", str(camt + amount))
            print("Deposited: $" + str(amount))
            print("Account Balance: $" + str(camt + amount))
        else:
            print("Invalid account details")

    def dbaccess(bsb, accnum, acctype, userid, passwd):
        return db_method.findAcc(bsb, accnum, acctype, userid, passwd)

if __name__ == '__main__':
    bsb = str(input("BSB: "))
    accnum = str(input("Account Number: "))
    acctype = str(input("Account Type: "))
    userid = str(input("User Id: "))
    passwd = str(input("Password: "))
    if access_acc.access(bsb, accnum, userid, passwd) == True: #and access_acc.dbaccess(bsb, accnum, acctype, userid, passwd):
        print("Access Granted")
        print(access_acc.getBalance(bsb, accnum))
        access_acc.deposit(bsb, accnum, int(input("Amount To Deposit: $")))
    else:
        print("Incorrect Details")
