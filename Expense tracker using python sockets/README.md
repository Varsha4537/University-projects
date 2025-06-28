FairShare Program with two user interfaces

The program was compiled on MacBook Air, Arm64 Architecture, M1 chip.
Compiled on the terminal using command "python3 FairShareUI.py"

ChatGPT Link: https://chatgpt.com/share/67dfdd35-5c6c-8005-82a8-6d0f3121cb95 
                https://chatgpt.com/share/67dfdd65-33a0-8005-98a3-b7705f073f33 
                

--------------------------------------------------------------------------------------------------------------

This folder contains four files.
FairShareUI.py: The main file. This is the client Server.
fairshar_Backend.py: This is the server containing all the backend functions.
DB.text: The DB that stores all the info.
        *Please DO NOT MESS with the DB.text file, the code is not independent of the DB.text file, any manual changes made to the DB.text file will crash the program.*
README.text: Contains the basic info you need to run this program. Please got thorugh this, before running the program.
logo.png: Just an image.



--------------------------------------------------------------------------------------------------------------

# TO RUN THE PROGRAM

Make sure you have TKinter installed.

Run the server first and then the client program.

have two terminals open at this folder.
On one first run:  'python fairshare_Backend.py'
On the second run: 'python FairShareUI.py'


--------------------------------------------------------------------------------------------------------------

In the DB.text file:
- the first line contains the number of transactions
- the second line consists of users
- the third line consists of passwords
- from the fourth line starts the matrix that stores the expenses of all the users

**NOTE: the distinction between two users is space, space is the delimiter, when registering or logging in do not add any spaces between the names instead use a '_'. Do not add spaces in expenses either.**

Sample Users: A B C 
Sample Passwords: 1234 5678 9101
There are no transactions recorded as of yet.

How to read the above:
User: A 
Password: 1234

User: B 
Password: 5678

--------------------------------------------------------------------------------------------------------------

**FairShareUI.py**

        There is load_fairshare1(), load_fairshare2() class and home function

        Home(): basic home interface with logo that give you two options either FaireShare1 or Fairshare2

        class load_fairshare1:
                Instructions are displayed for ease of use and no confusion
                for each function inside the file is opened and closed.
                this function contains more functions inside
                        - load_ui()
                        - register_user()
                        - log_expense()
                        - view_report()
                        - exit()
                        - show_expense_table():shows the DB.text in tabular form. Here the file opens and closes once it is done. This particular function is for fairshare1.
        
        class load_fairshare2:
                The file or DB.txt is opened in the begining of the load_fairshare2 function and closes when exit is pressed, do not directly close the program as it might cause loss of operations update on DB.txt.
                The functions inside this are
                        - load_ui()
                        - show_login()
                        - show_register()
                        - login_user()
                        - register_user()
                        - main_window()
                        - log_expense()
                        - view_report()
                        - view_report_all()
                        - show_expense_table()
                        - exit_fairshare(): closes the DB.text file and takes you to home function


COMMUNICATIONS USING SOCKETS

FairShare uses the socket module to facilitate client-server communication. The architecture follows a request-response model:

# Server Side

The server listens for incoming connections and creates a separate thread for each client.

It processes requests from clients and sends back responses, either as plain text or serialized Python objects using pickle.

Thread synchronization ensures that multiple clients can interact with shared data safely.

# Client Side

The client sends requests to the server as encoded strings.

It receives responses, decoding plain text or deserializing objects using pickle.loads().

It interacts with the GUI to send and display data.
