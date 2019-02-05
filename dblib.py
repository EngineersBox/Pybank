import pymongo

atmClient = pymongo.MongoClient("mongodb://localhost/")
atmdb = atmClient["atmdb"]
accCol = atmdb["accounts"]

"""
BSB (bsb)
Account Number (accnum)
Account type (acctype)
User id (uid)
Password (pwd)
Balance (bal)
"""

class db_method:

    def findAcc(bsb, accnum, acctype, userid, passwd):
        query = { "bsb": str(bsb), "accnum": str(accnum), "acctype": str(acctype), "uid": str(userid), "pwd": str(passwd) }
        if accCol.find(query).count() == 0:
            return False
        else:
            return True

    def addAcc(bsb, accnum, acctype, userid, passwd, balance=0):
        if db_method.findAcc(bsb, accnum, acctype, userid) == False:
            dataDict = { "bsb": str(bsb), "accnum": str(accnum), "acctype": str(acctype), "uid": str(userid), "pwd": str(passwd), "balance": str(balance) }
            x = accCol.insert_one(dataDict)
            print("Shop Instance Created")
        else:
            print("Shop Instance Already Exists")

    def delAcc(bsb, accnum, acctype, userid, passwd):
        query = { "bsb": str(bsb), "accnum": str(accnum), "acctype": str(acctype), "uid": str(userid), "pwd": str(passwd) }
        if db_method.findAcc(bsb, accnum, acctype, userid) == True:
            accCol.delete_one(query)
            print("Shop Instance Deleted")
        else:
            print("Shop Instance Does Not Exist")
