# NOTE
I compiled this code on mac and have editited the mini_curl.py so that I may run bank.py using it. Below is the sample terminal inputs I used.

# GOING TO INDEX PAGE FIRST
Enter URL (or 'exit' to quit): http://localhost:8080/index.py
Method [GET/POST] (default: GET): GET

# SIGNUP
Enter URL (or 'exit' to quit): http://localhost:8081/signup.py?return_to=http://localhost:8080/cgi-bin/dashboard.py
Method [GET/POST] (default: GET): POST
Enter POST data key=value (or blank to finish): username=Gun
Enter POST data key=value (or blank to finish): password=1234
Enter POST data key=value (or blank to finish):


# LOGIN
🌐 === Mini Curl ===
Enter URL (or 'exit' to quit): http://localhost:8081/login.py?return_to=http://localhost:8080/cgi-bin/dashboard.py
Method [GET/POST] (default: GET): POST
Enter POST data key=value (or blank to finish): username=Gun
Enter POST data key=value (or blank to finish): password=1234
Enter POST data key=value (or blank to finish):

# ADD MONEY
🌐 === Mini Curl ===
Enter URL (or 'exit' to quit): http://localhost:8080/add.py
Method [GET/POST] (default: GET): POST
Enter POST data key=value (or blank to finish): amount=100
Enter POST data key=value (or blank to finish):

# REMOVE MONEY
🌐 === Mini Curl ===
Enter URL (or 'exit' to quit): http://localhost:8080/remove.py
Method [GET/POST] (default: GET): POST
Enter POST data key=value (or blank to finish): amount=50
Enter POST data key=value (or blank to finish):

# LOGOUT
🌐 === Mini Curl ===
Enter URL (or 'exit' to quit): http://localhost:8081/logout.py?return_to=http://localhost:8080/index.py
Method [GET/POST] (default: GET): GET
