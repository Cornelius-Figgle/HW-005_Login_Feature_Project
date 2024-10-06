#!/usr/bin/env python3

'''
Programming Project - Login Feature Challenge

1. Ask the user for a username and password. Store these in variables with
appropriate names. Have clear messages for users and make sure you introduce
the program to the user so you make sure they know what they are doing.
2. Allow user to login if the username and password inserted matches a
previously stored username and password (one you had assigned to appropriately
named variables). Give the user a message of confirmation or not that username
and password is correct and login was permitted.
3. Create a menu of options for your user and display it if the user logins
successfully. Place this menu in a subroutine/procedure that can be called on
login happens.
4. Amend your program to allow user to either register or login at the start
of your program (after introducing the user to your program). The user should
input a username, a password and an email address.
5. Amend your code to allow verification of the password - this means the user
needs to input the password twice and you need to verify that both are the
same.
6. Amend the code to validate the password and make sure it has at least 8
characters in length and uses capitals, lowercase and numbers.
7. Amend your code to validate that the user inputted a valid email address and
ask the user to input again (password or email) if is not valid.
8. Record username, password and email in a list. Use a 2D list if  you want to
save more than one set of username/password/email.
9. Record all the usernames, passwords and emails in a file and amend the code
to when logging in compare the code to all the entries of the usernames in the
file. Display messages of incorrect password, users not registered and others,
if user not in the file.
'''


import os
import pickle
import sys
from getpass import getpass


class Login:
    ...


def prompt(fields: list[dict]):
    '''
    Prompts the user for an input and returns it. `fields` is a `list` of
    `dicts` structured as follows:

    ```python
    fields = [
        {
            "field_name": "username",
            "prompt_text": "Please enter a username: "
        },
        {
            "field_name": "password",
            "prompt_text": "Please enter a password: ",
            "hidden": True
        }
    ]
    ```

    The options for each field are as follows:

     - `field_name`
       - `string`, the key to store the input results under
     - `prompt_text`
       - `string`, contains the text to print
     - `hidden`
       - `bool`, whether or not to mask the user input
    '''

    # setup return dictionary
    inputs = dict()

    # prompt and store for each field
    for field in fields:
        if "hidden" in field and field["hidden"] == True:
            inputs[field["field_name"]] = getpass(field["prompt_text"])
        else:
            inputs[field["field_name"]] = input(field["prompt_text"])

    return inputs

def main() -> None:
    '''
        
    '''

    fields = [
        {
            "field_name": "username",
            "prompt_text": "Please enter a username: "
        },
        {
            "field_name": "password",
            "prompt_text": "Please enter a password: ",
            "hidden": True
        }
    ]
    print(prompt(fields))


# if called directly
if __name__ == '__main__':
    sys.exit(main())
