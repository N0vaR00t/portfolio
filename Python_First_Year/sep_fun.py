"""Name: Diana Nykonenko
ID: 001265364
Date created: 16/12/2022
"""

import os


def openfile():
    while True:
        print("What file do you want to open?", '\n'
                                                "Enter in format - file.txt")
        open_new_file = input("Enter 'n' to exit ").lower()
        social_NW = {}

        def dicfromfile():                              # function to creat dictionary from file
            try:
                for line in f:
                    words = line.split()                # splitting lines
                    if len(words) >= 1:                 # checking if there are at least one word in the line
                        the_key = words[0]
                        if len(words) > 1:              # checking if there are more than 1 word
                            if the_key in social_NW:    # checking if name is already in dictionary
                                social_NW[the_key].extend(words[1:])  # adding friends to the list in value
                            else:
                                social_NW[the_key] = words[1:]  # creating key-value pair with all other words as values
                        else:
                            if the_key not in social_NW:
                                social_NW[the_key] = []
            except IndexError:
                social_NW[words[0]] = 0
            try:
                for t_key, t_value in social_NW.items():
                    for v in t_value:
                        if v in social_NW.keys() and t_key not in social_NW[v]:
                            raise ValueError("The network is inconsistent, try another file.")
            except ValueError as e:
                print(e)
                return None
            else:
                pass
            return social_NW                                         # return as created dictionary

        if os.path.exists(open_new_file):                            # checking if entered file exists
            with open(open_new_file, 'r') as f:
                next(f)
                social_NW = dicfromfile()                            # calling the function to create dictionary
                if social_NW:
                    break
                else:
                    continue
        elif open_new_file == "n":                                   # exit if 'n' is entered
            exit()

        else:
            print("File doesn't exist, try again")

    while True:
        ask = input("Do you want to display all users' data? ")     # asking to print all users' data
        if ask == "yes":
            for key, value in social_NW.items():                    # printing data
                print(key, "->", *value)
            break
        elif ask == "no":
            break
        else:
            print("Please try again")

    while True:
        thename = input("Enter your name: ")                        # enter name to find friends
        if thename in social_NW:
            print("The number of friends added", len(social_NW[thename]))
            print("You are friends with", social_NW[thename])       # printing value (friends)
            break
        elif thename == "n":
            exit()
        else:
            print("User is not in the list, try another name ")
    return social_NW                                                # return as created dictionary
