from tkinter import*


def Login():
    def command1(event):
        if entry1.get() == 'admin' and entry2.get() == 'password' or entry1.get() == 'test' and entry2.get() =='pass':
            top.destroy()
        else:
            print('Wrong Password! , Try Again')
    def command2():
        top.destroy()
        sys.exit()

    #root = Tk()
    top = Tk()
    top.geometry('300x260')
    top.title('LOGIN SCREEN')
    photo2 = PhotoImage(file = 'LOGO.png')
    photo = Label(top, image = photo2, bg = 'white')
    lbl1 = Label(top, text ='Username : ',font = ('Helvtica',10))
    entry1 = Entry(top)
    lbl2 = Label(top, text = 'Password : ',font = ('Helvetica',10))
    entry2 = Entry(top,show = '*')
    #button1 = Button(top,text = 'Login', command = lambda:command1())
    button2 = Button(top,text = 'Cancel', command = lambda:command2())

    entry2.bind('<Return>', command1)
    #lbl3 = Label(top,text='Welcome Back!',font=('Arial',9))

    photo.pack()
    lbl1.pack()
    entry1.pack()
    lbl2.pack()
    entry2.pack()
    #button1.pack()
    button2.pack()
    #lbl3.pack()

    # root.title('Main Screen')
    # root.configure(background = 'white')
    # root.geometry('855x650')
    # root.withdraw()
    top.mainloop()