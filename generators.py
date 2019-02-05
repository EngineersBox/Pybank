import string
import random

class gens:

    def id_gen(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def bsb_gen(chars=string.digits):
        ret_val = ''
        for i in range(7):
            if i == 3:
                ret_val += '-'
            else:
                ret_val += random.choice(chars)
        return ret_val

    def accnum_gen(chars=string.digits):
        ret_val = ''
        for i in range(9):
            if i == 4:
                ret_val += ' '
            else:
                ret_val += random.choice(chars)
        return ret_val
