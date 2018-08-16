Unit tests completed manually and verified before setting story to “done done”. 

# Unit test checklist for each story:

## Login into remote ftp server <br />
Test 1: Single client can connect to server. DONE <br />
Test 2: Multiple clients can connect to server. DONE<br />
Test 3: username and password saved on server. DONE<br />
Test 4: Invalid login when wrong combination. DONE<br />
Test 5: Valid login when correct combination. DONE<br />

## List files/directories on server<br />
Test 1: List files in serverlocation directory. DONE<br />
Test 2: List directory in serverlocation directory. DONE<br />
Test 3: List blank if no files or directories. DONE<br />

## List files/directories on client<br />
Test 1: List files in clientlocation directory. DONE<br />
Test 2: List directory in clientlocation directory. DONE<br />
Test 3: List blank if no files or directories. DONE<br />

## Get file from server<br />
Test 1: Check if file exists and if so gets file from server. DONE<br />
Test 2: If file doesn’t exist no transfer. DONE<br />
Test 3: Transfer works on all types of extensions. DONE<br />

## Put file to server<br />
Test 1: Check if file exists and if so put file to server. DONE<br />
Test 2: If file doesn’t exist no transfer. DONE<br />
Test 3: Transfer works on all types of extensions. DONE<br />

## Get multiple<br />
Test 1: More than one file can be received from server. DONE<br />
Test 2: Deals with case where file doesn’t exist. DONE<br />
Test 3: Correctly runs the desired amount of iterations. DONE<br />

## Put multiple<br />
Test 1: More than one file can be received from server. DONE<br />
Test 2: Deals with case where file doesn’t exist. DONE<br />
Test 3: Correctly runs the desired amount of iterations. DONE<br />

## Create directory<br />
Test 1: directory created within the working directory. DONE<br />
Test 2: directory persists. DONE<br />

## Delete file in server<br />
Test 1: Delete file name that is chosen. DONE<br />
Test 2: No action/error if file does not exist. DONE<br />

## Log history<br />
Test 1: Log all commands to external text file. DONE<br />
Test 2: Log client information in logs. DONE<br />
Test 3: Log information persists even after disconnection. DONE<br />

## Search files on server<br />
Test 1: If desired file exists then shows path. DONE<br />
Test 2: if desired file does not exist then error. DONE<br />
Test 3: if no files in directory then error handled. DONE<br />

## Rename file in server<br />
Test 1: rename a file that doesn't exist. DONE<br />
Test 2: renaming a file that already exists. DONE<br />

## Rename file in client<br />
Test 1: rename a file that doesn't exist. DONE<br />
Test 2: renaming a file that already exists. DONE<br />

## Delete directory on client/server<br />
Test 1: If directory exists, delete. DONE<br />
Test 2: If directory does not exist then return error. DONE<br />
Test 3: Ensure contents of directory also deleted. DONE<br />

## Timeout if idle<br />
Test 1: if no command given in 600 seconds then timeout. DONE<br />
Test 2: if no command given within duration then client correctly disconnected. DONE<br />
Test 3: if command is issued before timer then no timeout. DONE<br />
