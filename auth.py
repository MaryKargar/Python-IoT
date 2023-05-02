from tkinter import PhotoImage
from tkinter import *

# Authentication class
class Auth:
    def __init__(self, login_win,root) :
        # get root window and login window from main
        self.login_win = login_win
        self.root = root
    def gui(self):
            
        # Adjust size
        self.login_win.geometry("350x400")

        # Add image file
        self.bg = PhotoImage(file = "d.png")

        # Create Canvas for create image in background
        self.canvas1 = Canvas( self.login_win, width = 400,
                        height = 400)

        self.canvas1.pack(fill = "both", expand = True)

        # Display image
        self.canvas1.create_image( 0, 0, image = self.bg,
                            anchor = "nw")

        
        # crate box for username
        username_lbl = Label(self.canvas1, text="Username")
        username_entry = Entry(self.canvas1)

        # create box for password
        password_lbl = Label(self.canvas1, text="Password")
        password_entry = Entry(self.canvas1, show="*")

        # create login and cancel buttons
        login_btn = Button(self.canvas1, text="Login", width=8, command = lambda:self.checkAuth(username_entry.get(), password_entry.get()))        
        cancel_btn = Button(self.canvas1, text="Cancel", width=8) 


        # Display above widget in window
        username_lbl_canvas = self.canvas1.create_window( 80, 50,
                                            anchor = "nw",
                                            window = username_lbl)

        username_entry_canvas = self.canvas1.create_window( 160, 50,
                                            anchor = "nw",
                                            window = username_entry)

        password_lbl_canvas = self.canvas1.create_window( 80, 80,
                                            anchor = "nw",
                                            window = password_lbl)

        password_entry_canvas = self.canvas1.create_window( 160, 80,
                                            anchor = "nw",
                                            window = password_entry)
        

        login_btn_canvas = self.canvas1.create_window( 100, 260, anchor = "nw",
                                            window = login_btn)
        
        cancel_btn_canvas = self.canvas1.create_window( 180, 260, anchor = "nw",
                                            window = cancel_btn)
        
    # check user Authentication
    # get user and pass and check for login
    def checkAuth(self, user, password):
        # create label for show result
        result= StringVar()
        result_label= Label(self.canvas1,textvariable=result,width=15) 
        # display label in window
        result_canvas = self.canvas1.create_window( 110, 300, anchor = "nw",
                                            window = result_label)
        # user can enter, if username and password is admin admin
        if user == "admin" and password =="admin":
            result.set("Welcome to app")
            # hide root window and show login window
            self.login_win.destroy()
            self.root.deiconify()
        else:
            # if user or password is wrong, show a message in label
            result.set("Login failed")


          




