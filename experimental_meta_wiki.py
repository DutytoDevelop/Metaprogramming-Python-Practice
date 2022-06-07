import ast
from inspect import Parameter, Signature
import inspect
from webbrowser import get


def exec_code(code):
    block = ast.parse(code, mode='exec')

    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode='exec'), _globals, _locals)
    return


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


def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


from collections import OrderedDict


class NicksMetaStructure(type):

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(mcs, clsname, bases, clsdict):
        #  Collect Descriptors and set their names
        fields = [key for key, val in clsdict.items() if isinstance(val, Descriptor)]

        for name in fields:
            print(name)
            clsdict[name].name = name

        clsobj = super().__new__(mcs, clsname, bases, dict(clsdict))

        sig = make_signature(fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj


class MetaClass(metaclass=NicksMetaStructure):
    _fields = ['name']

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)

        for name, val in bound.arguments.items():
            setattr(self, name, val)


class SkeletonStruct(MetaClass):
    expression = String()


class Stock(MetaClass):
    data = SizedStringContains(maxlen=5, contains_char='Z')  # maxlen and contains_char are interchangeable
    shares = PostiveInteger()
    price = PositiveFloat()


class futureClassStruct(MetaClass):
    """
    firstArg = firstArgType()

    unknown args will be in an array until further classification occurs?

    """


class print_string:
    string = "Test"
    print(string)


def main():
    class_struct = SkeletonStruct('''
class print_string():
    string = "Test"
    print(string)
''')
    exec(class_struct.expression)
    exec_code(class_struct.expression)
    # timeit.Timer(stmt=class_struct.expression)


if __name__ == '__main__':
    main()
