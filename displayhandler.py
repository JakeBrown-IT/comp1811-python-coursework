"""
Author: Jake Brown
ID: 001239595-1
Purpose: This file contains the DisplayHandler class for my coursework project. It handles the display of any data
         structures to reduce strain on the main program.
"""


class DisplayHandler:
    def __init__(self):
        pass

    @staticmethod
    def pretty_print(data_to_print):
        """
        Method checks type of data parsed then prints to console in 'pretty' (readable) format
        :param: data_to_print: data parsed in to print to console
        :return: none
        """

        alignment = 0  # preset alignment

        if type(data_to_print) == dict:  # if data type is dictionary
            for key in data_to_print:  # iterate over dictionary
                if len(key) > alignment:  # if length of key is greater than current alignment number
                    alignment = len(key)  # set alignment as length of key

            for element in data_to_print:  # iterates over the data
                if not data_to_print[element]:  # if element is empty
                    print("{:>{align}} -> None".format(element, align=alignment))
                else:
                    # print the key, join the elements stored in the dictionary under the key, then prints them aligned
                    print("{:>{align}} -> {}"
                          .format(element, ", ".join(map(str, data_to_print[element])), align=alignment))

        elif type(data_to_print) == str:  # if data type is string
            print(data_to_print)  # normally print string to console
