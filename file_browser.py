#!/usr/bin/env python

"""
"""
#Imports
from tabulate import tabulate
from tkinter import filedialog
from tkinter import *
import ftplib

#Global Variables
entry1=None
entry2=None
libox_serverdir=None
ftp=None

def button_upload_callback():
    """ 
    what to do when the "Go" button is pressed 
    """
    global entry1
    input_file = entry1.get()
    print("Uploading files: ",input_file)
    
def button_download_callback():
    """ 
    what to do when the "Go" button is pressed 
    """
    global entry2
    global libox_serverdir
    
    input_file = entry2.get()
    print("Downloading files: ",input_file)
    selected_text_list = [libox_serverdir.get(i) for i in libox_serverdir.curselection()]
    print("Downloading files: ",selected_text_list)
    
def button_browselocal_callback():
    """ 
    What to do when the Browse button is pressed 
    """
    global entry1
    filename = filedialog.askopenfilenames(initialdir=r"C:\temp\clientlocation")
    entry1.delete(0, END)
    entry1.insert(0, filename)
    entry1.config(fg='black')
    
def button_browseserver_callback():
    """ 
    What to do when the Browse button is pressed 
    """
    global entry2
    #filename = filedialog.askopenfilenames(initialdir=r"ftp://127.0.0.1:1501/")
    filename = filedialog.askopenfilenames(initialdir=r"C:\temp\serverlocation")
    entry2.delete(0, END)
    entry2.insert(0, filename)
    entry2.config(fg='black')
    
def button_list_callback():
    print("Insert method to list files from server")
    
    
def displayDir():
    global libox_serverdir
    global ftp
    libox_serverdir.delete('0', 'end')
    #libox_serverdir.insert(0,"--------------------------------------------")
    dirlist = []
    dirlist = ftp.nlst()
    for item in dirlist:
        libox_serverdir.insert(0, item)
        
def gui():
    """make the GUI version of this command that is run if no options are
    provided on the command line
    """
    global entry1
    global entry2
    global libox_serverdir
    global ftp
    
    root = Tk()
    root.title("Home")
    frame = Frame(root)
    frame.pack()
    
    ftp = ftplib.FTP()
    msg = ftp.connect("127.0.0.1",1501)
    msg = ftp.login("user","12345")

    statusText = StringVar(root)
    statusText.set("Press Browse button or enter filename with path, "
                   "then press the Go button")
    
    label1 = Label(root, text="Select File for FTP Upload: ",justify=LEFT)
    entry1 = Entry(root, width=50)
    entry1.insert(0,"Enter or Browse Upload File Path")
    entry1.config(fg='grey')
    label2 = Label(root, text="Select File for FTP Download: ",justify=LEFT)
    entry2 = Entry(root, width=50)
    entry2.insert(0,"Enter or Browse Download File Path")
    entry2.config(fg='grey')
    separator1 = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator2 = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator3 = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator4 = Frame(root, height=2, bd=1, relief=SUNKEN)
    libox_serverdir = Listbox(width=40,height=14,selectmode=MULTIPLE)
    
    button_browselocal = Button(root,
                           text="Browse Local",
                           width=25,
                           command=button_browselocal_callback)
    button_upload = Button(root,
                       text="Upload",
                       width=25,
                       command=button_upload_callback)
    button_browseserver = Button(root,
                           text="Browse Server",
                           width=25,
                           command=button_browseserver_callback)
    button_download = Button(root,
                       text="Download",
                       width=25,
                       command=button_download_callback)
    button_exit = Button(root,
                         text="Exit",
                         width=25,
                         command=sys.exit)
    button_list = Button(root,
                         text="List Server Files and Directories",
                         width=25,
                         command=displayDir)
                         
    
    label1.pack()
    entry1.pack(padx=5)
    button_browselocal.pack(padx=5)
    button_upload.pack(padx=5)
    separator2.pack(fill=X, padx=5, pady=5)
    label2.pack()
    libox_serverdir.pack()
    entry2.pack(padx=5)
    button_browseserver.pack(padx=5)
    button_download.pack(padx=5)
    separator3.pack(side=TOP,fill=X,padx=5,pady=5)
    button_list.pack(padx=5)
    separator4.pack(side=TOP,fill=X,padx=5,pady=5)
    button_exit.pack(padx=5, pady=(0,5))
    
if __name__ == "__main__":
    """ Run as a stand-alone script """
    gui()