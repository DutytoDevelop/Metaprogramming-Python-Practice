from functools import wraps


def nicks_type(type):

    def __new__(cls,clsname,bases,clsdict):
        clsobj = super().__new__(cls,clsname,bases,clsdict)
        return clsobj

    def __init__():
        return


def base(metaclass=nicks_type):
    return

if __name__ == '__main__':
    base()