import timeit
timeit
from inspect import Parameter,Signature
import ast
import tkinter

def exec_then_eval(code):
    block = ast.parse(code, mode='exec')

    # assumes last node is an expression
    last = ast.Expression(block.body.pop().value)

    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode='exec'), _globals, _locals)
    return eval(compile(last, '<string>', mode='eval'), _globals, _locals)


class Descriptor:

    def __init__(self, name=None):
        self.name = name

    # Instance getting manipulated

    def __get__(self,instance,cls):
        print("Get",self.name)
        return instance.__dict__[self.name]

    def __set__(self,instance,value):
        print("Set",self.name,value)
        instance.__dict__[self.name] = value

    def __delete__(self,instance):
        print("Delete",self.name)
        del instance.__dict__[self.name]


class Typed(Descriptor):
    ty = object  # Expected type

    def __set__(self,instance,value):
        if not isinstance(value,self.ty):
            raise TypeError("Expected %s" % self.ty)
        super().__set__(instance,value)


class Contains(Descriptor):
    def __init__(self,*args,contains_char,**kwargs):
        self.contains_char = contains_char
        super().__init__(*args,**kwargs)

    def __set__(self,instance,value):
        if not self.contains_char in value:
            raise ValueError('String does not contain %s' % self.contains_char)
        super().__set__(instance,value)


class Sized(Descriptor):

    def __init__(self,*args,maxlen,**kwargs):
        self.maxlen = maxlen
        super().__init__(*args,**kwargs)

    def __set__(self,instance,value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance,value)


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


class StringContains(String,Contains):
    pass


class Positive(Descriptor):
    def __set__(self,instance,value):
        if(value < 0):
            raise ValueError('Must be >=0')
        super().__set__(instance,value)


class PostiveInteger(Integer,Positive): # ORDER OF PARAMS MATTER (e.g int before < 0 )
    pass


class PositiveFloat(Float,Positive):
    pass


class SizedString(String,Sized):
    pass


class SizedStringContains(SizedString,Contains):
    pass


def make_signature(names):
    return Signature(Parameter(name,Parameter.POSITIONAL_OR_KEYWORD) for name in names)


from collections import OrderedDict


class NicksMetastructure(type):
    @classmethod
    def __prepare__(cls,name,bases):
        return OrderedDict()

    def __new__(cls,clsname,bases,clsdict):
        #Collect Descriptors and set their names
        fields = [key for key, val in clsdict.items() if isinstance(val,Descriptor)]

        for name in fields:
            print(name)
            clsdict[name].name = name
        clsobj = super().__new__(cls,clsname,bases,dict(clsdict))

        sig = make_signature(fields)
        setattr(clsobj,'__signature__',sig)
        return clsobj


class NicksClass(metaclass=NicksMetastructure):

    _fields = ['name']

    def __init__(self,*args,**kwargs):
        bound = self.__signature__.bind(*args,**kwargs)

        for name, val in bound.arguments.items():
            setattr(self,name,val)


class SkelectonStruct(NicksClass):
    expression = String()


class Stock(NicksClass):

    data = SizedStringContains(maxlen=5,contains_char='Z') # maxlen and contains_char are interchangeable
    shares = PostiveInteger()
    price = PositiveFloat()


def old_main():
    s = Stock('FOOZ', 10, 1.00)  # Creates Stock object

    print(type(s.data))  # name is a string with a max length of 5, contains char then returns the string, else err

    #.name = 'I'  # returns value, which is a string, otherwise raise error on **first** failed condition
    #s.name = 'II'  # returns value, which is a string, otherwise raise error on **first** failed condition
    # s.name='NOOOOI' # returns ValueError: Too big (maxlen = 5, contains_char='I')
    # s.name='NOOO' # returns Value Error: String does not contain Z (maxlen = 5, contains_char='Z')

    print(PostiveInteger.__mro__)  # Checks PositiveInteger -> Integer -> Typed -> Positive -> Descriptor -> object

class print_string():
    string = "Test"
    print(string)
timeit.timeit(print_string())

def main():
    class_struct = SkelectonStruct('''
class print_string():
    string = "Test"
    print(string)
timeit.timeit(print_string())
''')
    exec_then_eval(SkelectonStruct.expression)


if __name__ == '__main__':
    main()

