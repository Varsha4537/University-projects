class FairShare_Functions:

    def __init__(self):
        self.user_name = []  # Initial users
        self.num_users = len(self.user_name)
        self.passwords=[]
        self.expense_tracker = []  # Initialize before using
        if self.num_users > 0:
            self.expense_tracker.append([0] * self.num_users)
        self.i = 0  # Transaction index
        self.file = None

    def open_file(self):
        try:
            self.file = open("DB.text", "r+")  # Open for reading & writing without truncating
            lines = self.file.readlines()

            if not lines:
                self.i = 0
                self.user_name = []
                self.passwords = []
                self.num_users = 0
                self.expense_tracker = []
                return

            self.i = int(lines[0].strip()) if lines else 0  # First line: Number of transactions
            self.user_name = lines[1].strip().split() if len(lines) > 1 else []  # Usernames
            self.passwords = lines[2].strip().split() if len(lines) > 2 else []  # Passwords
            self.num_users = len(self.user_name)

            # Create an empty expense tracker with `self.i` rows and `self.num_users` columns
            self.expense_tracker = [[0] * self.num_users for _ in range(self.i)]

            # Read expense data from file (ensure correct size)
            for row_idx, line in enumerate(lines[3:self.i + 3]):  # Read only the expected rows
                values = list(map(float, line.split()))
                for col_idx, value in enumerate(values):
                    if col_idx < self.num_users:  # Avoid out-of-bounds errors
                        self.expense_tracker[row_idx][col_idx] = value

        except FileNotFoundError:
            self.file = open("DB.text", "w+")  # Create new file if missing

    def close_file(self):
        if self.file:
            self.file.seek(0)  # Reset file to beginning
            self.file.write(f"{self.i}\n")  # Write transaction count
            self.file.write(" ".join(self.user_name) + "\n")  # Write usernames
            self.file.write(" ".join(self.passwords) + "\n")  # Write passwords

            # Write expenses (truncate old content)
            for row in self.expense_tracker[:self.i]:
                self.file.write(" ".join(map(str, row)) + "\n")

            self.file.truncate()  # Remove any leftover data beyond new content
            self.file.close()
            self.file = None


    def register(self, user_name, password):
        if user_name not in self.user_name:  # Prevent duplicates
            self.user_name.append(user_name)
            self.passwords.append(password)
            self.num_users += 1
            for column in self.expense_tracker:
                column.append(0.0)  # Add a new column for the new user
            return 0
        else:
            print(f"User {user_name} is already registered.") 
            return 1

    def expense(self, user_name, amount):
        if user_name not in self.user_name: # Check if user is registered
            print(f"User {user_name} is not registered.")
            return

        column = self.user_name.index(user_name)  # Get user index
        # Ensure there are enough rows in expense_tracker
        while len(self.expense_tracker) <= self.i:
            self.expense_tracker.append([0.0] * self.num_users)  # Add missing rows
            
        if self.i < 50:  # Prevent out-of-bounds errors
            self.expense_tracker[self.i][column] = amount # Log the expense
            self.i += 1
            print(f"Logged expense of {amount} for {user_name}.")
        else:
            print("Transaction limit reached.")

    def report_user(self, user_name): # Report for a single user
        if user_name not in self.user_name:
            print(f"User {user_name} is not registered.")
            return

        column = self.user_name.index(user_name) # Get user index
        user_total = sum(self.expense_tracker[row][column] for row in range(self.i))  # Sum for the user
        total_expense = sum(sum(row) for row in self.expense_tracker)  # Sum of all expenses
        average = total_expense / self.num_users if self.num_users > 0 else 0 # Average expense per user
        output = []
        output.append(f"User {user_name}: Total Expense = {user_total}, Balance = {average - user_total}")
        return output
        #print(f"User {user_name}: Total Expense = {user_total}, Balance = {average - user_total}")

    def report(self): # Report for all users
        total_expense = sum(sum(row) for row in self.expense_tracker) # Total expense
        average = total_expense / self.num_users if self.num_users > 0 else 0 # Average expense per user
        output = []
        output.append(f"Average Expense per User: {average}") 

        for idx, user in enumerate(self.user_name): # Iterate over users
            user_total = sum(self.expense_tracker[row][idx] for row in range(self.i)) # Sum for the user
            print(f"{user} - Balance: {average - user_total}") # Print user balance
            output.append(f"{user} - Balance: {average - user_total}")
        return output

