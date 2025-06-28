import socket
import threading
import pickle
import logging
import time

class FairShareFunctions:
    def __init__(self, host='127.0.0.1', port=1234):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started on {host}:{port}")

        self.user_name = []  
        self.passwords = []
        self.expense_tracker = []  
        self.i = 0  
        self.num_users = 0
        self.file = None

        self.lock = threading.Lock()  # Lock for thread safety
        self.shutdown_event = threading.Event()
        self.threads = []  # Track active threads

        threading.Thread(target=self.start_listening, daemon=True).start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()

    def start_listening(self):
        while not self.shutdown_event.is_set():
            try:
                client, addr = self.server.accept()
                print(f"Connection from {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client,))
                client_thread.start()
                self.threads.append(client_thread)
            except Exception as e:
                logging.error(f"Server error: {e}")

    def handle_client(self, client):
        try:
            while True:
                data = client.recv(1024).decode().strip()
                if not data:
                    print("Client disconnected.")
                    break
                try:
                    request_parts = data.split()
                    action = request_parts[0]
                    response = self.process_request(action, request_parts)
                    if isinstance(response, str):
                        client.send(response.encode())
                    else:
                        client.sendall(pickle.dumps(response))
                except Exception as e:
                    logging.error(f"Processing error: {e}")
                    client.send("ERROR Invalid request format".encode())
        except ConnectionResetError:
            print("Client forcefully disconnected.")
        finally:
            client.close()

    def shutdown(self):
        print("Shutting down server...")
        self.shutdown_event.set()
        for thread in self.threads:
            thread.join()
        self.server.close()
        print("Server shut down successfully.")

    def process_request(self, action, request_parts):
        with self.lock:  # Ensure thread safety
            if action == "open_file":
                self.open_file()
                return "SUCCESS File opened"

            elif action == "close_file":
                self.close_file()
                return "SUCCESS File closed"

            elif action == "login":
                if len(request_parts) < 3:
                    return "ERROR Invalid login request format"
                username, password = request_parts[1], request_parts[2]
                if username in self.user_name and self.passwords[self.user_name.index(username)] == password:
                    return "SUCCESS Login successful"
                return "ERROR Invalid username or password"

            elif action == "register":
                return self.register(request_parts[1], request_parts[2])

            elif action == "expense":
                return self.expense(request_parts[1], float(request_parts[2]))

            elif action == "report_user":
                return "\n".join(self.report_user(request_parts[1]))

            elif action == "report":
                return "\n".join(self.report())

            elif action == "i":
                return str(self.i)

            elif action == "user_name":
                return self.user_name

            elif action == "passwords":
                return self.passwords

            elif action == "expense_tracker":
                return self.expense_tracker

            return "ERROR Invalid action."

    def open_file(self):
        try:
            with open("DB.text", "r+") as self.file:
                lines = self.file.readlines()
                if not lines:
                    self.i = 0
                    self.user_name = []
                    self.passwords = []
                    self.num_users = 0
                    self.expense_tracker = []
                    return

                self.i = int(lines[0].strip()) if lines else 0
                self.user_name = lines[1].strip().split() if len(lines) > 1 else []
                self.passwords = lines[2].strip().split() if len(lines) > 2 else []
                self.num_users = len(self.user_name)

                self.expense_tracker = [[0.0] * self.num_users for _ in range(self.i)]

                for row_idx, line in enumerate(lines[3:self.i + 3]):
                    values = list(map(float, line.split()))
                    for col_idx, value in enumerate(values):
                        if col_idx < self.num_users:
                            self.expense_tracker[row_idx][col_idx] = value

        except FileNotFoundError:
            with open("DB.text", "w+") as self.file:
                self.i = 0
                self.user_name = []
                self.passwords = []
                self.num_users = 0
                self.expense_tracker = []

    def close_file(self):
        if not self.file:
            return

        with open("DB.text", "w") as self.file:
            self.file.write(f"{self.i}\n")
            self.file.write(" ".join(self.user_name) + "\n")
            self.file.write(" ".join(self.passwords) + "\n")

            for row in self.expense_tracker[:self.i]:
                self.file.write(" ".join(map(str, row)) + "\n")

    def register(self, user_name, password):
        if user_name in self.user_name:
            return f"ERROR User {user_name} already registered"
        self.user_name.append(user_name)
        self.passwords.append(password)
        self.num_users += 1

        for row in self.expense_tracker:
            row.append(0.0)

        if not self.expense_tracker:
            self.expense_tracker.append([0.0] * self.num_users)

        return "SUCCESS"

    def expense(self, user_name, amount):
        if user_name not in self.user_name:
            return f"ERROR User {user_name} not registered"

        column = self.user_name.index(user_name)

        while len(self.expense_tracker) <= self.i:
            self.expense_tracker.append([0.0] * self.num_users)

        self.expense_tracker[self.i][column] = amount
        self.i += 1

        return f"SUCCESS Logged expense of {amount} for {user_name}"

    def report_user(self, user_name):
        if user_name not in self.user_name:
            return [f"ERROR User {user_name} not registered"]

        column = self.user_name.index(user_name)
        user_total = sum(self.expense_tracker[row][column] for row in range(self.i))
        total_expense = sum(sum(row) for row in self.expense_tracker)
        average = total_expense / self.num_users if self.num_users > 0 else 0
        output = [f"User {user_name}: Total Expense = {user_total}, Balance = {average - user_total}"]
        return output

    def report(self):
        total_expense = sum(sum(row) for row in self.expense_tracker)
        average = total_expense / self.num_users if self.num_users > 0 else 0
        output = [f"Average Expense per User: {average}"]

        for idx, user in enumerate(self.user_name):
            user_total = sum(self.expense_tracker[row][idx] for row in range(self.i))
            output.append(f"{user} - Balance: {average - user_total}")

        return output


if __name__ == "__main__":
    FairShareFunctions()