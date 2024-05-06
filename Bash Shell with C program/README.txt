FLAme-SHell: Flash Shell

Course Information
Course: Systems Programming
Course Code: CSIT206
Professor: Abhijat Vichare

Team Members
Sneh Pahuja
Varsha Gunturu
Vineesha Vuppala

******************************************************************************************************************************************************************

ASSIGNMENT OVERVIEW

The FLAme-SHell project implements a simple shell in C, showcasing basic inter-process communication using pipes. It executes two commands concurrently, demonstrating bidirectional data flow between processes.

******************************************************************************************************************************************************************

OBJECTIVES

Implement inter-process communication using pipes.
Execute two commands concurrently.
Redirect input/output streams.
Support environment variables.
Demonstrate the functionality of pipes in a Unix-like environment.

******************************************************************************************************************************************************************

FEATURES

Simple Command Line: Execute a single program with its command-line options.
Background Command Line: Run a command in the background using the "#" character.
Sequence: Execute multiple commands separated by commas (,).
Pipeline: Pipe data from one command to another using "--".
Redirection: Redirect standard input/output using "<" and ">".
Environment Variables: Support for up to 15 environment variables, including setting and getting values.
Program Functionality
Takes two commands as input arguments.
Executes commands concurrently, with output serving as input to the next command.
Demonstrates bidirectional communication between processes using pipes.

******************************************************************************************************************************************************************

TECHNICAL DETAILS

Libraries: stdio.h, stdlib.h, unistd.h, sys/wait.h, string.h
System Calls: fork(), pipe(), dup2(), execlp()
Error Handling: Graceful error messages, exit codes
Concurrency: Concurrent execution of processes using fork()
Synchronisation: Unidirectional data flow, waitpid() for process synchronisation

******************************************************************************************************************************************************************

BUILDING AND RUNNING 

Compile the program using the provided Makefile:
Copy code
gcc flash.c -o flash
Run the program with desired commands:
bash
Copy code
./flash
pwd, date
ls | grep .c
get ?
cat < 'filename'
cat < 'filename' > 'filename'
set 'env_variable' = "input"
get 'env_variable'
ls -l
ls -l > 'filename'
wc -l < 'filename'
sleep 'seconds'
sleep 'seconds' #
ls -l, cat file.txt, echo "Hello, world!"
set INVALID_COMMAND
get ?
exit

******************************************************************************************************************************************************************

DESIGN CHOICES

Error Handling: Centralised error handling with readable messages and graceful exit.
Exit Codes: Standard exit codes for identifying success/failure of system calls and program execution.
Modular Design: Modular approach for better code readability and maintenance.
Concurrency: Utilisation of fork() for concurrent process execution.
Redirection: Implementation of input/output redirection using dup2().

******************************************************************************************************************************************************************
FINAL SUBMISSION

Source File: flash.c
Executable: flash
Makefile: Included
README: Provided
