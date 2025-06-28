from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from fairshare_Backend import FairShare_Functions #importing backend logic        


class FairShare1:
    def __init__(self, parent, fairshare_instance, home_callback):
        self.parent = parent
        self.fairshare = fairshare_instance  # Pass FairShare_Functions instance
        self.home_callback = home_callback  # Function to go back to home
        self.report_text = StringVar()
        self.load_ui()

    def load_ui(self):
        self.fairshare.open_file()
        for widget in self.parent.winfo_children():
            widget.pack_forget()

        Button(self.parent, text="Home", highlightbackground="light blue", fg="black", 
                  command=self.home_callback, font=("Helvetica", 14, "bold"), width=5, height=2).pack(anchor='nw', pady=5, padx=5)
        
        Label(self.parent, text="Welcome to FairShare1 🤗", font=("Helvetica", 22, "bold"), bg="black", fg="white").pack(pady=10)
        
        instructions_text = (
            "📌 **Register User:** Enter username and password in the expense textbox, then click the Register button.\n\n"
            "📌 **Log Expense:** Enter username & expense amount, then click the Log Expense button.\n\n"
            "📌 **View Report:** Enter username & click the View Report button to see expenses & balance owed.\n"
            "📌 **View Table:** Displays all transactions and records in the database.\n\n"
            "📌 **Exit:** Click the Exit button to return home."
        )
        
        Label(self.parent, text=instructions_text, font=("Helvetica", 14), bg="light blue", fg="blue", justify="left", anchor="w").pack(fill="x", padx=10, pady=10)
        
        self.username_entry = Entry(self.parent, font=("Arial", 14))
        self.expense_entry = Entry(self.parent, font=("Arial", 14))
        
        Label(self.parent, text="Enter Roommate:", font=("Arial", 14), bg="black", fg="white").pack()
        self.username_entry.pack(pady=5)
        
        Label(self.parent, text="Enter Expense:", font=("Arial", 14), bg="black", fg="white").pack()
        self.expense_entry.pack(pady=5)
        
        button_frame = Frame(self.parent)
        button_frame.pack(pady=30)
        
        Button(button_frame, text="Register User", highlightbackground="light blue", fg="black", command=self.register_user, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="Log Expense", highlightbackground="light blue", fg="black", command=self.log_expense, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="View Report", highlightbackground="light blue", fg="black", command=self.view_report, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="View Table", highlightbackground="light blue", fg="black", command=self.show_expense_table, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="Exit", highlightbackground="light blue", fg="black", command=self.home_callback, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        
        Label(self.parent, textvariable=self.report_text, font=("Arial", 12), wraplength=500, bg="black", fg="white").pack(pady=10)
    
    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.expense_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Enter a valid username.")
            return
        self.fairshare.open_file()
        if username in self.fairshare.user_name:
            messagebox.showerror("Error", f"User {username} already exists.")
        else:
            self.fairshare.register(username, password)
            messagebox.showinfo("Success", f"User {username} registered successfully.")
        self.fairshare.close_file()
    
    def log_expense(self):
        username = self.username_entry.get().strip()
        amount = self.expense_entry.get().strip()
        try:
            amount = float(amount)
            self.fairshare.open_file()
            self.fairshare.expense(username, amount)
            self.fairshare.close_file()
            messagebox.showinfo("Success", f"Expense of {amount} logged for {username}.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")
    
    def view_report(self):
        self.fairshare.open_file()
        username = self.username_entry.get().strip()
        if username:
            report_data = self.fairshare.report_user(username)
        else:
            report_data = self.fairshare.report()
        self.report_text.set("\n".join(report_data))
        messagebox.showinfo("Report", "\n".join(report_data))
        self.fairshare.close_file()
    
    def show_expense_table(self):
        self.fairshare.open_file()
        table_window = Toplevel()
        table_window.title("Expense Tracker")
        table_window.geometry("700x400")
        if not hasattr(self.fairshare, "i") or self.fairshare.i == 0:
            messagebox.showwarning("No Data", "No transactions available!")
            return
        columns = ["Transaction"] + self.fairshare.user_name  
        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        for idx in range(self.fairshare.i):  
            row_data = [idx + 1] + self.fairshare.expense_tracker[idx][:self.fairshare.num_users]  
            tree.insert("", "end", values=row_data)
        tree.pack(expand=True, fill="both", padx=10, pady=10)
        scrollbar_x = ttk.Scrollbar(table_window, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_y = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)
        self.fairshare.close_file()
        self.username_entry = None
        self.password_entry = None
        self.reg_username_entry = None
        self.reg_password_entry = None


class FairShare2:
    def __init__(self, frame, fairshare, home_Page):
        self.frame = frame
        self.fairshare = fairshare
        self.home_Page = home_Page
        self.expense_entry = None
        self.report_text = StringVar()
        self.username_entry = None
        self.password_entry = None
        self.reg_username_entry = None
        self.reg_password_entry = None

    def load_ui(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()

        self.home_button = Button(self.frame, text="Home", highlightbackground="light blue", fg="black", 
                                  command=self.home_Page, font=("Helvetica", 14, "bold"), width=5, height=2)
        self.home_button.pack(anchor='nw', pady=5, padx=5)

        self.logo = PhotoImage(file="logo.png")
        self.logo_label = Label(self.frame, image=self.logo, bg="black")
        self.logo_label.image = self.logo
        self.logo_label.pack(pady=10)

        Label(self.frame, text="Welcome to FairShare2", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)
        Label(self.frame, text="Click Below to either Login or Register", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)

        Button(self.frame, text="LOGIN", highlightbackground="light blue", fg="black", 
               command=self.show_login, font=("Helvetica", 14, "bold"), width=10, height=2).pack(pady=10)

        Button(self.frame, text="REGISTER", highlightbackground="light blue", fg="black", 
               command=self.show_register, font=("Helvetica", 14, "bold"), width=10, height=2).pack(pady=10)
        
    def show_login(self):
        for widget in frame.winfo_children():
            widget.pack_forget()

        self.home_button = Button(self.frame, text="Home", highlightbackground="light blue", fg="black", 
                                  command=self.home_Page, font=("Helvetica", 14, "bold"), width=5, height=2)
        self.home_button.pack(anchor='nw', pady=5, padx=5)
        home_logo()
        Label(frame, text="Enter Username:", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)
        global username_entry, password_entry
        username_entry = Entry(frame, font=("Arial", 14))
        username_entry.pack(pady=5)

        Label(frame, text="Enter Password:", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)
        password_entry = Entry(frame, font=("Arial", 14), show="*")  # Hides password input
        password_entry.pack(pady=5)

        Button(frame, text="Submit", highlightbackground="light blue", fg="black", 
               command=self.login_user, font=("Helvetica", 14, "bold"), width=10, height=2).pack(pady=10)

    def show_register(self):
        # Use self.frame instead of frame
        for widget in self.frame.winfo_children():
            widget.pack_forget()
        
        self.home_button = Button(self.frame, text="Home", highlightbackground="light blue", fg="black", 
                                  command=self.home_Page, font=("Helvetica", 14, "bold"), width=5, height=2)
        self.home_button.pack(anchor='nw', pady=5, padx=5)
        home_logo() 

        Label(self.frame, text="Enter New Username:", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)

        # Store entry fields as instance variables
        self.reg_username_entry = Entry(self.frame, font=("Arial", 14))
        self.reg_username_entry.pack(pady=5)

        Label(self.frame, text="Enter New Password:", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)

        self.reg_password_entry = Entry(self.frame, font=("Arial", 14), show="*")
        self.reg_password_entry.pack(pady=5)

        Button(self.frame, text="Submit", highlightbackground="light blue", fg="black", 
            command=self.register_user, font=("Helvetica", 14, "bold"), width=10, height=2).pack(pady=10)

        
    def login_user(self):
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Enter a valid username and password.")
            return

        if username not in self.fairshare.user_name:
            messagebox.showerror("Error", f"User {username} not found.")
        elif password != self.fairshare.passwords[self.fairshare.user_name.index(username)]:
            messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showinfo("Success", f"User {username} logged in successfully.")
            self.main_window(username)

    def register_user(self):
        new_username = self.reg_username_entry.get().strip()
        new_password = self.reg_password_entry.get().strip()

        if new_username == "" or new_password == "":
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return

        if new_username in self.fairshare.user_name:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.fairshare.register(new_username, new_password)
            messagebox.showinfo("Success", "Registration successful!")
            self.main_window(new_username)

    def main_window(self, username):
        for widget in self.frame.winfo_children():
            widget.pack_forget()

        Label(self.frame, text=f"Welcome to FairShare2 {username} 🤗", font=("Helvetica", 22, "bold"), bg="black", fg="white").pack(pady=10)

        instructions_text = (
        "📌 **Log Expense:** Enter the amount and click the Log Expense button.\n\n"
        "📌 **View Report:** Click to view your expense report.\n"
        "Expense: total expense made by the user, Balance: total amount owed by the user.\n\n"
        "📌 **View Report (All Users):** View reports for all users.\n\n"
        "📌 **View Table:** Displays all transactions and records in the database.\n\n"
        "📌 **Exit:** Click to exit the program.")

        Label(
            self.frame, text=instructions_text,
            font=("Helvetica", 16), bg="light blue", fg="blue",
            justify="left", anchor="w").pack(fill="x", padx=10, pady=10)

        self.report_text = StringVar()

        self.expense_entry = Entry(self.frame, font=("Arial", 14))
        self.expense_entry.pack(pady=5)

        button_frame = Frame(self.frame)
        button_frame.pack(pady=30)

        Button(button_frame, text="Log Expense", highlightbackground="light blue", fg="black", command=lambda: self.log_expense(username), font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="View Report", highlightbackground="light blue", fg="black", command=lambda: self.view_report(username), font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="View Report All", highlightbackground="light blue", fg="black", command=self.view_report_all, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="View Table", highlightbackground="light blue", fg="black", command=self.show_expense_table, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="Exit", highlightbackground="light blue", fg="black", command=self.exit_fairshare, font=("Helvetica", 14, "bold"), width=10, height=2).pack(side=LEFT, padx=5)

        Label(self.frame, textvariable=self.report_text, font=("Arial", 12), wraplength=500, bg="black", fg="white").pack(pady=10)


    def log_expense(self, username):
        amount = self.expense_entry.get().strip()
        try:
            amount = float(amount)
            self.fairshare.expense(username, amount)
            messagebox.showinfo("Success", f"Expense of {amount} logged for {username}.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def view_report(self, username):
        report_data = self.fairshare.report_user(username)
        self.report_text.set("\n".join(report_data))
        messagebox.showinfo("Report", "\n".join(report_data))

    def view_report_all(self):
        report_data = self.fairshare.report()
        self.report_text.set("\n".join(report_data))
        messagebox.showinfo("Report", "\n".join(report_data))

    def show_expense_table(self):
        table_window = Toplevel()
        table_window.title("Expense Tracker")
        table_window.geometry("700x400")

        if not hasattr(self.fairshare, "i") or self.fairshare.i == 0:
            messagebox.showwarning("No Data", "No transactions available!")
            return

        columns = ["Transaction"] + self.fairshare.user_name  
        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        for idx in range(self.fairshare.i):  
            row_data = [idx + 1] + self.fairshare.expense_tracker[idx][:self.fairshare.num_users]  
            tree.insert("", "end", values=row_data)

        tree.pack(expand=True, fill="both", padx=10, pady=10)

        scrollbar_x = ttk.Scrollbar(table_window, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        scrollbar_y = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

    def exit_fairshare(self):
        self.fairshare.close_file()
        self.home_Page()



def home_logo():
    frame.logo = PhotoImage(file="logo.png")
    logo_label = Label(frame, image=frame.logo, bg="black")
    logo_label.pack(pady=10)  # Only pack once

def home_Page():
    fairshare = FairShare_Functions()  # Your existing backend logic  
    app = FairShare1(frame, fairshare, home_Page)  # Create an instance of the class
    app2 = FairShare2(frame, fairshare, home_Page)  # Create an instance of the class
    
    for widget in frame.winfo_children():
        widget.pack_forget()

    # Load and display the logo
    home_logo()
    
    Label(frame, text="FAIR SHARE APP", font=("Helvetica", 18, "bold"), bg="black", fg="white").pack(pady=10)
    Label(frame, text="Choose the interface you want to use", font=("Helvetica", 16, "bold"), bg="black", fg="white").pack(pady=10)

    Button(frame, text="FairShare1", highlightbackground="light blue", fg="black", 
           command=app.load_ui, font=("Helvetica", 14, "bold"), width=10, height=2).pack(pady=10)

    Button(frame, text="FairShare2", highlightbackground="light blue", fg="black", 
           command=app2.load_ui, font=("Helvetica", 14, "bold"), width=10, height=2).pack(pady=10)

root = Tk()
root.title("FairShare App")
root.geometry("700x600")
root.config(bg="black")

frame = Frame(root, bg="black")
frame.pack(expand=True)

home_Page()
root.mainloop()