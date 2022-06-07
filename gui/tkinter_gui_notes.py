# project.py
import tkinter as tk

root = tk.Tk()

display1 = tk.StringVar()
entry1 = tk.Entry(root,
                  relief=tk.FLAT,
                  textvariable=display1,
                  justify='right',
                  bg='orange')
entry1.pack()
entry1["font"] = "arial 30 bold"

display2 = tk.StringVar()
entry2 = tk.Entry(root,
                  relief=tk.FLAT,
                  textvariable=display2,
                  justify='right',
                  bg='orange')
entry2.pack()
entry2["font"] = "arial 30 bold"

display3 = tk.StringVar()
entry3 = tk.Entry(root,
                  relief=tk.FLAT,
                  textvariable=display3,
                  justify='right',
                  bg='orange')
entry3.pack()
entry3["font"] = "arial 30 bold"

display4 = tk.StringVar()
entry4 = tk.Entry(root,
                  relief=tk.FLAT,
                  textvariable=display4,
                  justify='right',
                  bg='orange')
entry4.pack()
entry4["font"] = "arial 30 bold"

display5 = tk.StringVar()
entry5 = tk.Entry(root,
                  relief=tk.FLAT,
                  textvariable=display5,
                  justify='right',
                  bg='orange')
entry5.pack()
entry5["font"] = "arial 30 bold"

b1 = tk.Button(root,
               # relief=tk.FLAT,
               compound=tk.LEFT,
               text="new",
               # command=None,
               # image=tk.PhotoImage("img.png")
               )
b1.pack()

root.mainloop()
