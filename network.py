"""
Author: Jake Brown
ID: 001239595-1
Purpose: This file contains the SocialNetwork and Network classes for my coursework project. It is the main object focus
         of the program and handles everything to do with the networks.
"""


class SocialNetwork:
    def __init__(self, network_data):
        valid = self._validate_network_data(network_data)  # test network_data for consistency number
        if valid:  # if network_data has a consistent checksum, data is valid so proceed with initialisation
            self._network_data = network_data
            self._network_structure = self._generate_network_structure()
            self._network_common_friends_structure = self._generate_common_friends_structure()
        else:  # otherwise is network_data is not valid, don't initialise any attributes with their methods
            self._network_data = None
            self._network_structure = None
            self._network_common_friends_structure = None
            pass

    def _validate_network_data(self, network_data):
        raise NotImplementedError("Implement in non-abstract subclass to use this method.")

    def _generate_network_structure(self):
        raise NotImplementedError("Implement in non-abstract subclass to use this method.")

    def get_network_structure(self):
        raise NotImplementedError("Implement in non-abstract subclass to use this method.")

    def validate_network_structure(self):
        raise NotImplementedError("Implement in non-abstract subclass to use this method.")

    def _generate_common_friends_structure(self):
        raise NotImplementedError("Implement in non-abstract subclass to use this method.")

    def get_network_common_friends_structure(self):
        raise NotImplementedError("Implement in non-abstract subclass to use this method.")


class Network(SocialNetwork):
    def __init__(self, network_data):
        super().__init__(network_data)  # instantiate super class

    def _validate_network_data(self, network_data):
        """
        Returns evaluation of whether network_data checksum is consistent or not
        :param: network_data: network_data from filehandler
        :return: Boolean, True if consistent, False if inconsistent.
        """
        # network data file consistency checksum should be at the start of the file, if it is not, then the file format
        # is incorrect and the program cannot read the file accurately.
        checksum = "".join(network_data[0])  # get network checksum from first element in network_data
        try:
            checksum = int(checksum)  # try to caste checksum to integer
            users = []  # empty users list
            for value in network_data[1:]:  # iterate over values after first value in network_data
                for sub_value in value:  # iterate over sub_values in value
                    users.append(sub_value)  # append each sub value to users
            if len(set(users)) == checksum:  # convert users to set to remove duplicates and compare length to checksum
                return True  # if length equal to checksum, consistent checksum
            else:  # otherwise
                return False  # inconsistent checksum
        except ValueError:  # except ValueError when trying to caste checksum to catch incorrect file format
            return False  # inconsistent network file

    def _generate_network_structure(self):
        """
        Method sorts network data acquired from file into a dictionary.
        :return: social network structure dictionary.
        """
        # remove the first element of the list because it is not needed for the social network data structure
        consistency_number = self._network_data[0]
        self._network_data.remove(consistency_number)

        # this section of code deals with creating the set of keys for the data structure
        # create empty list to compile all data in file_contents
        users_list = []
        # for loop iterates over all main elements in the nested list
        for values in self._network_data:
            # for loop to iterate over all sub-elements in the list
            for sub_values in values:
                # append each sub_element value to users_list
                users_list.append(sub_values)
        # convert users_list into a set
        # automatically removes duplicates from the data, creating usable keys for a dictionary
        dict_keys = set(users_list)
        # sort the keys alphanumerically
        # converts set of keys back into a list
        dict_keys = sorted(dict_keys)

        # this section of code deals with getting the values to be put in the data structure
        # creates empty list to append data to
        dict_values = []
        # iterates over all keys in the list
        for key in dict_keys:
            # filter statement that creates a list of values that contain the key
            # iterates over the file_contents list and appends them to filtered_values list if they contain the key
            filtered_values = list(filter(lambda element: key in element, self._network_data))
            # appends the list of values to a new sub_list in dict_values
            dict_values.append(filtered_values)

        # this section of code deals with the creation and assignment of the data structure in the form of a dictionary
        # creates an empty dictionary
        social_nw = {}
        # creates a pointer variable
        pointer = 0
        # iterates over every key in dict_keys list
        for key in dict_keys:
            # creates a new key:value pair in the dictionary
            # assigns the current key from dict_keys as the key
            # assigns the current values in dict_values indicated by the pointer
            social_nw[key] = dict_values[pointer]
            # increments the pointer to remain in line with key assignment
            pointer += 1

        # this section of code deals with the cleanup and sorting of dictionary values
        # to be updated in the future with implementing this in the previous code blocks to increase efficiency
        # creates an empty list
        item_list = []
        # iterates over every entry in the dictionary
        for key in social_nw:
            # iterates over every item in the list in the key:value pair
            for item in social_nw.get(key):
                # iterates over each sub-item in the list
                for sub_item in item:
                    # if the sub_item doesn't match the key
                    if sub_item != key:
                        # append the sub_item to the item_list
                        item_list.append(sub_item)
                    # if the sub_item matches the key
                    else:
                        # don't append to item_list
                        pass
            # assign the newly cleaned up and sorted item_list to the current key
            social_nw[key] = sorted(item_list)
            # reset the item list back to empty for next cleanup iteration
            item_list = []
        # appends consistency number back to network data
        self._network_data.insert(0, int(*consistency_number))
        # returns the social network dictionary back to the init method
        return social_nw

    def get_network_structure(self):
        """
        Getter for network_structure
        :return: network_structure
        """
        return self._network_structure

    def validate_network_structure(self):
        """
        Returns if network_structure is valid or not
        :return: Boolean, True if valid, False if invalid.
        """
        if self._network_structure is None:
            return False
        else:

            for key in self._network_structure:  # iterate over network structure keys
                for user in self._network_structure:  # nested iteration over network keys
                    if key == user:  # if key equal to user
                        pass  # skip iteration
                    elif user in self._network_structure[key]:  # if user is in values associated with key
                        if key in self._network_structure[user]:  # if key is in values associated with user
                            pass  # skip iteration because no error
                        else:  # otherwise, error detected
                            return False  # inconsistent network
                    else:  # otherwise
                        pass  # skip iteration
            return True  # if no return called, network is consistent

    def _generate_common_friends_structure(self):
        """
        Method analyses social network structure and creates dictionary storing number of common friends for each user.
        :return: common friends dictionary
        """
        # create empty dictionary to put common friends in for each user
        common_friends = {}
        # create a temporary list object
        temp = []
        # for loop to iterate over every key in the social network structure
        for key in self._network_structure:
            # create a new key:value pair in the common_friends dictionary
            # assign the key as the same in the social network structure and the value as an empty list
            common_friends[key] = []
        # for loop to iterate over the common_friends dictionary
        for key in common_friends:
            # for loop to iterate over the social network structure
            for item in self._network_structure:
                # finds the intersection of the network structure key and item
                # returning a set of values containing the items where the key is present
                # this set is converted to a list and the length of the list is assigned to count
                count = len(list(set(self._network_structure[key]) & set(self._network_structure[item])))
                # count is then appended to the temporary list
                temp.append(count)
            # assigns the temporary list to the key in common_friends
            common_friends[key] = temp
            # sets the temporary list to empty to be used for next iteration
            temp = []
        # return the common_friends back to the class attribute
        return common_friends

    def get_network_common_friends_structure(self):
        """
        Getter for network_common_friends_structure
        :return: network_common_friends_structure
        """
        return self._network_common_friends_structure

    def recommend_friend(self, user):
        """
        Method finds the highest number of common friends for a user and recommends a friend based on the highest value.
        :param: user: string input from user
        :return: none
        """
        # creates an empty dictionary to store recommended friends
        recommended_friends = {}
        # creates an empty pointer for item assignment
        pointer = 0
        # gets the common friend count for the user
        struct = self._network_common_friends_structure[user]
        # converts the keys in network structure to a list then iterates over that list
        for name in self._network_structure:
            # create new key in dictionary and assign the item under the pointer index as the value
            recommended_friends[name] = struct[pointer]
            # increment pointer by one
            pointer += 1
        # if the user is in recommended friends
        if user in recommended_friends:
            # set the value to zero
            recommended_friends[user] = 0
        # get intersection of recommended friends and existing friends, convert to list and iterate over it
        for item in list(set(recommended_friends.keys()) & set(self._network_structure[user])):
            # set each existing friends value to zero
            recommended_friends[item] = 0
        # create list of values in recommended friends
        values = list(recommended_friends.values())
        # create list of keys in recommended friends
        keys = list(recommended_friends.keys())
        # if the maximum value in recommended friends is equal to zero
        if max(values) == 0:
            # there are no recommended friends, so set it to None
            recommended_friend = "None"
        # otherwise
        else:
            # set recommended friend to the key(s) with the maximum values
            recommended_friend = keys[values.index(max(values))]
        # display recommended_friend
        # print("Recommended friend for {} is {}.".format(user, recommended_friend))

        return recommended_friend

    def friend_count(self, user):
        """
        Method calculates and displays the friend count of a user
        :param user: string input from user
        :return: none
        """
        # gets length of the list of values stored under the users name in the network structure dictionary
        count = len(self._network_structure[user])
        # displays the friend count for the user
        # print("The friend count for {} is {}.".format(user, count))

        return count

    def least_friends(self):
        """
        Returns users with zero and least number of friends.
        :return:
        """
        least_friends_dict = {"No Friends": [], "Least Friends": []}  # dictionary with empty values

        least_friends_dict["No Friends"].sort()  # add list of users with no friends to dictionary

        minimum = len(self._network_structure)  # set minimum number of friends
        # get list of users with the least amount of friends
        for key in self._network_structure:  # iterate over network structure keys
            if len(self._network_structure[key]) == 0:  # if user has no friends
                least_friends_dict["No Friends"].append(key)
            else:  # otherwise
                if len(self._network_structure[key]) < minimum:  # if friends is less than the current minimum
                    minimum = len(self._network_structure[key])  # new minimum is set

        for key in self._network_structure:  # iterate over network structure keys
            if len(self._network_structure[key]) == minimum:  # if amount of friends is equal to minimum
                least_friends_dict["Least Friends"].append(key)  # appends key to dictionary

        least_friends_dict["No Friends"].sort()
        least_friends_dict["Least Friends"].sort()  # sorts list alphanumerically

        return least_friends_dict  # return dictionary

    def user_friends(self, user):
        """
        Returns the friends of the user in the network structure
        :param user: username input by user
        :return: returns list of friends
        """
        friends = self._network_structure[user]  # gets values stored under user in network structure

        return friends  # returns friends back to main program

    def indirect_friends(self, user):
        """
        Returns the friends of the friends of the user entered.
        :param: user:
        :return:
        """
        friends = self._network_structure[user]  # set users friends to values under user

        if len(friends) == 0:  # get length of friends, if zero, user has no friends
            return "{} has no indirect friends.".format(user)

        else:  # if length is not zero
            indirect_friends_dict = {}  # empty dictionary
            for friend in friends:  # iterate over friends
                # create new key called friend, set values to friends of that user
                indirect_friends_dict[friend] = self._network_structure[friend]

            for key in indirect_friends_dict:  # iterate over indirect friends dictionary
                indirect_friends_dict[key].remove(user)  # remove username from list under key
                if len(indirect_friends_dict[key]) == 0:  # if length of values under key is zero
                    indirect_friends_dict[key] = ["None"]  # set value to None

            return indirect_friends_dict  # return indirect_friends_dict
