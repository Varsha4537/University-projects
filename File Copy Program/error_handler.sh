#!/bin/bash

./flame_cp -i "$1" -o "$2"
err_code=$?

if [ $err_code -ne 0 ]; then
    case $err_code in
        1) echo "Invalid usage.";;
        2) echo "Failed to open source file.";;
        3) echo "Failed to open destination file.";;
        4) echo "Failed to write to destination file.";;
        5) echo "Failed to read from source file.";;
        *) echo "Unknown error.";;
    esac
    exit $err_code
fi
