CC = gcc
CFLAGS = -Wall -Wextra

TARGET = flash_shell

all: $(TARGET)

$(TARGET): flash_shell.o
	$(CC) $(CFLAGS) -o $(TARGET) flash_shell.o

flash_shell.o: flash_shell.c
	$(CC) $(CFLAGS) -c flash_shell.c

clean:
	rm -f $(TARGET) *.o