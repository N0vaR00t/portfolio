"""Name: Diana Nykonenko
ID: 001265364
Date created: 23/11/2022
"""

import shelve                                                              # creating database using shelve


def register():
    def add_friend():                                                      # creating function for registration
        friend = input("Who do you know? ")
        if friend not in avengers:                                         # checking if friend is registered
            print("Friend is not found")
            attempt = input("Proceed without connections? yes/no/again: ").lower()
            if attempt == "yes":                                           # addidng without friend
                avengers[name] = friends
            elif attempt == "no":
                exit()
            elif attempt == "again":
                add_friend()
            else:
                print("Invalid answer, try again")
                add_friend()
        else:
            if len(avenger_profile) < 2:         # checking if there are not enought registered users to use info about
                inside_out_friends = []          # friends list is empty if only one user is in the system
            else:
                inside_out_friends = list(avenger_profile.get(friend))      # getting list of already added friends
            inside_out_friends.append(name)
            friends.append(friend)                                          # adding names to lists
            avengers[name] = friends
            avengers[friend] = inside_out_friends                           # updating dictionary
            if len(friends) < 2:
                second_friend()
            else:
                pass

    def second_friend():
        other = input("Do you want to add another friend? yes/no ").lower()  # to add another friend
        if other == "yes":
            add_friend()                                                     # calling function to add the secong friend
            print("User is added to the system")
        elif other == "no":
            print("User is added to the system")
        else:
            print("Invalid answer, try again")
            second_friend()

    with shelve.open("avengersdata") as avengers:                           # printing all key-value pairs
        avenger_profile = dict(avengers.items())

    def db_to_text():
        number_of_users = len(avenger_profile)
        file_data = "datafromdatabase"
        fd = open(file_data, "w")
        fd.write(str(number_of_users) + '\n')
        for k, v in avenger_profile.items():
            fd.write(str(k) + ' ' + str(v) + '\n')
        fd.close()

    avengers = shelve.open("avengersdata")
    name = input("Enter your name: ")                                       # entering name
    if name in avengers:                                                    # checking if name is in the system
        with shelve.open("avengersdata"):
            print("Access granted", name)
            friends = list(avenger_profile.get(name))
            print("You are friends with", friends)
    else:
        print("Access denied")
        questn = input("Do you want to register? yes/no/again: ").lower()
        if questn == "yes":
            print("Registration started for", name)       # starting registration by adding user to the shelve
            friends = []
            add_friend()                                  # calling function for friends registration
        elif questn == "no":
            print("Try another time")
            exit()
        elif questn == "again":
            register()
        else:
            print("Invalid answer, try again")
            register()
        with shelve.open("avengersdata") as avengers:
            avenger_profile = dict(avengers.items())
    db_to_text()
    avengers.close()
    return avenger_profile
