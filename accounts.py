from uuid import uuid4
from generators import gens
from encryptlib import msgEnc, keyGen
from inilib import ini_config
from enum import Enum, unique
import os

if os.path.isfile('/encKey.txt'):
    print("File exists, skipping generation")
else:
    newKey = keyGen.newKey()
    with open('encKey.txt', 'w+') as f:
        f.write(str(newKey))
@unique
class accountType(Enum):
    savings = 0
    cheque = 1
    business = 2

    @classmethod
    def trykey(cls, keyVal):
        return keyVal in cls.__members__

class account:

    def __init__(self, acctype, bsb, accnum, userid, passwd):
        if accountType.trykey(acctype) == True:
            self.acctype = acctype
        else:
            self.acctype = 'savings'
        self.bsb = bsb
        self.accnum = accnum
        self.userid = userid
        self.passwd = msgEnc.encMsg(newKey, passwd).decode('utf-8')[:-2]
        self.balance = 0
        self.section = self.bsb + " " + self.accnum
        ini_config.writeValue(self.section, "inherits", "account")
        ini_config.writeValue(self.section, "acctype", self.acctype)
        ini_config.writeValue(self.section, "uid", self.userid)
        ini_config.writeValue(self.section, "pwd", self.passwd)
        ini_config.writeValue(self.section, "bal", str(self.balance))

    def getAcctype(self):
        return self.acctype

    def getbsb(self):
        return self.bsb

    def getaccnum(self):
        return self.accnum

    def getuserid(self):
        return self.userid

    def getpasswd(self):
        return self.passwd

    def change_passwd(self, oldpass, newpass=gens.id_gen(10)):
        if self.passwd == msgEnc.encMsg(newKey, oldpass).decode('utf-8')[:-2]:
            self.passwd = msgEnc.encMsg(newKey, newpass).decode('utf-8')[:-2]
            ini_config.writeValue(self.secion, 'pwd', str(self.passwd))
        else:
            print("Error: Passwords do not match")

    def getbal(self):
        return self.balance

    def addbal(self, count):
        self.balance += count
        ini_config.writeValue(self.section, "bal", str(self.balance))

    def rembal(self, count):
        self.balance -= count
        ini_config.writeValue(self.section, "bal", str(self.balance))

    def setbal(self, bal, password):
        if self.passwd == password:
            self.balance = bal
            ini_config.writeValue(self.section, "bal", str(self.balance))
        else:
            pass

class cheque(account):

    def __init__(self, userid, passwd=gens.id_gen(10)):
        account.__init__(self, 'cheque', gens.bsb_gen(), gens.accnum_gen(), userid, passwd=passwd)

class savings(account):

    def __init__(self, userid, passwd=gens.id_gen(10)):
        account.__init__(self, 'savings', gens.bsb_gen(), gens.accnum_gen(), userid, passwd=passwd)

class business(account):

    def __init__(self, userid, passwd=gens.id_gen(10)):
        account.__init__(self, 'business', gens.bsb_gen(), gens.accnum_gen(), userid, passwd=passwd)

chq = cheque('testuser1')
print(chq.getAcctype())
