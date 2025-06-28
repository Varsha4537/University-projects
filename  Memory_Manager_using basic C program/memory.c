#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MEMORY_SIZE 100//just good practice

char memory[MEMORY_SIZE];//using array for easier representation of memory and ease in implementing functions to manipulate the memory

void initialize_array(void){//basic initializing of the memory, setting all blocks to f = free
    for (int i = 0; i < MEMORY_SIZE; i++) {
        memory[i] = 'f';
    }
}

int load(void);
int save(void);
void print_map(void);
void compact(void);
int Free_1(int start_address, int size);
int Free_2(int start_address, int size);//not using it
int alloc(int n);

int main(void){
    initialize_array();//initializing array before load, in case the user doesn't want to work on the old memory and wants to work on fresh free memory
    char input[20];
    char command[20];
    int value;
    int value1 = 0;
    printf("Input Suntax:\n load \n print_map \n alloc <size> \n free <starting position> <no of blocks> : for freeing memory partially allocated\n compact \n save \n exit \n");
    while(strcmp(input, "exit") != 0){//a whil loop that keeps taking user input until the exit command in given
        printf("\nUser Input\n");
        fgets(input, sizeof(input), stdin);//getting and storing the input
        input[strcspn(input, "\n")] = '\0'; // Remove the newline character from the input
        
        if(strcmp(input, "load") == 0){//comparing the input to known sytax to run the particular function
            printf("%d \n",load());
        }
        else if (strcmp(input, "save") == 0){
            printf("%d \n",save());
        }
        else if (strcmp(input, "compact") == 0){
            compact();
        }
        else if (strcmp(input, "print_map") == 0){
            print_map();
        }
        else if (sscanf(input, "%s %d", command, &value) == 2){//when the sytax has a string and integer that is needed in the function, so storing it seperately for comparing the sytax and for the integer input required for the particular function to be run
            if (strcmp(command, "alloc") == 0){
                printf("%d",alloc(value));
            }
            else if (sscanf(input, "%s %d %d", command, &value, &value1) == 3){//when there is one string and two integer input that is required to call the particular function
                if(strcmp(command, "free") == 0){
                    Free_1(value, value1);}
            }
        }
//the below code has not been used as it didn't run as expected
//        else if (fscanf(stdin, "%s %d %d", command, &value, &value1) == 3){
//            printf("Command: %s, Value: %d, Value1: %d\n", command, value, value1);
//            if (strcmp(command, "Free") == 0){
//                Free(value, value1);}
//        }
        else if (strcmp(input, "exit") == 0){
            //exit, this is put here so that the error else condition for incorrect input is not executed
        }
        else {
            perror("Incorrect Input try again\n");// when the user input anything else other than the specified syntax
        }
    }
    return 0;
}


int load(void){
    FILE *storage;
    storage = fopen("./memory_state.txt", "r");
    if (storage==NULL){
        perror("Not able to open the file");//error message
        return 1;
    }
    int i=0;
    char ch =getc(storage);//reading the first character of the file
    while(ch!=EOF){//condition to load the character into the arry till the end of the file
        memory[i]=ch;
        i+=1;
        ch=getc(storage);
    }
    if(fclose(storage)!=0){
        perror("Error clossing File");//error
        return 1;
    }
    return 0;
}

void print_map(void){ 
    printf("\n");
    for (int i=0;i<100;i++){//printing all 100 indexes of the memory array
        printf("%c ",memory[i]);
        if((i+1)%10==0){
            printf("\n");//having 10 * 10 Grid for easier understanding and display of the array
        }
    }
    printf("\n");
}

int save(void){
    FILE *storage1;//variable to store file
    char ch;//character to temporarily store array values
    storage1 = fopen("./memory_state.txt", "w");//opening file with writing capabilities
    if (storage1==NULL){
        perror("Not able to open the file");//error message
        return 1;
    }
    //writing the array values to the file
    for (int i=0;i<100;i++){
        ch=memory[i];
        putc(ch,storage1);//writing to the file
    }
    if(fclose(storage1)!=0){//closing the file
        perror("Error clossing File");//error in closing the file
        return 1;
    }
    return 0;
}

//  partial free handling - FINAL OPTION
int Free_1(int start_address, int size) {
    if (start_address < 0 || start_address >= MEMORY_SIZE || start_address + size > MEMORY_SIZE) {
            perror("Error: invalid memory address or size.\n");
            return 1;
        }
    
    printf("Freeing the remaining memory\n");
        for (int i = start_address; i < start_address + size; i++) {
            memory[i] = 'f';
        }

        printf("Memory successfully freed from address %d to %d.\n", start_address, start_address + size - 1);
    return 0;
}


int Free_2(int start_address, int size) {
    if (start_address < 0 || start_address >= MEMORY_SIZE || start_address + size > MEMORY_SIZE) {//when incorrect memory size is specified
        printf("error: invalid memory address or size.\n");
        return 1;
    }

    for (int i = start_address; i < start_address + size; i++) {
        if (memory[i] == 'f') {
            printf("error: not all blocks are allocated, so free failed.\n");//to make sure that all blocks from start adress is allocted and not fragmented
            return 1;
        }
    }

    for (int i = start_address; i < start_address + size; i++) {//after confirming that the blocks from the starting adress to specified size address is allocated, only then the freeing is done.
        memory[i] = 'f';
    }

    printf("memory successfully freed from address %d.\n", start_address);
    return 0;
}

//defragmenting
void compact(void)
{
    int start = 0, end = 99;
    while (start < end)
    {
        if (memory[start] == 'f' && memory[end] == 'a') // swap free at the left side with allocated on the right
        {
            memory[start] = 'a';
            memory[end] = 'f';
            start++;
            end--;
        }
        if (memory[start] == 'a') // continue if allocated are on left
        {
            start++;
        }
        if (memory[end] == 'f') // continue if free are on right
        {
            end--;
        }
    }
}

int alloc(int size)  { //FIRSTFIT
    int start = -1; // To store starting index of the block
    int count = 0;  // To count contiguous free blocks

    for (int i = 0; i < MEMORY_SIZE; i++) { //Finds first large enough of contiguous blocks to allocate 
        if (memory[i] == 'f') {
            count++;
            if (count == size) {
                start = i - size + 1;
                break;
            }
        } else {
            count = 0; // Reset count if a used block is found
        }
    }

    if (start != -1) { // Allocation successful
        for (int i = start; i < start + size; i++) {
            memory[i] = 'a'; // Mark blocks as allocated
        }
        printf("Memory allocated: Starting block = %d, Size = %d\n", start, size);
        return 0; // Success
    } else { // Allocation failed
        perror("Error: Unable to allocate blocks. Insufficient contiguous memory.\n");
        return 1; // Failure
    }
}