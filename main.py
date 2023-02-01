"""
Author: Jake Brown
ID: 001239595-1
Purpose: Main program file for the coursework project controlling the flow of the program.
"""

# import all custom classes
import filehandler as fh
import displayhandler as dh
import network as nw


print("Social Network Simulator")


# main program function
def main():
    # instantiate all objects
    file_handler = fh.FileHandler()
    display_handler = dh.DisplayHandler()
    network = nw.Network(file_handler.get_file_contents())

    def eval_yesno(char):
        """
        Returns true if user entered 'y' and returns false if user entered 'n'. If neither were entered, then the method
        displays an error message and prompts user for correct input.
        :param: char: takes in char from main() for evaluation
        :return: returns true if 'y' entered, false if 'n' entered
        """
        while True:  # loop until break statement
            if char == 'n':  # if user entered n
                return False  # return false so next statement in main() is not executed
            elif char == 'y':  # if user entered y
                return True  # return true so next statement in main() is executed
            else:  # if neither n nor y were entered
                print("Error: Invalid Input: {}! Please enter either 'y' or 'n'.".format(char))  # display error
                char = str(input("-> "))  # prompt for new input to evaluate

    def eval_u_name(usr_u_name):
        """
        Returns true if u_name is in network structure keys, displays error message and prompts for correct input if
        otherwise.
        :param: u_name: username taken in from main() to evaluate
        :return: returns true when u_name is correct
        """
        while True:  # loop until break statement
            if usr_u_name in network.get_network_structure():  # if u_name is in the network structure keys
                return True, usr_u_name  # return true because username exists
            else:  # if u_name is not in network structure keys
                # display error message
                print("Error: Invalid Username: {}! Please enter a Username that exists in the Network."
                      .format(usr_u_name))
                usr_u_name = str(input("-> "))  # prompt for new input to evaluate

    # if network data initialisation failed, meaning the checksum was invalid and the network data could not be
    # extracted successfully
    if network.get_network_structure() is None:
        print("Error: File Consistency Checksum cannot be validated and the Network data cannot be extracted.")
        outcome = eval_yesno(str(input("Try another Social Network? [y/n] -> ").lower()))
        if outcome:  # if the outcome is true, restart program
            main()
        else:
            print("Exiting program.")
            quit()  # quit program

    outcome = network.validate_network_structure()  # validate network structure consistency
    if not outcome:  # if outcome is false
        outcome = eval_yesno(str(input("Error: Inconsistent Network Structure detected. No actions can be performed"
                                       " apart from viewing.\nStill View the Social Network? [y/n] -> ").lower()))
        if outcome:
            display_handler.pretty_print(network.get_network_structure())  # pretty print network structure
            outcome = eval_yesno(str(input("Try another Social Network? [y/n] -> ").lower()))
            if outcome:
                main()
            else:
                print("Exiting program.")
                quit()

    # pretty print social network structure
    outcome = eval_yesno(str(input("View the Social Network? [y/n] -> ").lower()))  # parse input to eval method
    if outcome:  # if outcome is true
        display_handler.pretty_print(network.get_network_structure())  # pretty print network structure

    # common friends
    outcome = eval_yesno(str(input("Show all common friends in the Social Network? [y/n] -> ").lower()))
    if outcome:  # if outcome is true
        # pretty print common friends structure
        display_handler.pretty_print(network.get_network_common_friends_structure())

    # recommended friends
    outcome = eval_yesno(str(input("Show recommended friends for a user? [y/n] -> ").lower()))
    if outcome:  # if outcome is true
        u_name = str(input("Enter the name of a user -> "))  # get input as string
        outcome, u_name = eval_u_name(u_name)  # call eval and parse u_name for evaluation
        if outcome:  # if outcome is true
            print("Recommended friend for {} is {}.".format(u_name, network.recommend_friend(u_name)))

    # friend count
    outcome = eval_yesno(str(input("Show friend count for a user? [y/n] -> ").lower()))
    if outcome:  # if outcome is true
        u_name = str(input("Enter the name of a user -> "))
        outcome, u_name = eval_u_name(u_name)  # call eval and parse u_name for evaluation
        if outcome:  # if outcome is true
            friends_count = network.friend_count(u_name)
            if friends_count == 1:
                print("User {} has 1 friend.".format(u_name))
            else:
                print("User {} has {} friends.".format(u_name, friends_count))

    # least/no friends
    outcome = eval_yesno(str(input("Show users with least/no friends? [y/n] -> ")))
    if outcome:
        display_handler.pretty_print(network.least_friends())

    # friends
    outcome = eval_yesno(str(input("Show all friends for a user? [y/n] -> ").lower()))
    if outcome:
        u_name = str(input("Enter the name of a user -> "))
        outcome, u_name = eval_u_name(u_name)
        if outcome:
            friends = network.user_friends(u_name)
            if len(friends) == 0:
                print("User {} does not have any friends.".format(u_name))
            elif len(friends) == 1:
                print("User {} is friends with {}.".format(u_name, *friends))
            else:
                print("User {} is friends with {} and {}.".format(u_name, ", ".join(friends[:-1]), friends[-1]))

    # indirect friends
    outcome = eval_yesno(str(input("Show indirect friends for a user? [y/n] -> ")))
    if outcome:
        u_name = str(input("Enter the name of a user -> "))
        outcome, u_name = eval_u_name(u_name)
        if outcome:
            display_handler.pretty_print(network.indirect_friends(u_name))

    outcome = eval_yesno(str(input("Try another Social Network? [y/n] -> ")))
    if outcome:
        main()  # call main again to restart program

    else:
        print("Exiting Program.")


# call main method
main()
