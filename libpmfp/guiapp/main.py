
from tkinter import *
from tkinter.ttk import *
from app import Application

def main():
    app = Application()
    app.master.title('Hello World')
    app.master.geometry("600x400+100+400")
    app.mainloop()

if __name__ =="__main__":
    main()
