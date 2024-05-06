#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 4096

void printUsage() {
    fprintf(stderr, "Usage: flame_cp -i <source file pathname> -o <destination file pathname>\n");
}

int main(int argc, char *argv[]) {
    char *inputPath = NULL;
    char *outputPath = NULL;

    // Check if the correct number of arguments are provided
    if (argc != 5) {
        printUsage();
        return 1; // Exit code for incorrect usage
    }

    // Parse command line arguments
    for (int i = 1; i < argc; i += 2) {
        if (strcmp(argv[i], "-i") == 0) {
            inputPath = argv[i + 1];
        } else if (strcmp(argv[i], "-o") == 0) {
            outputPath = argv[i + 1];
        } else {
            printUsage();
            return 1; // Exit code for incorrect usage
        }
    }

    // Check if both input and output paths are provided
    if (!inputPath || !outputPath) {
        printUsage();
        return 1; // Exit code for incorrect usage
    }

    FILE *inputFile;
    FILE *outputFile;

    // Check if input should be read from standard input
    if (strcmp(inputPath, "-") == 0) {
        inputFile = stdin;
    } else {
        inputFile = fopen(inputPath, "rb");
        if (!inputFile) {
            return 2; // Exit code for input file not found
        }
    }

    // Check if output should be written to standard output
    if (strcmp(outputPath, "-") == 0) {
        outputFile = stdout;
    } else {
        outputFile = fopen(outputPath, "wb");
        if (!outputFile) {
            if (inputFile != stdin) {
                fclose(inputFile);
            }
            return 3; // Exit code for unable to create output file
        }
    }

    // Copy content from input to output
    char buffer[BUFFER_SIZE];
    size_t bytesRead;

    while ((bytesRead = fread(buffer, 1, BUFFER_SIZE, inputFile)) > 0) {
        fwrite(buffer, 1, bytesRead, outputFile);
    }

    // Close files
    if (inputFile != stdin) {
        fclose(inputFile);
    }

    if (outputFile != stdout) {
        fclose(outputFile);
    }

    return 0; // Exit code for successful execution
}

