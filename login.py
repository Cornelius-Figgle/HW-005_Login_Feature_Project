#!/usr/bin/env python3

'''
# Login Feature Project

A test project for my college course.

## TODO:

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


class Interface:
    '''
    Collection of methods for displaying information to, and receiving
    information from, the user in a consistant and modifiable way. 
    '''

    def __init__(self) -> None:
        '''
        Empty meta method.
        '''

        # do nothing
        pass

        return

    def info(self, message_text: str, title: bool = False) -> None:
        '''
        Prints a message to user.

        Optionaly formats it as a title.
        '''

        # format & print the message
        if title:
            print(f'# {message_text}\n')
        else:
            print(f'{message_text}\n')

        return
    
    def prompt(self, prompt_text: str, hidden: bool = False) -> str:
        '''
        Prompts the user for an input and returns this input.

        Optionally masks the user input with `getpass.getpass()`.
        '''

        # prompt and store the input value
        if hidden:
            user_text = getpass(prompt_text)
        else:
            user_text = input(prompt_text)

        return user_text

class Login:
    '''
    Collection of methods for generating a login window for an application.
    '''

    def __init__(self) -> None:
        '''
        Initialises the object.  
        '''

        # create object for the interface
        self.InterfaceObj = Interface()

        # print a title and description
        self.InterfaceObj.info('Login Feature Project', title=True)
        self.InterfaceObj.info(
            'Simple login feature that could be implemented into another '
            +'program.'
        )

        return

    ...


def main() -> None:
    '''
        
    '''

    LoginObj = Login()

    user = dict()
    user['username'] = LoginObj.InterfaceObj.prompt(
        'Username: '
    )
    user['password'] = LoginObj.InterfaceObj.prompt(
        'Password: ',
        hidden=True
    )

    print('\n'+str(user))

    return

# only execute if called directly
if __name__ == '__main__':
    sys.exit(main())
