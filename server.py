import socket
import threading
import os
import pickle
import shutil
#Global variables
currentserverpath = None
currentclientpath = None
users = []    ##this is a list of tuples storing username and password like (username, password).

#function to be run by each socket thread
def clientrun(name,sock):
    global currentserverpath
    global currentclientpath

    currentclientpath = os.path.realpath("ClientLocation")
    currentserverpath = os.path.realpath("ServerLocation")

    #Start by attempting to authenticate the client that is connecting to server
    username = sock.recv(1024)    #get username from client
    exists = False
    logincheck = False
    #check to see if username already exists in server's users list
    for i in users:
        if i[0] == username:
            exists = True
    #if user doesn't exist then add user to list (newly registed user)
    if exists == False:
        sock.send("NEW")
        password = sock.recv(1024)
        users.append((username,password))
        logincheck = True
    #if user already exists in list then check if password combo is correct
    elif exists == True:
        sock.send("EXIST")
        password = sock.recv(1024)
        for i in users:
            if i[0] == username and i[1] == password:
                logincheck = True
    #Send login status to client based on above checks
    if logincheck == False:
        sock.send("FAIL")
    elif logincheck == True:
        sock.send("PASS")

    #check what command client is requesting to perform
    #IMPORTANT: right now the way its set up is to allow only one command, if want to continue to
    #carry out commands then we need a WHILE loop for all these if statements
    #*********************************************
    #Caameron: Added in the while loop so that the server and client should keep asking for you if you
    #want to do any addition commands. Will stop once you enter 'N'
    while True:
        #print("Wait for command")
        command = sock.recv(1024)
        #if command is GET then get ready to send file to client.
        #send file from Serverfiles to client's ClientFiles directory.
        if command == "GET":
            sock.send("GET")    #send this command back to client to verify action
            filename = sock.recv(1024)
            #get the complete relative path to ServerFiles
            completename = os.path.join(os.path.expanduser(currentserverpath),filename)
            #check if file exists in ServerFiles directory
            if os.path.isfile(completename):
                sock.send("FOUND " + str(os.path.getsize(completename)))
                response = sock.recv(1024)
                if response[:6] == 'OKSEND':
                    #open file and start sending bytes to client untill all is sent
                    with open(completename, 'rb') as f:
                        sendbyte = f.read(1024)
                        while sendbyte != "":
                            sock.send(sendbyte)
                            sendbyte = f.read(1024)
            else:
                sock.send("NOFOUND")

        #if command is PUT then get ready to recieve file from client.
        #recieve file from Clientfiles to server's ServerFiles directory.
        elif command == "PUT":
            sock.send("PUT")    #send this command back to client to verify action
            filename = sock.recv(1024)
            #if filename is valid proceed
            if filename != '!!!':
                sock.send("OKSEND")
                filesize = long(sock.recv(1024))
                completename = os.path.join(os.path.expanduser(currentserverpath),filename)
            ##    f = open(completename, 'wb')
                content = sock.recv(1024)
                if content != '!!!':
                    f = open(completename, 'wb')
                    currentrec = len(content)
                    f.write(content)
                    #continue to receive data from client untill current recieve
                    #equals the filesize.
                    while currentrec < filesize:
                        content = sock.recv(1024)
                        currentrec = currentrec + len(content)
                        f.write(content)


        #Caameron: if command is MKDIR then we will obtain the name of the directory from the client
        #and create a new directory in ServerFiles with that name.
        elif command == "MKDIR":
            sock.send("MKDIR")
            directory_name = sock.recv(1024)
            dirpath = os.path.join(currentserverpath,directory_name)
            os.mkdir(dirpath)
            sock.send("DONE")

        #Caameron: if command is LIST then ask the user if they want to display the local or server
        #files and directories and print them out accordingly
        elif command == "LIST":
            sock.send("LIST")
            choice = sock.recv(1024)
            #Because this is a list and not a string we have to first pickle.dump the contents to be sent over
            #to the client.
            if choice == "SERVER":
                files = os.listdir(os.path.expanduser(currentserverpath))
                send_files = pickle.dumps(files)
                sock.send(send_files)
            elif choice == "LOCAL":
                files = os.listdir(os.path.expanduser(currentclientpath))
                send_files = pickle.dumps(files)
                sock.send(send_files)

        elif command == "CD":
            sock.send("CD")
            choice=sock.recv(1024)
            if choice in "LOCAL":
                currentclientpath = sock.recv(1024)
                print "Current client path: ",currentclientpath
            elif choice in "SERVER":
                dirname = sock.recv(1024)
                if os.path.exists(currentserverpath+"\\"+dirname):
                    currentserverpath = currentserverpath+"\\"+dirname
                    print "Current server path: ", currentserverpath
                    sock.send("PASS")
                else:
                    print "Path: ",currentserverpath+"\\"+dirname, " does not exist on server"
                    sock.send("FAIL")

        elif command == "DELETEFILE":
            sock.send("DELETEFILE")
            choice = sock.recv(1024)
            if choice in "LOCAL":
                continue
            elif choice in "SERVER":
                filenames = sock.recv(1024)
                filelist = filenames.split(" ")
                for filename in filelist:
                    filepath = currentserverpath+"\\"+filename
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        if not os.path.exists(filepath):
                            print "File \"%s\" deleted"%filename
                            sock.send("PASS")
                        else:
                            print "Unable to delete \"%s\""%filename
                            sock.send("FAIL")
                    else:
                        sock.send("FAIL")
                        print "File \"%s\" does not exist in directory \"%s\". Please use LIST to see files in server"%(filename,currentserverpath)
            else:
                continue

        elif command == "DELETEDIR":
            sock.send("DELETEDIR")
            choice = sock.recv(1024)
            if choice in "LOCAL":
                continue
            elif choice in "SERVER":
                dirnames = sock.recv(1024)
                dirlist = dirnames.split(" ")
                for dirname in dirlist:
                    dirpath = os.path.join(currentserverpath,dirname)
                    print "dirpath \"%s\""%dirpath
                    if os.path.exists(dirpath):
                        shutil.rmtree(dirpath)
                        if not os.path.exists(dirpath):
                            print "Directory \"%s\" deleted"%dirname
                            sock.send("PASS")
                        else:
                            print "Unable to delete \"%s\""%dirname
                            sock.send("FAIL")
                    else:
                        sock.send("FAIL")
                        print "Directory \"%s\" does not exist! \"%s\". Please use LIST to see files in server"%(dirname,currentserverpath)
            else:
                continue

        elif command == "RENAME":
            sock.send("RENAME")

        elif command == "SEARCH":
            sock.send("SEARCH")
            choice = sock.recv(1024)
            if choice in "LOCAL":
                continue
            elif choice in "SERVER":
                sock.send("OKSENDFILE")
                fileregex = sock.recv(1024)
                directory = currentserverpath
                fileregex = fileregex.lower()
                foundList = []
                for dirpath, dirnames, files in os.walk(directory):
                    for name in files:
                        if fileregex.lower() in name.lower():
                            print(os.path.join(dirpath, name))
                            foundList.append(os.path.join(dirpath, name))
                        elif not fileregex:
                            print(os.path.join(dirpath, name))
                if len(foundList) < 1:
                    sock.send("FAIL")
                else:
                    sock.send("PASS")
                    sock.send(str(foundList))

        elif command == "QUIT":
            sock.send("QUIT")
            print("CLOSING")
            sock.close()
            return

        else:
            sock.send("UNSUPPORTED")

        #Wait for response if the user wants to complete another command.
        #Loop breaks if client doesn't respond 'again'
        #continue_response = sock.recv(1024)
        #if continue_response != 'again':
        #    break
##      other commands can go here in if statements like list directories, etc.
##      just be sure to also implement the complementary command for the client.
##      for example:

##      elif command == 'LISTSERVER':
##        sock.send('LISTSERVER')
##              enter code here to list files and directories found in server (aka files found in ServerFiles)



def Main():
    global currentclientpath
    global currentserverpath

    host = '127.0.0.1'    #host ip of server
    port = 8888    #port of server

    try:
        #make a folder/directory on the relative path to desktop of server called ServerFiles.
        #this folder will be the primary directory where files will be sent to and from.
        os.mkdir(os.path.expanduser(currentserverpath))
    except:
        #continue if folder already exists in server's desktop.
        print("CONTINUE")

    s = socket.socket()    #get server socket
    s.bind((host,port))    #bind host ip with port

    s.listen(5)    #start listening for connections

    print("Server connected")
    #Server will continue to run forever
    while True:
        c, addr = s.accept()    #accept a client socket that is connecting
        print("client connected to server: " + str(addr))
        #start seperate thread for the client
        t = threading.Thread(target=clientrun, args=("clientrun",c))
        t.start()

    s.close()

if __name__ == '__main__':
    Main()
