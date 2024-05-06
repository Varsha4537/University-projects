README FILE

my_fm.c  a c program that can implement basic system calls on files.

GROUP: Varsha Gunturu, Abhipsha Luitel

DEVICE: Mac Users 


DESCRIPTION
my_fm.c utilises the command line for creating directories, texts files and binary files. It can also display the contents of the file on terminal, rename the file or delete the file according to the command inputed by the user. my_fm is our executable file.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

TERMINAL/CONSOLE COMMANDS TO EXECUTE IN SEQUENCE & PURPOSE (Everything after the arrow explains what the command does)

gcc -Wall -o my_fm my_fm.c  --> to create the executable, NOTE: that the -Wall is necessary for the program to run

./my_fm -c <directory name>  --> to create the directory

./my_fm -c <text file name>.txt -t "TEXT TO DISPLAY"  --> to create the text file, NOTE: It is important to have the ".txt" extension and "-t" for the file file to be text. The text to display is optional for the user, but make sure to put the double quotes, otherwise the program will not execute

./my_fm -c <directory name>.bin -b <starting number>   --> to create the binary file, NOTE: It is important to have the ".bin" extension and "-b" for the file to be binary. The starting number should be between 50 and 200 exclusive, otherwise the program will create an empty binary file. You can use the same command again if you wish to rewrite the contents of a file. However note that if the previous data of the file will be overwritten. 

chmod +rx <directory name>    --> this command will be required if you want to manually open a directory, otherwise you will be denied permission to view or edit the directory

./my_fm -p <file name with extension>    -->this command will print the first 50 bytes of the file or directory mentioned

./my_fm -r <old directory name/old file name with extension> <new directory name/new file name with extension>    --> to rename a directory or a file, first specify the old name followed by the new name

./my_fm -d <directory/file name>   --> to delete a directory or a file. Note that a directory with a file inside or contents inside will not be deleted even if the command is given.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SAMPLE COMMANDS WE USED

gcc -Wall -o my_fm my_fm.c
./my_fm -c demo
./my_fm -c binary.bin -b 55
./my_fm -c file.txt -t "Hello, world!"
./my_fm -p file.txt 
./my_fm -p binary.bin
./my_fm -r file.txt first.txt
./my_fm -d first.txt
./my_fm -d binary.bin
./my_fm -d demo
./my_fm -d demo2         --> NOTE: A demo2 file with a text file is provided in the zip, this is to test that a directory with content or files in it cannot be deleted.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

FUNCTIONS USED IN THE C-CODE:

print_usage()
Prints the usage information and available options for the program.

append_text()
Appends the specified text to the end of a text file.

append_odd_numbers()
Creates a binary file and appends odd numbers starting from the specified value. Makes sure that the starting number is more than 50 and write odd numbers till 200. Note that if the starting number does not fall between 50 and 200, where both are exclusive, an empty binary file will be created.

display_first_50_bytes()
Prints the first 50 bytes of a file in decimal format. Used for printing the odd numbers from the binary file.

print_first_50_bytes(FILE *file)
Prints the first 50 bytes of the text file as a string.

is_binary()
Checks whether the file to print or output is a binary or a text file.

main()
The main function handles command-line arguments and executes the corresponding actions based on the provided options. An nested if else statement is used so that the user can navigate through the various options for simple manipulation of the file.



