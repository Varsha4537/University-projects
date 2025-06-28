FairShare Program with two user interfaces

The program was compiled on MacBook Air, Arm64 Architecture, M1 chip.
Compiled on the terminal using command "python3 FairShareUI.py"

ChatGPT Link: https://chatgpt.com/share/67d7106b-397c-8005-87a7-b34f0a1f5c9f 
                https://chatgpt.com/share/67d71082-73a8-8005-bae5-4e234e2ea6cd 
                https://chatgpt.com/share/67d71099-513c-8005-8d33-a9f337bffbbe 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This folder contains four files.
FairShareUI.py: The main file. Run this to start the program process. The structure of this is given further below.
fairshar_Backend.py: This file contains the backend process for the program.
DB.text: The DB that stores all the info.
        *Please DO NOT MESS with the DB.text file, the code is not independent of the DB.text file, any manual changes made to the DB.text file will crash the program.*
README.text: Contains the basic info you need to run this program. Please got thorugh this, before running the program.
logo.png: Just an image.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

                        


        

