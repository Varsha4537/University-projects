#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <ctype.h>

#define MAX_ENV_VARIABLES 15
#define MAX_ENV_NAME_LENGTH 17
#define MAX_ENV_VALUE_LENGTH 241
#define MAX_COMMANDS_IN_SEQUENCE 10  // Maximum number of commands in a sequence

struct EnvironmentVariable {
    char name[MAX_ENV_NAME_LENGTH];
    char value[MAX_ENV_VALUE_LENGTH];
};

struct EnvironmentVariable environment[MAX_ENV_VARIABLES];
int env_count = 0;
int last_exit_status = 0;

void set_environment_variable(const char *name, const char *value) {
    if (env_count >= MAX_ENV_VARIABLES) {
        fprintf(stderr, "Error: Maximum number of environment variables reached.\n");
        return;
    }

    if (strlen(name) >= MAX_ENV_NAME_LENGTH || strlen(value) >= MAX_ENV_VALUE_LENGTH) {
        fprintf(stderr, "Error: Environment variable name or value exceeds length limits.\n");
        return;
    }

    strncpy(environment[env_count].name, name, MAX_ENV_NAME_LENGTH - 1);
    strncpy(environment[env_count].value, value, MAX_ENV_VALUE_LENGTH - 1);
    environment[env_count].name[MAX_ENV_NAME_LENGTH - 1] = '\0';
    environment[env_count].value[MAX_ENV_VALUE_LENGTH - 1] = '\0';

    env_count++;
}

char *get_env_variable(char *name) {
    for (int i = 0; i < env_count; i++) {
        if (strcmp(environment[i].name, name) == 0) {
            return environment[i].value;
        }
    }
    return NULL;
}

char *trim(char *str) {
    char *end;
    while (isspace(*str)) {
        str++;
    }
    if (*str == 0) {
        return str;
    }
    end = str + strlen(str) - 1;
    while (end > str && isspace(*end)) {
        end--;
    }
    *(end + 1) = '\0';
    return str;
}

int parse_time_interval(char *command) {
    int interval = -1;
    if (command[strlen(command) - 1] == '#') {
        command[strlen(command) - 1] = '\0';
        sscanf(command, "%*s %d", &interval);
    }
    return interval;
}

void execute_command(char *command) {
    char *args[64];
    char *token = strtok(command, " ");
    int i = 0;
    while (token != NULL) {
        args[i++] = token;
        token = strtok(NULL, " ");
    }
    args[i] = NULL;

    int input_redirect = 0; // Flag to track input redirection
    int output_redirect = 0; // Flag to track output redirection
    char *output_file = NULL;

    for (int j = 0; j < i; j++) {
        if (strcmp(args[j], "<") == 0) {
            input_redirect = 1;
            args[j] = NULL; // Remove "<" from arguments
        } else if (strcmp(args[j], ">") == 0) {
            output_redirect = 1;
            output_file = args[j + 1];
            args[j] = NULL; // Remove ">" from arguments
        }
    }

    pid_t pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        if (input_redirect) {
            int fd = open(args[i - 1], O_RDONLY);
            if (fd == -1) {
                perror("open");
                exit(EXIT_FAILURE);
            }
            if (dup2(fd, STDIN_FILENO) == -1) {
                perror("dup2");
                exit(EXIT_FAILURE);
            }
            close(fd);
        }
        if (output_redirect) {
            int fd = open(output_file, O_WRONLY | O_CREAT | O_TRUNC, 0666);
            if (fd == -1) {
                perror("open");
                exit(EXIT_FAILURE);
            }
            if (dup2(fd, STDOUT_FILENO) == -1) {
                perror("dup2");
                exit(EXIT_FAILURE);
            }
            close(fd);
        }
        execvp(args[0], args);
        perror("execvp");
        exit(EXIT_FAILURE);
    } else {
        int return_val;
        waitpid(pid, &return_val, 0);
        if (strcmp(args[0], "flash") != 0) {
            printf("Return value of '%s': %d\n", args[0], WEXITSTATUS(return_val));
            char return_val_str[32];
            snprintf(return_val_str, sizeof(return_val_str), "%d", WEXITSTATUS(return_val));
            set_environment_variable("?", return_val_str); // Update the return value in environment
            last_exit_status = WEXITSTATUS(return_val); // Update the last exit status
        }
    }
}

void execute_sequence(char *sequence) {
    char *commands[MAX_COMMANDS_IN_SEQUENCE];
    int num_commands = 0;

    char *token = strtok(sequence, ",");
    while (token != NULL && num_commands < MAX_COMMANDS_IN_SEQUENCE) {
        trim(token);
        commands[num_commands++] = token;
        token = strtok(NULL, ",");
    }

    for (int i = 0; i < num_commands; i++) {
        execute_command(commands[i]);
    }
}

int main() {
    char input[1024];
    while (1) {
        printf("flash> ");
        fgets(input, sizeof(input), stdin);
        char *pos;
        if ((pos = strchr(input, '\n')) != NULL) {
            *pos = '\0'; // Remove newline character
        }
        trim(input);

        if (strcmp(input, "exit") == 0) {
            break;
        }

        if (strncmp(input, "set", 3) == 0) {
            char name[MAX_ENV_NAME_LENGTH];
            char value[MAX_ENV_VALUE_LENGTH];
            if (sscanf(input, "set %16s = \"%240[^\"]\"", name, value) == 2) {
                set_environment_variable(name, trim(value));
                printf("Environment variable set.\n");
                continue;
            } else {
                puts("Invalid set command.");
                continue;
            }
        }

        if (strncmp(input, "get", 3) == 0) {
            char name[MAX_ENV_NAME_LENGTH];
            if (sscanf(input, "get %16s", name) == 1) {
                char *val = get_env_variable(name);
                if (val != NULL) {
                    puts(val);
                } else {
                    puts("Environment variable not found.");
                }
                continue;
            } else {
                puts("Invalid get command.");
                continue;
            }
        }

        int background = 0;
        if (input[strlen(input) - 1] == '#') {
            background = 1;
            input[strlen(input) - 1] = '\0'; // Remove the "#" character
        }

        char *pipe_symbol = strstr(input, "|");
        if (pipe_symbol != NULL) {
            char *command1 = strtok(input, "|");
            char *command2 = strtok(NULL, "|");
            if (command1 != NULL && command2 != NULL) {
                trim(command1);
                trim(command2);

                int pipe_fd[2];
                if (pipe(pipe_fd) == -1) {
                    perror("pipe");
                    exit(EXIT_FAILURE);
                }

                pid_t pid1 = fork();
                if (pid1 == -1) {
                    perror("fork");
                    exit(EXIT_FAILURE);
                } else if (pid1 == 0) {
                    close(pipe_fd[0]);
                    dup2(pipe_fd[1], STDOUT_FILENO);
                    close(pipe_fd[1]);
                    execute_command(command1);
                    exit(EXIT_SUCCESS);
                } else {
                    pid_t pid2 = fork();
                    if (pid2 == -1) {
                        perror("fork");
                        exit(EXIT_FAILURE);
                    } else if (pid2 == 0) {
                        close(pipe_fd[1]);
                        dup2(pipe_fd[0], STDIN_FILENO);
                        close(pipe_fd[0]);
                        execute_command(command2);
                        exit(EXIT_SUCCESS);
                    } else {
                        close(pipe_fd[0]);
                        close(pipe_fd[1]);
                        waitpid(pid1, NULL, 0);
                        waitpid(pid2, NULL, 0);
                    }
                }
                continue;
            } else {
                puts("Invalid command with pipe symbol.");
                continue;
            }
        }

        int interval = parse_time_interval(input);
        if (interval > 0) {
            printf("Waiting for %d seconds...\n", interval);
            sleep(interval);
        }

        if (background) {
            pid_t pid = fork();
            if (pid == -1) {
                perror("fork");
                exit(EXIT_FAILURE);
            } else if (pid == 0) {
                execute_command(input);
                exit(EXIT_SUCCESS);
            } else {
                printf("Background process started with PID %d\n", pid);
            }
        } else {
            execute_sequence(input);
        }
    }

    return 0;
}






