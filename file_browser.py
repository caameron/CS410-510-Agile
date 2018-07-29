#!/usr/bin/env python

"""
"""
##Imports
#from tabulate import tabulate
#from tkinter import filedialog
#from tkinter import *
#import ftplib
import socket
#
##Global Variables
#entry1=None
#entry2=None
#libox_serverdir=None
#ftp=None
#
#def button_upload_callback():
#    """ 
#    what to do when the "Go" button is pressed 
#    """
#    ###############################################
#    #ADD METHOD TO UPLOAD FILES HERE
#    ###############################################
#    global entry1
#    input_file = entry1.get()
#    print("Uploading files: ",input_file)
#    upload_files = input_file.split(" ")
#    
#def button_download_callback():
#    """ 
#    what to do when the "Download" button is pressed 
#    """
#    ###############################################
#    #ADD METHOD TO DOWNLOAD FILES HERE
#    ###############################################
#    global entry2
#    global libox_serverdir
#    
#    input_file = entry2.get()
#    print("Downloading files: ",input_file)
#    selected_text_list = [libox_serverdir.get(i) for i in libox_serverdir.curselection()]
#    print("Downloading files: ",selected_text_list)
#    
#def button_browselocal_callback():
#    """ 
#    What to do when the Browse button is pressed 
#    """
#    global entry1
#    filename = filedialog.askopenfilenames(initialdir=r"C:\temp\clientlocation")
#    entry1.delete(0, END)
#    entry1.insert(0, filename)
#    entry1.config(fg='black')
#    
#def upload():
#    host = '127.0.0.1'      #host ip
#    port = 8888             #port number
#
#    s = socket.socket()     #get client socket s
#    s.connect((host,port))
#    if os.path.isfile(completename):
#        s.send(filename)
#        feedback = s.recv(1024)
#        if feedback == 'OKSEND':
#            filesize = str(os.path.getsize(completename))
#            s.send(filesize)
#            response = raw_input("File to PUT is " + str(filesize) + " Bytes, Proceed? (Y/N) ")            
#            if response == 'Y':
#                #open the file found in client and get ready to send the data over to the server
#                with open(completename, 'rb') as f:
#                    sendbyte = f.read(1024)    #this will read and return bytes from file
#                    s.send(sendbyte) #send the bytes to server
#                    currentsent = len(sendbyte)
#                    #print "{0:.2f}".format((currentsent/float(filesize))*100)+ "% Done"
#                    #continue to send bytes to server untill all bytes of file is sent.
#                    while sendbyte != "":
#                        sendbyte = f.read(1024)
#                        s.send(sendbyte)
#                        currentsent += len(sendbyte)
#
#                        #like in SET, below will simulate a progress bar.
#                        os.system('clear')
#                        progress = '['
#                        for x in range (0, int(currentsent/float(filesize) * 100)):
#                                                    progress += '#'
#                        #print current progress
#                        #print("{0:.2f}".format((currentsent/float(filesize))*100)+ "% " + progress + "]")
#                print("PUT successful")
#            else:
#                s.send("!!!")    #this will alert server that we aren't proceeding with PUT
#
#        #This branch taken if file not found in client.
#    else:
#        s.send("!!!")    #this will alert the server that we aren't proceeding with PUT
#        print("File not found in client")
#    
#def button_browseserver_callback():
#    """ 
#    What to do when the Browse button is pressed 
#    """
#    global entry2
#    #filename = filedialog.askopenfilenames(initialdir=r"ftp://127.0.0.1:1501/")
#    filename = filedialog.askopenfilenames(initialdir=r"C:\temp\serverlocation")
#    entry2.delete(0, END)
#    entry2.insert(0, filename)
#    entry2.config(fg='black')
#    
#def button_list_callback():
#    ###############################################
#    #ADD METHOD TO LIST FILES FROM SERVER HERE
#    ###############################################
#    print("Insert method to list files from server")
#    global libox_serverdir
#    global ftp
#    libox_serverdir.delete('0', 'end')
#    #libox_serverdir.insert(0,"--------------------------------------------")
#    dirlist = []
#    dirlist = ftp.nlst()
#    for item in dirlist:
#        libox_serverdir.insert(0, item)
#    libox_serverdir.insert(0, "..")
#    libox_serverdir.bind("<Double-Button-1>",listbox_double_click)
#    
#def listbox_double_click(event):
#    curr_selection = libox_serverdir.curselection()
#    print("Listbox double click selection: ",libox_serverdir.get(curr_selection[0]))
#    ############################################################################
#    #libox_serverdir.get(curr_selection[0]) returns the selection string
#    #Insert method here to use that string to change directories. Add try/except
#    #to account for double click on files instead of directories
#    #Before double clicking, need to clear all current selections
#    ############################################################################
#        
def gui():
    """make the GUI version of this command that is run if no options are
    provided on the command line
    """
    global entry1
    global entry2
    global libox_serverdir
    global ftp
    
#    root = Tk()
#    root.title("Home")
#    frame = Frame(root)
#    frame.pack()
    
    #ftp = ftplib.FTP()
    #msg = ftp.connect("127.0.0.1",8888)
    #msg = ftp.login("user","12345")
    
    ###############################################################################
    ###############################################################################
    host = '127.0.0.1'    #host ip
    port = 8888        #port number

    s = socket.socket()    #get client socket s
    s.connect((host,port))    #attempt to connect to server using host and port.
    
    username = "test1"
    password = "test2"
    
    s.send(username)    #send username that was received from command line to server to check if username exists
    member = s.recv(1024)    
    #send password next to server to validate.
    print("sending password")
    if member == 'NEW':
        s.send(password)
    if member == 'EXIST':
        s.send(password)
    
    login = s.recv(1024)
    #if received login info from server is FAIL then alert that its incorrect user/pass combo and disconnect client.
    if login == "FAIL":
        print("Incorrect username and password combination, reconnect with: python client.py username password")
        s.close()
        sys.exit()
    #if login info from server is PASS and member is EXIST then this means already existing user relogging
    if login == "PASS" and member == "EXIST":
        print("Welcome back " + username)
    #if login info is just PASS then new user is registered
    elif login == "PASS":
        print("Thanks for registering on the FTP client " + username)
    ###############################################################################
    ###############################################################################
    
#    statusText = StringVar(root)
#    statusText.set("Press Browse button or enter filename with path, "
#                   "then press the Go button")
#    
#    label1 = Label(root, text="Select File for FTP Upload: ",justify=LEFT)
#    entry1 = Entry(root, width=50)
#    entry1.insert(0,"Enter or Browse Upload File Path")
#    entry1.config(fg='grey')
#    label2 = Label(root, text="Select File for FTP Download: ",justify=LEFT)
#    entry2 = Entry(root, width=50)
#    entry2.insert(0,"Enter or Browse Download File Path")
#    entry2.config(fg='grey')
#    separator1 = Frame(root, height=2, bd=1, relief=SUNKEN)
#    separator2 = Frame(root, height=2, bd=1, relief=SUNKEN)
#    separator3 = Frame(root, height=2, bd=1, relief=SUNKEN)
#    separator4 = Frame(root, height=2, bd=1, relief=SUNKEN)
#    libox_serverdir = Listbox(width=40,height=14,selectmode=MULTIPLE)
#    
#    button_browselocal = Button(root,
#                           text="Browse Local",
#                           width=25,
#                           command=button_browselocal_callback)
#    button_upload = Button(root,
#                       text="Upload",
#                       width=25,
#                       command=button_upload_callback)
#    button_browseserver = Button(root,
#                           text="Browse Server",
#                           width=25,
#                           command=button_browseserver_callback)
#    button_download = Button(root,
#                       text="Download",
#                       width=25,
#                       command=button_download_callback)
#    button_exit = Button(root,
#                         text="Exit",
#                         width=25,
#                         command=sys.exit)
#    button_list = Button(root,
#                         text="List Server Files and Directories",
#                         width=25,
#                         command=button_list_callback)
#                         
#    
#    label1.pack()
#    entry1.pack(padx=5)
#    button_browselocal.pack(padx=5)
#    button_upload.pack(padx=5)
#    separator2.pack(fill=X, padx=5, pady=5)
#    label2.pack()
#    libox_serverdir.pack()
#    entry2.pack(padx=5)
#    button_browseserver.pack(padx=5)
#    button_download.pack(padx=5)
#    separator3.pack(side=TOP,fill=X,padx=5,pady=5)
#    button_list.pack(padx=5)
#    separator4.pack(side=TOP,fill=X,padx=5,pady=5)
#    button_exit.pack(padx=5, pady=(0,5))
#    
if __name__ == "__main__":
    """ Run as a stand-alone script """
    gui()