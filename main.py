import meta

class Structure:

    _fields = []

    def __init__(self, *args):
        for name, val in zip(self._fields,args):
            setattr(self,name,val)



class example_base_class(Structure):
    _fields = ['name','shares','price']


def main():

    example_object = example_base_class('data',44,2.2)
    for field_value in example_object._fields:
        print(field_value)




    return


if __name__ == '__main__':
    main()