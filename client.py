'''
from tkinter import *


def login():
    login = textLogin.get()
    passw = textPassword.get()
    #print(f'Login: {login}, Password: {passw}')
    if True:
        print("go")
        print(f"Login: {login}, Password: {passw}")
        #page.destroy()
        #import main
    else:
        print("go back")

page = Tk()
page.geometry("470x260")
page.title("GrepoSyf Client")
page.resizable(False, False)

label1 = Label(page, text="GrepoSyf").pack()
label2 = Label(page, text="by Menemeth11").pack()

textLogin = StringVar()
labelLogin = Label(page, text="Login:").pack()
inputLogin = Entry(page, textvariable=textLogin).pack()

textPassword = StringVar()
labelPassword = Label(page, text="Password:").pack()
inputPassword = Entry(page, textvariable=textPassword, show="*").pack()

buttonLogin = Button(page, text="Login", command=login).pack()

page.mainloop()'''