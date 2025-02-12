"""Name: Diana Nykonenko
ID: 001265364
Date created: 19/12/2022
"""

from avengers import register  # importiong functions
from sep_fun import openfile

data = None
print("Please enter 'l' to login to the system", '\n'  # asking what user would like to do
                                                 "Enter 'f' to open your own file", '\n'
                                                                                    "Enter 'n' to exit ", '\n')


class Menu:  # class that contains different options for user to do
    def __init__(self):
        pass

    def start(self):  # start again
        while True:
            self.menuu()
            while True:
                start_again = input("Do you want to start again? (yes/no) ").lower()
                if start_again == "yes":
                    break
                elif start_again == "no":
                    exit()
                else:
                    print("Please try again")

    @staticmethod
    def menuu():
        task = input("login(l) / file(f) / end(n) ").lower()  # actually asking to choose
        if task == "l":
            avengers_profile = register()
            name = UsersClass(avengers_profile)  # connection dictionary to the class
            global data
            data = vars(name)
            while True:
                recommend = input("Do you want to see friends suggestions? yes/no ")
                if recommend == "yes":
                    again()
                    break
                elif recommend == "no":
                    break
                else:
                    print("Please try again")
            sn = SocialNetwork()
            sn.less()
        elif task == "f":
            social_NW = openfile()               # basically the same for other case
            name = UsersClassFile(social_NW)
            data = vars(name)
            while True:
                recommend = input("Do you want to see friends suggestions? yes/no ")
                if recommend == "yes":
                    again()
                    break
                elif recommend == "no":
                    break
                else:
                    print("Please try again")
            sn = SocialNetwork()
            sn.less()
        elif task == "n":
            exit()
        else:
            print("Invalid command, try again ")


class UsersClass:  # creating class to store users
    def __init__(self, a):
        self.__dict__ = a


class UsersClassFile:  # creating class to store users
    def __init__(self, f):
        self.__dict__ = f


class SocialNetwork:  # creating class for finding common friends
    def __init__(self):
        self.data = data

    def commonfriends(self):  # friends recomendation system
        input_key = input("Please enter your name: ")
        print(f"Suggestion for: {input_key}")
        if input_key not in self.data:
            print(f"{input_key} not found in data")
            return
        input_list = set(self.data[input_key])
        common_values = []  # create an empty list to store the common values
        for key, values in self.data.items():
            if key != input_key:  # check if the key is not the input key
                common = set(values) & input_list  # find the common elements
                if key not in input_list or common:  # check if the key is not in the input list
                    # common_values.extend(list(common))  # add the common elements to the list of common values
                    if common and key not in input_list:
                        common_values.extend(list(common))  # add the common elements to the list of common values
                        print(f"{key} has {len(common)} common friend(s) with {input_key}")
        if not common_values:
            print("No friends suggestions were found for this user")

    def less(self):
        task = input("Do you want to see users with the less/the most/zero numbers of friends? yes/no ").lower()
        if task == "yes":

            most_elements = max(self.data, key=lambda x: len(self.data[x]))
            print("User(s) with the most connections:",
                  [key for key, value in self.data.items() if len(value) == len(self.data[most_elements])],
                  len(self.data[most_elements]), "friends added")

            # Find the key(s) with the least elements (ignoring zero)
            non_zero_values = {key: value for key, value in self.data.items() if len(value) != 0}
            least_elements = min(non_zero_values, key=lambda x: len(non_zero_values[x]))
            print("User(s) with the least connections:",
                  [key for key, value in self.data.items() if len(value) == len(non_zero_values[least_elements])],
                  len(self.data[least_elements]), "friens added")

            # Find the key(s) with zero elements
            zero_elements = [key for key, value in self.data.items() if len(value) == 0]
            print("User(s) with no friends added:", zero_elements)

        elif task == "no":
            pass
        else:
            print("Please try again")
            sn = SocialNetwork()
            sn.less()


def again():  # function to display friends recomendations again
    while True:  # loop for recomendation
        sn = SocialNetwork()
        sn.commonfriends()  # calling function for class
        more = input("Do you want to reccommend friend to another user? yes/no ")
        if more == "yes":
            pass
        elif more == "no":
            break
        else:
            print("Please try again")

