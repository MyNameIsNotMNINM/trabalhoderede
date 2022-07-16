#import libraries
import re
import os
import argparse
import csv

# error messages
INVALID_IP_MSG = "Error: Invalid IP address.\n%s is not a correct IP address."
REPEATED_SERVER_MSG = "Error: %s is already a File Server."
FILE_NOT_FOUND_MSG = "Error: Configuration file does not exist. Run ssoftp --setup"
SERVER_NOT_FOUND_MSG = "Error: File Server does not exist"

#path of configuration file
PATH_CONF = "config.json"


def get_arguments():
    # create parser object
    parser = argparse.ArgumentParser(description = "Manage the SOFTP Core Server")

    parser.add_argument("action", nargs="?")
    parser.add_argument("address", action = 'store',
                        help = "Core server address")
    parser.add_argument("-d", "--directory", action = 'store',
                        help = "choose file output directory")
    parser.add_argument("-f", "--file", action = 'store',
                        help = "file path")
    parser.add_argument('-r', '--redundancy', action= 'store',
                        help = 'N of redundancies')
    parser.add_argument("-p", "--port", action = 'store',
                        help = "Starts server with the selected port.") 
    args = parser.parse_args()
    return args