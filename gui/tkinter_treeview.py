import os
from inspecting_classes_and_modules.inspect_notes import module_and_class,module_from_filepath, return_node_tree
import inspect
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo

example = [{"Administration": ["John Doe", "John Doe"]},
           {"Logistics": {"Sub-Log": ["Data1", {"Sub-Log": ["Data1", "Data2"]}]}},
           {"L4": {"Another_Dict": ["Data1", {"Sub-Log": ["Data1", "Data2"]}]}},
           {"L5": "Test"}]


def remove_treeview(treeview_widget):
    treeview_widget.delete(*treeview_widget.get_children())
    return


#  Return filepath
def get_filepath_of_file(title, initialdir, filetypes):
    selected_file = ""

    #  If file doesn't exist, continue prompting file selection
    selected_file = tk.filedialog.askopenfilename(title=title,
                                               initialdir=initialdir,
                                               filetypes=filetypes)
    #  Return filepath
    return selected_file


def get_object_from_method_and_classname(class_name,method):
    return getattr(class_name,method)


#  Return text inside of Tkinter Entry widget
def get_text_widget_text(element):
    text = ""
    text = element.get()
    return text


#  Set text inside of Tkinter Entry widget
def set_text_widget_text(element, text):
    element.configure(state="normal")
    element.delete(1.0, tk.END)
    element.insert(1.0, text)
    element.configure(state="disabled")
    return

#  Return text inside of Tkinter Entry widget
def get_entrybox_text(element):
    text = ""
    text = element.get()
    return text


#  Set text inside of Tkinter Entry widget
def set_entrybox_text(element, text):
    element.configure(state="normal")
    element.delete(0, tk.END)
    element.insert(0, text)
    element.configure(state="readonly")
    return

def add_nodes(treeview_widget, node_count=0, data_nodes=None, **kwargs):
    sub_array = []
    if 'node_array' not in kwargs:
        for index, node in enumerate(data_nodes):
            parent_node = index
            for key, value in node.items():
                print(parent_node,node_count,key.__name__)
                try:
                    if(inspect.isclass(type(key))):
                        obj_type = 'class'
                except:
                    obj_type = ''
                treeview_widget.insert('', tk.END,text=key.__name__,value=obj_type, iid=node_count, open=False,tags=('cb'))
                sub_array.append({node_count: value})
                node_count += 1
        add_nodes(treeview_widget, node_count, data_nodes, node_array=sub_array)
    else:
        sub_array = kwargs['node_array']
        # print("node_array", node_array)
        while (len(sub_array) > 0):
            temp_arr = []
            for index in range(0, len(sub_array)):
                print("TTTTTT",sub_array)
                for key, value in sub_array[index].items():
                    print("TTT",key,value)
                    try:
                        print(">key", key, type(key))
                        print(">value", value, type(value))
                        if (inspect.isclass((value))):
                            obj_type = 'class'
                        elif (inspect.ismethod((value))):
                            obj_type = 'method'
                        elif (inspect.isfunction((value))):
                            obj_type = 'function'
                        else:
                            obj_type = 'var'
                    except:
                        obj_type = ''
                    if isinstance(value, dict):
                        for k, v in value.items():
                            print("HEEYY",k,v,type(v))
                            # print(k,v)
                            treeview_widget.insert('', tk.END, text=k,value=obj_type , iid=node_count, open=False,tags=('cb'))
                            treeview_widget.move(node_count, index, 0)
                            temp_arr.append({node_count: v})
                            node_count += 1
                    elif isinstance(value, list):
                        for ind, vals in enumerate(value):
                            print(vals)

                            if isinstance(vals, dict):
                                for keys in vals.keys():
                                    if(not isinstance(keys,str)):
                                        try:
                                            print("KEY", keys,type(keys))
                                            if (inspect.isfunction(keys)):
                                                obj_type = 'class'
                                            elif (inspect.isfunction(keys)):
                                                obj_type = 'method'
                                            elif (inspect.isfunction(keys)):
                                                obj_type = 'function'
                                            else:
                                                obj_type = 'var'
                                        except:
                                            obj_type = ''
                                    else:
                                        obj_type = ''
                                    temp_arr.append({node_count: vals.get(keys)})
                                    print("GADGAG",keys,vals)
                                    treeview_widget.insert('', tk.END, text=keys,value=obj_type , iid=node_count, open=False,tags=('cb'))
                            elif isinstance(vals, list):
                                print("BREAK",(key,vals))
                                print(getattr(key,vals))
                                treeview_widget.insert('', tk.END, text=key.__name__, value=obj_type ,iid=node_count, open=False,tags=('cb'))
                            else:
                                print(value,vals,"AHHHHHHHHHHHHHHHHH")
                                treeview_widget.insert('', tk.END, text=vals, value=obj_type ,iid=node_count, open=False,tags=('cb'))
                            treeview_widget.move(node_count, key, ind)
                            node_count += 1
                    elif isinstance(value, str):
                        try:
                            print("KEY2", value, type(value))
                            if (inspect.isfunction(keys)):
                                obj_type = 'class'
                            elif (inspect.isfunction(keys)):
                                obj_type = 'method'
                            elif (inspect.isfunction(keys)):
                                obj_type = 'function'
                            else:
                                obj_type = 'var'
                        except:
                            obj_type = ''
                        print(node_count,key)
                        treeview_widget.insert('', tk.END, text=key,value=obj_type , iid=node_count, open=False,tags=('cb'))
                        treeview_widget.move(node_count, key, 0)
                        node_count += 1
            sub_array = temp_arr
    return


def make_treeview(tkinter_gui_title, node_array):
    # create root window
    root = tk.Tk()
    root.title('Treeview - Python Module Visualizer')
    root.geometry('1200x500')

    # configure the grid layout
    root.rowconfigure(2, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(0, weight=0)
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=2)
    root.columnconfigure(2, weight=0)
    root.columnconfigure(3, weight=0)


    # create a treeview
    tree = ttk.Treeview(root, selectmode="browse")
    tree['columns'] = ['Type',f"{tkinter_gui_title.upper()[0]}{tkinter_gui_title[1:]} object name",'tre']
    column_width_list = [180,199,199]

    tree.column(column='#0', anchor='w', width=160,stretch='NO')
    tree.heading(column='#0', anchor='w')
    for index,column in enumerate(tree['columns']):
        tree.column(column=index, anchor='w',width=column_width_list[index],stretch='NO')
        tree.heading(column=index, text=tree['columns'][index], anchor='w')


    node_count=0
    add_nodes(tree,node_count,node_array)

    #  These widgets make up the function allowing you to select a Python file to compile
    ttk.Label(root, text='Select Python File:').grid(row=0, column=0, sticky="W",padx=(5, 0))

    filepath_string = tk.StringVar()

    program_filepath_textbox = tk.Entry(root, textvariable=filepath_string)
    program_filepath_textbox.configure(state='readonly')
    program_filepath_textbox.grid(row=0, column=1,columnspan=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

    file_selection_button = tk.Button(root, text='Select Python File', command=lambda: load_py_file_intro_treeview(
        title="Select Python File",
        initialdir=os.getcwd(),
        filetypes=[("Python File", "*.py")],
        element=program_filepath_textbox))
    file_selection_button.configure()
    file_selection_button.grid(row=0, column=3, padx=5, pady=5, sticky="EW")

    #  Grab filepath of Python file
    def load_py_file_intro_treeview(title, initialdir, filetypes, element):
        filepath = get_filepath_of_file(title, initialdir, filetypes)
        element.configure(state="normal")
        set_entrybox_text(element, filepath)
        element.configure(state="readonly")
        remove_treeview(tree)
        node_count = 0
        print(filepath)
        module = module_from_filepath(filepath)
        print(module,module.__name__)
        tree.heading('#0', text=f"{module.__name__} module treeview", anchor='w')
        node_array = return_node_tree(module)
        print(node_array)
        add_nodes(tree,node_count,node_array.get(module.__name__))
        return

    # Constructing vertical scrollbar
    # with treeview
    verscrlbar = ttk.Scrollbar(root,
                               orient="vertical",
                               command=tree.yview)

    # Calling pack method w.r.to verical
    # scrollbar
    verscrlbar.grid(row=1, column=2,rowspan=2, sticky='nse',padx=(10,0),pady=(0,5))

    # Configuring treeview
    tree.configure(yscrollcommand=verscrlbar.set)

    # place the Treeview widget on the root window
    tree.grid(row=1, column=0, rowspan=2,columnspan=3,padx=(10,0),pady=(0,5), sticky='nsew')

    def cb(event):
        print(tree.selection(),tree.item(tree.selection(),"text"),tree.item(tree.selection(),"values"),type(tree.item(tree.selection(),"values")))
        module = module_from_filepath(get_entrybox_text(program_filepath_textbox))
        obj_name = tree.item(tree.selection(),"text")
        obj_data = tree.item(tree.selection(),"values")
        treeview_widget_id = tree.selection()[0]
        parent = tree.parent(tree.selection())
        print(obj_name,obj_data,)
        try:
            print(inspect.getsource(getattr(module,obj_name)))
        except:
            None

        try:
            method_source_code = inspect.getsource(get_object_from_method_and_classname(class_name=getattr(module,"Application"),method=obj_name))
        except:
            None

        set_text_widget_text(codebox_entry,method_source_code)


    tree.tag_bind('cb', '<1>', cb)
    tree.tag_bind('cb', '<<TreeviewSelect>>', cb)

    codebox_entry = tk.Text(root,width=40)
    codebox_entry.configure(state='disabled')
    codebox_entry.grid(row=1, column=3, rowspan=2, sticky='NSEW', padx=(5, 5), pady=(5,5))

    # run the app
    root.mainloop()


if __name__ == '__main__':
    make_treeview("N",[])