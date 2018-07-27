from tkinter import *
import tkinter.messagebox as tm
import file_browser

username=None
password=None

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")
        
        self.label_username.grid(row=0, sticky=E,padx=5)
        self.label_password.grid(row=1, sticky=E,padx=5)
        self.entry_username.grid(row=0, column=1,padx=5)
        self.entry_password.grid(row=1, column=1,padx=5)
        
        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2,padx=5,pady=5)
    
        self.pack()
    
    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == "test" and password == "test":
            self.master.destroy()
            file_browser.gui()
        else:
            tm.showerror("Login error", "Incorrect username")

root = Tk()
root.title("Login")
lf = LoginFrame(root)
root.mainloop()