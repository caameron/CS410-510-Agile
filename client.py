import socket
import os.path
import sys
import os
import pickle
import shutil
import time
from select import select

currentclientpath = None
currentserverpath = None
currentpath = os.path.realpath("Logs")
logfile = os.path.join(currentpath,"client.log")
fObj = open(logfile,"a+")
fObj.write("\n******************************************************************************")
fObj.write("\nCurrent Session Date and Time:"+time.strftime("%c"))
fObj.write("\n******************************************************************************")

#method to print to display and logging
def printandlog(text):
    global fObj
    try:
        fObj.write("\n"+text)
    except:
        fObj.write("\n"+text.get_string())
    print text

#method to consume raw input and logging
def rawinputandlog(text):
    userin = raw_input(text)
    fObj.write("\n"+text+userin)
    return userin.upper()

def Main(username,password):
    global table
    global currentclientpath
    global currentserverpath
    global fObj

    currentclientpath = os.path.realpath("clientlocation")

    host = '127.0.0.1'  #host ip
    port = 8888         #port number

    s = socket.socket()             #get client socket s
    try:
        s.connect((host,port))      #attempt to connect to server using host and port.
    except:
        printandlog("Connection refused! Please ensure Server is up and running!!")
        return

    s.send(username)                #send username that was received from command line to server to check if username exists
    member = s.recv(1024)

    #send password next to server to validate.
    if member == 'NEW':
        s.send(password)
    if member == 'EXIST':
        s.send(password)

    login = s.recv(1024)
    #if received login info from server is FAIL then alert that its incorrect user/pass combo and disconnect client.
    if login == "FAIL":
        printandlog("Incorrect username and password combination, reconnect with: python client.py username password")
        s.close()
        sys.exit()
    #if login info from server is PASS and member is EXIST then this means already existing user relogging
    if login == "PASS" and member == "EXIST":
        printandlog("Welcome back " + username)
    #if login info is just PASS then new user is registered
    elif login == "PASS":
        printandlog("Thanks for registering on the FTP client " + username)

    try:
        #this will make a folder in the client's desktop (using relative pathing) called ClientFiles. This folder will
        #act as the primary directory for the client where files will be sent to and from the folder for put/get.
        os.mkdir(os.path.expanduser(currentclientpath))
    except:
        #if file already exists on desktop then just continue
        printandlog("CONTINUE")

    printandlog("")
    #Cameron:Added in While loop to keep asking for commands
    while True:
        fObj.write("\n******************************************************************************")
        printandlog("Enter \"HELP\" to show all supported commands")
        sys.stdout.write("\n>>> ")
        sys.stdout.flush()

        #Dhwanil: created a timeout mechanism where client disconnects from server if idle for a minute
        timeout = 60
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            action = sys.stdin.readline().strip()
         
        else:
            print("\n\n\nIdle for too long. Disconnecting...")
            action = "QUIT"
        
        action = action.upper()

        #Namratha: Created a command line of sorts to input commands and parameters. Enter "HELP" to get the list of all commands
        if action == "HELP":
            from prettytable import PrettyTable
            table = PrettyTable()
            table.field_names = ["COMMAND","DESCRIPTION"]
            table.add_row(["GET","Download file from server"])
            table.add_row(["PUT","Upload file to server"])
            table.add_row(["MKDIR","Create directory on server"])
            table.add_row(["LIST","List files in local or server"])
            table.add_row(["GETMULTIPLE","Download file from server"])
            table.add_row(["PUTMULTIPLE","Upload file to server"])
            table.add_row(["CD","Change directory"])
            table.add_row(["DELETEFILE","Delete file"])
            table.add_row(["DELETEDIR","Delete directory"])
            table.add_row(["RENAME","Rename file in local or server"])
            table.add_row(["SEARCH","Search file in local or server"])
            table.add_row(["COPY","Copy directories on server"])
            table.add_row(["QUIT","Log Off"])
            printandlog(table)
            continue

        #Namratha: Check on client side to ensure only valid commands are sent to the server. Additional check is done on the server side for supported commands
        if action not in ["GET","PUT","MKDIR","LIST","CD","DELETEFILE","DELETEDIR","RENAME","SEARCH","QUIT","GETMULTIPLE","PUTMULTIPLE","COPY"]:
            printandlog("Unsupported command!!")
            continue

        s.send(action)          #send the attempted command to server to get server ready to perform desired command
        command = s.recv(1024)  #get verification from server that we will be performing command, get client ready.

        #IMPORTANT: right now the way its set up is to allow only one command before client is disconnected, if want to continue to
        #carry out commands then we need a WHILE loop for all these if statements
        #*********************************************
        #Caameron: Added in the while loop so that the server and client should keep asking for you if you
        #want to do any addition commands. Will stop once you enter 'N'.
        #The changes are made above after the print("CONTINUE") statement

        #if command is GET then we can use this to get a file from the server (get a file from server's Serverfiles directory)
        if command == 'GET':
            filename = rawinputandlog("Enter filename you want to get from server: ")
            s.send(filename)
            content = s.recv(1024)
            if content[:5] == 'FOUND':    #file was found in server
                filesize = long(content[5:])
                response = rawinputandlog("File to GET is " + str(filesize) + " Bytes, Proceed? (Y/N) ")
                if response == 'Y':
                    s.send('OKSEND')    #tell server it can send the data now
                    completename = os.path.join(os.path.expanduser(currentclientpath),filename) #this gets full path to ClientFiles
                    #get ready to write the file to ClientFiles
                    f = open(completename, 'wb')
                    content = s.recv(1024) #initial receive of data from server
                    currentrec = len(content)
                    f.write(content)

                    #while the currentrecieved data is less than the actual size of data keep recieving bytes
                    while currentrec < filesize:
                        content = s.recv(1024)
                        currentrec = currentrec + len(content)
                        f.write(content)

                    printandlog("GET successful")
                else:
                    printandlog("Aborting GET")

            #this else branch taken if file not found
            else:
                printandlog("File not found in server")

        #if command is PUT then we can use this to put a file from client (ClientFiles) to server's ServerFiles directory
        #uses similar logic as GET except almost reversed.
        elif command == 'PUT':
            filename = rawinputandlog("Enter filename you want to put to server: ")
            completename = os.path.join(os.path.expanduser(currentclientpath),filename)
            #if the file exists in the Client's ClientFiles directory then continue
            if os.path.isfile(completename):
                s.send(filename)
                feedback = s.recv(1024)
                if feedback == 'OKSEND':
                    filesize = str(os.path.getsize(completename))
                    s.send(filesize)
                    response = rawinputandlog("File to PUT is " + str(filesize) + " Bytes, Proceed? (Y/N) ")
                    if response == 'Y':
                        #open the file found in client and get ready to send the data over to the server
                        with open(completename, 'rb') as f:
                            sendbyte = f.read(1024)    #this will read and return bytes from file
                            s.send(sendbyte) #send the bytes to server
                            currentsent = len(sendbyte)
                            while sendbyte != "":
                                sendbyte = f.read(1024)
                                s.send(sendbyte)
                                currentsent += len(sendbyte)

                                #like in SET, below will simulate a progress bar.
                                os.system('clear')
                                progress = '['
                                for x in range (0, int(currentsent/float(filesize) * 100)):
                                                            progress += '#'
                        printandlog("PUT successful")
                    else:
                        s.send("!!!")    #this will alert server that we aren't proceeding with PUT

            #This branch taken if file not found in client.
            else:
                s.send("!!!")    #this will alert the server that we aren't proceeding with PUT
                print("File not found in client")

        #Caameron: if command is MKDIR then ask the user for the name of new directory and send it over to the
        #server to be created. Print out if successfull or not
        elif command == "MKDIR":
            directory_name = rawinputandlog("Enter name of directory you want to create: ")
            s.send(directory_name)
            feedback = s.recv(1024)
            if feedback == "DONE":
                printandlog("Directory Created")
            else:
                printandlog("ERROR directory not created")

        #Caameron: if command is LIST ask the user if they want to display the files and directories on the local
        #or server and then print them out accordingly
        elif command == "LIST":
            choice = rawinputandlog("List files/directories for server or local? (SERVER or LOCAL): ")
            s.send(choice)
            #Because this is not a list, we need to receieve it and then use pickle to load the data sent over.
            data = s.recv(1024)
            files = pickle.loads(data)
            printandlog('Files with have an extensions. Directories will just be a name')
            for file in files :
                printandlog('%s' % file)

        #Namratha: need to add path variable to all command methods to be able to make this work in any directory of server
        elif command == "CD":
            choice = rawinputandlog("Change directory in server or local? (SERVER or LOCAL): ")
            if choice in "LOCAL":
                s.send(choice)
                dirname = rawinputandlog("Enter local directory name to CD into: ")
                if os.path.exists(currentclientpath+"\\"+dirname):
                    currentclientpath = currentclientpath+"\\"+dirname
                    s.send(currentclientpath)
                    printandlog(currentclientpath)
                else:
                    printandlog("Directory: %s does not exist. Please use LIST to see what directories exist in local!"%dirname)

            elif choice in "SERVER":
                s.send(choice)
                dirname = rawinputandlog("Enter server directory name to CD into: ")
                s.send(dirname)
                direxists = s.recv(1024)
                if direxists in "PASS":
                    printandlog("CD in server successful")

        elif command == "DELETEFILE":
            choice = rawinputandlog("Delete file in server or local? (SERVER or LOCAL): ")
            filename = rawinputandlog("Enter filename(s) to delete (ex: file1.txt file2.txt file2.txt ...): ")
            if choice in "LOCAL":
                s.send("LOCAL")
                filepath = currentclientpath+"\\"+filename
                if os.path.exists(filepath):
                    os.remove(filepath)
                    if not os.path.exists(filepath):
                        printandlog("File \"%s\" deleted"%filename)
                    else:
                        printandlog("Unable to delete \"%s\""%filename)
                else:
                    printandlog("File \"%s\" does not exist in directory \"%s\". Please use LIST to see files in local"%(filename,currentclientpath))
            elif choice in "SERVER":
                s.send("SERVER")
                s.send(filename)
                filelist = filename.split(" ")
                for filename in filelist:
                    deletestatus = s.recv(1024)
                    if deletestatus in "PASS":
                        printandlog("File \"%s\" deleted"%filename)
                    else:
                        printandlog("Unable to delete %s"%filename)
            else:
                s.send("UNKNOWN")
                response = s.recv(1024)

        elif command == "DELETEDIR":
            choice = rawinputandlog("Delete directory on server or local? (SERVER or LOCAL): ")
            dirname = rawinputandlog("Enter directory name to delete: ")
            if choice in "LOCAL":
                s.send("LOCAL")
                dirpath = os.path.join(currentclientpath,dirname)
                printandlog("dirpath \"%s\""%dirpath)
                if os.path.exists(dirpath):
                    shutil.rmtree(dirpath)
                    if not os.path.exists(dirpath):
                        printandlog("Directory \"%s\" deleted"%dirname)
                    else:
                        printandlog("Unable to delete \"%s\""%dirname)
                else:
                    printandlog("Directory \"%s\" does not exist ! \"%s\". Please use LIST to see files in local"%(dirname,currentclientpath))
            elif choice in "SERVER":
                s.send("SERVER")
                s.send(dirname)
                dirlist = dirname.split(" ")
                for dirname in dirlist:
                    deletestatus = s.recv(1024)
                    if deletestatus in "PASS":
                        printandlog("Directory \"%s\" deleted"%dirname)
                    else:
                        print "Unable to delete %s"%dirname
        
            else:
                s.send("UNKNOWN")
                response = s.recv(1024)

        elif command == "RENAME":
            choice = raw_input("Rename file for server or local? (SERVER or LOCAL): ")
            changefile = raw_input("Enter filename to change: ")
	    newname = raw_input("Enter new name: ")
            if choice in "LOCAL":
  		##path = os.getcwd()
      	  	print "Current working dir : %s" % os.getcwd()        
                # Now open a directory "/tmp"
		fd = os.open( "clientlocation", os.O_RDONLY )
		# Use os.fchdir() method to change the dir
		os.fchdir(fd)
	        # Print current working directory
		print "Current working dir : %s" % os.getcwd()
    ##                break	
	        if os.path.exists(changefile) == True:
		    os.rename(changefile, newname)
                else:
		    print "error!" 
			
      	    elif choice in "SERVER":
		s.send("SERVER")
	        	
      	  	print "Current working dir : %s" % os.getcwd()        
                # Now open a directory "/tmp"
		fd = os.open( "serverlocation", os.O_RDONLY )
		# Use os.fchdir() method to change the dir
		os.fchdir(fd)
	        # Print current working directory
		print "Current working dir : %s" % os.getcwd()
   
	        if os.path.exists(changefile) == True:
		    os.rename(changefile, newname)
	              	

        elif command == "SEARCH":
            choice = rawinputandlog("Rename file for server or local? (SERVER or LOCAL): ")
            fileregex = rawinputandlog("Enter filename or extension to search: ")
            if choice in "LOCAL":
                s.send("LOCAL")
                directory = currentclientpath
                fileregex = fileregex.lower()
                for dirpath, dirnames, files in os.walk(directory):
                    for name in files:
                        if fileregex.lower() in name.lower():
                            printandlog(os.path.join(dirpath, name))
                        elif not fileregex:
                            continue

            elif choice in "SERVER":
                s.send("SERVER")
                s.recv(1024)
                s.send(fileregex)
                searchstatus = s.recv(1024)
                if searchstatus in "PASS":
                    foundList = s.recv(1024)
                    for file in foundList.lstrip("[").rstrip("]").split(","):
                        printandlog(file)
                else:
                    printandlog("File not found!")

        elif command == "QUIT":
            fObj.close()
            break

        elif command == "UNSUPPORTED":
            printandlog("Server does not support commmand: ", action, ". Please check again!")



##    other commands can go here in if statements like list directories, etc.
##    just be sure to also implement the complementary command for the server.
##    for example:

##    elif command == 'LISTSERVER':
##        enter code here to list files and directories found in server (aka files found in ServerFiles)

##    elif command == 'LISTCLIENT':
##        enter code here to list files and directories found in client (aka files found in ClientFiles)


    s.close()


#Make sure the correct amount of arguments are given when running in command line
if(len(sys.argv) < 3):
    print ('Connect to server with: python client.py username password')
    sys.exit()

#get the username and password entered in command line
username = sys.argv[1]
password = sys.argv[2]

#pass username and password to main function.
if __name__ == '__main__':
    Main(username,password)
