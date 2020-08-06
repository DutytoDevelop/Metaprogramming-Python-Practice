from inspect import Parameter, Signature, getfullargspec

'''
def exec_then_eval(code):
    block = ast.parse(code, mode='exec')

    # assumes last node is an expression
    last = ast.Expression(block.body.pop().value)

    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode='exec'), _globals, _locals)
    return eval(compile(last, '<string>', mode='eval'), _globals, _locals)
'''


def _make_init(fields):
    # Takes fields, make __init__ method
    code = 'def __init__(self,%s):\n' % \
           ','.join(fields)

    for name in fields:
        code += "   self.%s = %s\n" % (name, name)
    return code


def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


class Descriptor:

    def __init__(self, name=None):
        self.name = name

    # Instance getting manipulated

    def __get__(self, instance, cls):
        print("Get", self.name)
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        print("Set", self.name, value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print("Delete", self.name)
        del instance.__dict__[self.name]


class Typed(Descriptor):
    ty = object  # Expected type

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError("Expected %s" % self.ty)
        super().__set__(instance, value)


class Contains(Descriptor):
    def __init__(self, *args, contains_char, **kwargs):
        self.contains_char = contains_char
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.contains_char in value:
            raise ValueError('String does not contain %s' % self.contains_char)
        super().__set__(instance, value)


class Sized(Descriptor):

    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance, value)


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


class StringContains(String, Contains):
    pass


class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Must be >=0')
        super().__set__(instance, value)


class PostiveInteger(Integer, Positive):  # ORDER OF PARAMS MATTER (e.g int before < 0 )
    pass


class PositiveFloat(Float, Positive):
    pass


class SizedString(String, Sized):
    pass


class SizedStringContains(SizedString, Contains):
    pass


from collections import OrderedDict


class NoDupOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if key in self:
            raise NameError('%s already defined' % key)
        super().__setitem__(key, value)


class Metastructure(type):
    """
    OrderedDict() keeps things in order as they are provided... think FIFO when providing arguments to this function...

    Example:
        class Stock(NicksMetaStructure):
            name = SizedString(maxlen=4) <- We don't need to add in the field name because it is provided before '=' lol
            shares = PositiveInteger()
            price = PositiveFloat()

        OrderedDict() takes 'name', then 'shares', then 'price' and stores them within the dictionary

        Structure:
            clsdict = OrderedDict(
                ('name', <class 'SizedString'>),
                ('shares', <class 'PositiveInteger'>),
                ('price', <class 'PositiveFloat'>)
            )

    """

    @classmethod
    def __prepare__(cls, name, bases):

        """
        See 'Example Structure' above :)

        You could customize what you want to return, if you wanted to do duplicate variable detection then simply
        implement the function displayed in 1:33:22 in 'Python 3 Metaprogramming' YouTube video by David Beazley

        Link: https://www.youtube.com/watch?v=sPiWg5jSoZI&t=5608s

        THANK YOU DAVID BEAZLEY
        """

        return NoDupOrderedDict()

    def __new__(mcs, clsname, bases, clsdict):
        # Collect Descriptors and set their names

        """
        Analyzing __new__:

        Explanation:
            Everything returned in clsdict.items() is returned and added to fields array
            Pass clsdict array inside of clsobj during super().__new__(cls,clsname,bases,dict(clsdict)) to

        """
        fields = [key for key, val in clsdict.items() if isinstance(val, Descriptor)]

        # For each field, print name, added the field to the clsdict object, and then create the object associated
        for name in fields:
            print(name)
            clsdict[name].name = name

        if fields:
            init_code = _make_init(fields)
            exec(init_code, globals(), clsdict)

        clsobj = super().__new__(mcs, clsname, bases, dict(clsdict))

        return clsobj


class MetaClass(metaclass=Metastructure):
    _fields = ['name']

    """
    
    Since MetaClass is only inherited, __init__ does not get run
    
    def __init__(self):
        super().__init__()
        print(self.__name__)
            
    """

    def __init_subclass__(cls, all_subclasses=[], **kwargs):
        print("We're inside the MetaClass, printing inheriting subclass names when subclass is :", cls.__name__)
        print("Printing each argument inside of", cls.__name__, "below:")

        cls.all_subclasses = all_subclasses
        cls.all_subclasses.append(cls.__name__)

        for obj in getfullargspec(cls)[0]:
            print("OBJECT", obj, "CONTAINS", cls.__dict__.values())


class SkeletonStruct(MetaClass):
    expression = String()


class Stock(MetaClass):
    """

    Because of the __prepare__ classmethod inside of our metastructure (what gets ran upon every class instance),
    we are able to take the name of the variable and store it within clsdict before passing it to our Descriptors
    to

    """

    data = SizedStringContains(maxlen=5, contains_char='Z')  # maxlen and contains_char are interchangeable
    shares = PostiveInteger()
    price = PositiveFloat()
    test_var = Integer()

    @staticmethod
    def func_test(*args, **kwargs):
        print("args:", args, "kwargs:", kwargs)
        return


class futureClassStruct(MetaClass):
    """
    firstArg = firstArgType()

    unknown args will be in an array until further classification occurs?

    """


def old_main():
    s = Stock('FOOZ', 10, 1.00, 52)  # Creates Stock object

    print("Type of s.data:",
          type(s.data))  # name is a string with a max length of 5, contains char then returns the string, else err

    # .name = 'I'  # returns value, which is a string, otherwise raise error on **first** failed condition
    # s.name = 'II'  # returns value, which is a string, otherwise raise error on **first** failed condition
    # s.name='NOOOOI' # returns ValueError: Too big (maxlen = 5, contains_char='I')
    # s.name='NOOO' # returns Value Error: String does not contain Z (maxlen = 5, contains_char='Z')

    print(PostiveInteger.__mro__)  # Checks PositiveInteger -> Integer -> Typed -> Positive -> Descriptor -> object
    print(s.test_var)


class PrintString:
    string = "Test"
    print(string)


def main():
    expression = '''
class print_string():
    string = "Successfully executed string code!! Keep it up buddy."
    print(string)
'''

    class_struct = SkeletonStruct(expression)

    exec(class_struct.expression)
    s = Stock('FOOZ', 10, 1.00, 52)  # Creates Stock object
    print(s.data)
    s.func_test("Non-kwarg1", 2, 5, test=5)
    print(s.__dict__)


if __name__ == '__main__':
    main()
