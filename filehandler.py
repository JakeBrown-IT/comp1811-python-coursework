"""
Author: Jake Brown
ID: 001239595-1
Purpose: This file contains the FileHandler class for my coursework project. It handles anything to do with the network
         file to take strain off of the main program and separate it out into readable sections.
"""


import os.path


class FileHandler:
    def __init__(self):
        self.__filename = self.__set_filename()
        self.__file_contents = self.__set_file_contents()

    @staticmethod
    def __set_filename():
        """
        Method gets filename from user
        :return: filename acquired from user
        """
        # while the condition is false
        while True:
            # get filename from the user as type string
            f_name = str(input("Enter a filename for network data -> "))
            # set all characters to lowercase for input sanitation
            f_name = f_name.lower()
            # check if input is equal to 'n' for program termination
            if f_name != 'n':
                # if input is not equal to 'n' then check if the filename exists in the current directory
                if os.path.exists(f_name):
                    # return filename
                    return f_name
                # if filename doesn't exist then
                else:
                    # display error message to user and jump to next loop iteration
                    print("Error: File '{}' does not exist.\nPlease enter a valid filename.".format(f_name))
            # if input is equal to 'n' then
            else:
                # display exiting program message
                print("Exiting program.")
                # terminate program
                quit()

    def __set_file_contents(self):
        """
        Method opens file and reads each line into a list
        :return: contents of file in list format
        """
        file_contents = []
        # open the file in read mode
        with open(self.__filename, 'r') as network_file:
            # for each line in the network file
            for line in network_file:
                # strip the line of its newline character
                # split the line at each space
                # append the line to the file_contents attribute
                file_contents.append(line.rstrip().split())
        # return file_contents to main program to update class attribute
        return file_contents

    def get_file_contents(self):
        """
        Getter for file_contents
        :return: file_contents
        """
        return self.__file_contents
