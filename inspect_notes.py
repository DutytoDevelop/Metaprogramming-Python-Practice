import importlib, sys, inspect, os
global num_classes
from gui.tkinter_treeview import make_treeview

num_classes = 1

class NicksMetastructure(type):

    def __new__(mcs, name, bases, clsdict):
        clsobj = super().__new__(mcs, name, bases, clsdict)
        #sig = make_signature(clsobj._fields)
        #setattr(clsobj, '__signature__', sig)
        return clsobj


    def __init__(cls, name, bases, clsdict):
        global num_classes
        num_classes += 1
        print("New class created:",cls.__name__,"from",super().__name__)


class MetaClass(metaclass=NicksMetastructure):
    _fields = []

    @classmethod
    def every_class_gets_this(cls):
        print("Every class can call this. Current class",cls.__name__)

    @classmethod
    def thisMethodIsAccessibletoSubclasses(cls):
        print("This class and subclass can call this. Only shows in MetaClass. Current class",cls.__name__)


class inheritMetaClass(MetaClass):


    def blank_function(self):
        test_var = [1,2,4]
        print("blank_function in inheritedMetaClass")


    def every_class_gets_this(cls):
        print("Override")


def get_class_objs_in_module(module):
    list_of_classes = inspect.getmembers(module, inspect.isclass)
    #print(list_of_classes)

    class_objs_only = []
    for classes in list_of_classes:
        class_obj = classes[1]
        #print(class_obj)
        class_objs_only.append(class_obj)
    return class_objs_only


def get_class_name_in_module(module):

    list_of_classes = inspect.getmembers(module, inspect.isclass)

    class_name_only = []
    for classes in list_of_classes:
        class_name = classes[1].__name__
        class_name_only.append(class_name)

    return class_name_only

def module_and_class(module_obj,class_name):
    class_name = module_obj.__class__
    module = class_name.__module__
    if module == 'builtins':
        return class_name.__qualname__ # avoid outputs like 'builtins.str'
    return module + '.' + class_name.__qualname__

def get_methods(class_name):
    class_method_dict = {}
    methodList = []
    print(class_name)
    for method_name in dir(class_name.__name__):
        try:
            print(getattr(class_name,method_name),method_name)
            #print(inspect.getsourcelines(getattr(class_name, method_name))[0])
            if callable(getattr(class_name, method_name)) and inspect.getsourcelines(getattr(class_name, method_name))[0]:
                if(method_name!='__class__'):
                    print(getattr(class_name,method_name))
                    methodList.append(method_name)
        except:
            None
            #methodList.append(str(method_name))
    class_method_dict.update({class_name:methodList})
    print(methodList)
    return methodList


def get_variables(module,class_name,class_method_var_list):
    #print("class_name:", class_name)
    var_list = []

    for variable in vars(class_name):
        if variable[0:2] != '__':
            if variable not in class_method_var_list:
                print(variable)
                var_list.append(variable)
    return var_list


def pretty(d, indent=0):
    if isinstance(d,dict):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict) or isinstance(value,list):
                pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))
    elif isinstance(d,list):
        for list_element in d:
            print('\t' * indent + str(list_element))
            if isinstance(list_element, dict) or isinstance(list_element, list):
                pretty(list_element, indent + 1)
            else:
                print('\t' * (indent + 1) + str(list_element))



def return_node_tree(module):
    all_classes = get_class_name_in_module(module)
    print(all_classes)
    all_class_objs = get_class_objs_in_module(module)
    print(all_class_objs)

    python_file_struct_list = {}
    methods_and_vars_list = []
    #print(python_module)
    #print(inspect.getmembers(get_variables))
    for class_name in all_class_objs:
        #  G
        print(class_name.__name__)
        method_list = get_methods(class_name)
        print("MethodList",method_list)
        class_methods_dict = {'Methods': method_list}

        #  G
        variables_list = get_variables(module,class_name, method_list)
        variables_list_dict = {'Variables': variables_list}

        try:
            print("Method vars too:",vars(method_list))
        except Exception as e:
            None

        #  G
        class_methods_dict_list = [class_methods_dict, variables_list_dict]
        methods_and_vars_list.append({class_name: class_methods_dict_list})
        print(methods_and_vars_list)
    print({module.__name__: methods_and_vars_list})
    python_file_struct_list.update({module.__name__: methods_and_vars_list})
    return python_file_struct_list

def get_source_code():
    inspect.getsource()

def module_from_filepath(filepath):
    spec = importlib.util.spec_from_file_location(os.path.basename(filepath), filepath)
    selected_module = spec.loader.load_module()
    return selected_module

if __name__ == '__main__':
    default_filepath = __file__
    module = module_from_filepath(default_filepath)
    print(module)
    print(module.__name__)
    python_file_struct_list = return_node_tree(module)
    gui_title = module.__name__
    print(python_file_struct_list)
    make_treeview(gui_title, python_file_struct_list.get(module.__name__))