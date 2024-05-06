#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <stdbool.h> // Include stdbool.h for bool type

#define MAX_FILENAME_LENGTH 256
#define MAX_TEXT_LENGTH 50
#define MAX_BYTES_TO_DISPLAY 50 // Define MAX_BYTES_TO_DISPLAY

void print_usage() {
    printf("Usage: my_fm [option] [filename]\n");
    printf("Options:\n");
    printf("  -c        Create a file or directory\n");
    printf("  -t TEXT   Create a text file and append given text\n");
    printf("  -b START  Create a binary file and append odd numbers\n");
    printf("  -p        Print the first 50 bytes of the file\n");
    printf("  -d        Delete the file or an empty directory\n");
    printf("  -r NEW    Rename the file or directory\n");
}

void append_text(FILE *file, const char *text) {
    fseek(file, 0, SEEK_END);
    fwrite(text, sizeof(char), strlen(text), file);
}

void append_odd_numbers(const char *filename, int start) {
    FILE *file = fopen(filename, "ab"); // "ab" mode for appending in binary format
    if (file == NULL) {
        perror("Error opening file");
        return;
    }
    if (start < 50) {//to make sure the odd numbers are from 50-200
        perror("Error low starting number");
        return;
    }
    if (start%2==0){start++;} //to convert even to odd number as start
    for (int i = start; i < 200; i += 2) {
        fwrite(&i, sizeof(int), 1, file);
    }

    fclose(file);
}

void display_first_50_bytes(const char *filename) {
    FILE *file = fopen(filename, "rb"); // "rb" mode for reading in binary format
        if (file == NULL) {
            perror("Error opening file");
            return;
        }

        printf("First %d bytes of file %s in decimal format:\n", MAX_BYTES_TO_DISPLAY, filename);

        // Read and print each byte
        int byte;
        while ((byte = fgetc(file)) != EOF) {
            if (byte != 0) {
                printf("%d ", byte); // Print each non-zero byte as a decimal number
            }
        }
        printf("\n");

        fclose(file);
}

void print_first_50_bytes(FILE *file) {
    rewind(file);
    char buffer[MAX_TEXT_LENGTH];
    fread(buffer, sizeof(char), MAX_TEXT_LENGTH, file);
    printf("First 50 bytes of the file:\n%s\n", buffer);
}

bool is_binary(const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        perror("Error opening file");
        return false;
    }

    int byte;
    while ((byte = fgetc(file)) != EOF) {
        if (byte == 0 || (byte >= 1 && byte <= 8) || (byte >= 14 && byte <= 31) || byte == 127) {
            fclose(file);
            return true; // Non-printable character found, likely binary
        }
    }

    fclose(file);
    return false; // No non-printable characters found, likely text
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        print_usage();
        return 1;
    }

    char *filename = argv[2];

    if (strcmp(argv[1], "-c") == 0) {
        mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH;
        if (argc >= 4 && strcmp(argv[3], "-t") == 0) {
            FILE *file = fopen(filename, "w+");
            if (file == NULL) {
                perror("Error creating text file");
                return 1;
            }
            if (argc >= 5) {
                append_text(file, argv[4]);
            }
            fclose(file);
            printf("Text file created: %s\n", filename);
        } else if (argc >= 4 && strcmp(argv[3], "-b") == 0) {
            FILE *file = fopen(filename, "wb+");
            if (file == NULL) {
                perror("Error creating binary file");
                return 1;
            }
            if (argc >= 5) {
                int start = atoi(argv[4]);
                append_odd_numbers(filename, start);
            }
            fclose(file);
            printf("Binary file created: %s\n", filename);
        } else {
            if (mkdir(filename, mode) == 0) {
                printf("Directory created: %s\n", filename);
            } else {
                printf("File created: %s\n", filename);
            }
        }
    } else if (strcmp(argv[1], "-p") == 0) {
        FILE *file = fopen(filename, "r");
        if (file == NULL) {
            perror("Error opening file");
            return 1;
        }
        if (is_binary(filename)) {
            display_first_50_bytes(filename);
            return 1;
        }
        print_first_50_bytes(file);
        fclose(file);
    } else if (strcmp(argv[1], "-d") == 0) {
        if (rmdir(filename) == 0) {
            printf("Directory deleted: %s\n", filename);
        } else if (unlink(filename) == 0) {
            printf("File deleted: %s\n", filename);
        } else {
            perror("Error deleting file or directory");
            return 1;
        }
    } else if (strcmp(argv[1], "-r") == 0) {
        if (rename(filename, argv[3]) == 0) {
            printf("File or directory renamed from %s to %s\n", filename, argv[3]);
        } else {
            perror("Error renaming file or directory");
            return 1;
        }
    } else {
        print_usage();
        return 1;
    }

    return 0;
}







