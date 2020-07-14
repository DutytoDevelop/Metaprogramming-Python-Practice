#Imports
from inspect import Parameter,Signature


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


class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class String(Typed):
    ty = str

class Contains(Descriptor):
    def __init__(self,*args,contains_char,**kwargs):
        self.contains_char = contains_char
        super().__init__(*args,**kwargs)

    def __set__(self,instance,value):
        if not self.contains_char in value:
            raise ValueError('String does not contain %s' % self.contains_char)
        super().__set__(instance,value)

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


class Sized(Descriptor):

    def __init__(self,*args,maxlen,**kwargs):
        self.maxlen = maxlen
        super().__init__(*args,**kwargs)

    def __set__(self,instance,value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance,value)

class SizedString(String,Sized):
    pass


class SizedStringContains(SizedString,Contains):
    pass

def make_signature(names):
    return Signature(Parameter(name,Parameter.POSITIONAL_OR_KEYWORD) for name in names)

class NicksMetastructure(type):

    def __new__(cls,name,bases,clsdict):
        clsobj = super().__new__(cls,name,bases,clsdict)

        sig = make_signature(clsobj._fields)
        setattr(clsobj,'__signature__',sig)
        return clsobj


class NicksClass(metaclass=NicksMetastructure):

    _fields = []

    def __init__(self,*args,**kwargs):
        bound = self.__signature__.bind(*args,**kwargs)

        for name, val in bound.arguments.items():
            setattr(self,name,val)


class Stock(NicksClass):
    _fields = ['name','shares','price']

    name = SizedStringContains('name',maxlen=5,contains_char='Z') # maxlen and contains_char are interchangeable
    shares = PostiveInteger('shares')
    price = PositiveFloat('price')


def main():
    s = Stock('FOOI', 10, 1.00)  # Creates Stock object

    print(type(s.name))  # name is a string with a max length of 5, contains char then returns the string, else err

    s.name = 'I'  # returns value, which is a string, otherwise raise error on **first** failed condition
    s.name = 'II'  # returns value, which is a string, otherwise raise error on **first** failed condition
    # s.name='NOOOOI' # returns ValueError: Too big (maxlen = 5, contains_char='I')
    # s.name='NOOO' # returns Value Error: String does not contain Z (maxlen = 5, contains_char='Z')

    print(PostiveInteger.__mro__)  # Checks PositiveInteger -> Integer -> Typed -> Positive -> Descriptor -> object


if __name__ == '__main__':
    main()

