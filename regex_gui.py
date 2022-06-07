import builtins
import os
import sys
import platform
from tkinter import BOTH, TOP, Canvas, Label, LabelFrame, Menu,Tk, Toplevel,ttk,messagebox,Grid,Text
from threading import Thread
from PIL import Image, ImageTk
import PIL.Image
from win32api import GetSystemMetrics  # Program dimension and placement


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# GUI globals
global curdir
curdir = os.getcwd()

global project_dir
project_dir = os.path.dirname(os.path.abspath(__file__))

global current_user
current_user = os.environ['USERPROFILE'] # "C:\Users\[username]"

global detected_os
detected_os = platform.system()

"""
from pynput.keyboard import Key, Listener

def on_press(key):
    print('{0} pressed'.format(
        key))


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False
    if key == Key.f7:
        return False

def on_press_highlight(key):
    None

def on_release_highlight(key):
    global index
    global colour_changer

    colour_changer+= 50
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False
    elif key == Key.ctrl_l:
        x, y = win32api.GetCursorPos()
    elif key == Key.ctrl_r:
        None
        '''
            elif key == Key.page_down:
                builtins.labtech_window = builtins.labtech_window.descendants(depth=1)[index]
                index = 0
                builtins.labtech_window.draw_outline(colour=colour_changer, thickness=2)
                return
            elif key == Key.up:
                index = (index-1)%len(builtins.labtech_window.descendants(depth=1))
                builtins.labtech_window.descendants(depth=1)[index].draw_outline(colour=colour_changer, thickness=2)
                return
            elif key == Key.down:
                index = (index + 1) % len(builtins.labtech_window.descendants(depth=1))
                builtins.labtech_window.descendants(depth=1)[index].draw_outline(colour=colour_changer, thickness=2)
                return'''

        return

def key_listener():
    # Collect events until released
    with Listener(on_press=on_press_highlight, on_release=on_release_highlight) as listener:
        listener.join()

"""
def thread_function(function, *args): # thread_function(key_listener)
    if(isinstance(function, str)):
        make_new_thread = Thread(target=eval(function))
    else:
        make_new_thread = Thread(target=function, args=(args))
    make_new_thread.start()


class regex_gui():

    def __init__(self,*args):

        # Root Window
        self.root = Tk()
        self.root.withdraw()
        self.root.title("Regex Helper")

        # Window size
        self.app_width = 420
        self.app_height = 490

        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

        self.menubar = Menu(self.root)
        self.optionmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Options", menu=self.optionmenu)
        self.optionmenu.add_command(label="About...", command=self.about_popup)
        self.optionmenu.add_command(label="Help", command=None)
        self.optionmenu.add_separator()
        self.optionmenu.add_command(label="Exit", command=self.exit_compiler)

        self.root.config(menu=self.menubar)

        # Notebook
        self.note = ttk.Notebook(self.root)

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        # Tab 1
        self.tab1 = ttk.Frame(self.note)
        self.note.add(self.tab1, text = "Configuration", compound=TOP)

        self.labelframe = LabelFrame(self.tab1, text="Ticket Information:")
        self.labelframe.pack(fill="both", expand="yes",padx=5,pady=2)
        self.quick_functions_frame = LabelFrame(self.labelframe, text='Quick Functions:')
        self.quick_functions_frame.grid(row=1, column=4, rowspan=8, columnspan=2,sticky="n")

        Label(self.labelframe, text='Label1:').grid(row=1, column=1, sticky="e")

        # Tab 2
        self.tab2 = ttk.Frame(self.note)
        self.note.add(self.tab2, text = "Search", compound=TOP)


        # Pack notebook widget (expanded to fill entire root window)
        self.note.pack(fill=BOTH, expand="yes",padx=2,pady=2)

        # Main window settings
        self.root.geometry(str(self.app_width)+"x"+str(self.app_height)+"+"+str(int((self.screen_width/2)-(self.app_width/2)))+"+"+str(int((self.screen_height/2)-(self.app_height/2))))
        self.root.resizable(False, False)  # Not resizable
        self.root.deiconify()
        self.root.iconbitmap(project_dir + r'\ico\favicon.ico')


    def get_radiobutton_value(self, element):
        self.element = element
        radiobtn_val = self.element.get()
        return radiobtn_val

    # Return text inside of Tkinter Entry widget
    def get_entrybox_text(self, element):
        self.element = element
        element.configure(state="normal")
        entrybox_text = os.path.join(self.element.get())
        element.configure(state="disabled")
        return entrybox_text

    # Set text inside of Tkinter Entry widget
    def set_entrybox_text(self, element: Text, text: str, append_text: bool = False):
        self.element = element
        self.text = text
        if (append_text is True):
            if (detected_os == 'windows'):
                seperator = ';'
            else:
                seperator = ':'
            if (self.get_entrybox_text(self.element) != ''):
                self.text = self.text
            else:
                self.text = seperator.join(self.get_entrybox_text(self.element), self.text)
            self.element.insert('end', self.text)
        else:
            self.element.delete(0, 'end')
            self.element.insert(0, self.text)
        return

    
    # Display GUI
    def show(self):
        self.root.mainloop()

    # Exit GUI
    def exit_compiler(self):
        self.root.destroy()
        exit()

    # Popup that gets created when you click the 'About' menu option
    def about_popup(self):
        top = Toplevel()
        top.title("About Me")
        top.geometry = "500x400"
        top.resizable(False,False)

        ico_directory = resource_path("ico")
        pyxe_favicon = os.path.join(ico_directory, "favicon.ico")
        top.iconbitmap(pyxe_favicon)

        about_labelframe = LabelFrame(top,labelanchor="nw",text="Developer Profile:",width=600,height=200,font=('',10))
        about_labelframe.pack(fill="both",expand=True,padx=3,pady=3)

        profile_photo = Image.open(resource_path(r"resources\data\Developer_Profile_Photo.jpg"))
        resized = profile_photo.resize((150,150))
        profile_photo_resize = ImageTk.PhotoImage(resized)

        canvas = Canvas(about_labelframe,height=150,width=150)
        canvas.create_image(75,75,image=profile_photo_resize)
        canvas.image = profile_photo_resize
        canvas.grid(row=1,column=1,padx=3,pady=(3,0),sticky="nsew")

        about_label = Label(about_labelframe,text="Name: Nicholas H.\nGitHub: DutytoDevelop",font=('',10,'bold'))
        about_label.configure(anchor="center", justify='center')
        about_label.grid(row=2,column=1,padx=3,pady=(0,3),sticky="nsew")
        return


if __name__ == '__main__':
    gui = regex_gui()
    thread_function(function=gui.show())