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


import json
import os
import sys
from getpass import getpass
from hashlib import sha256
from re import fullmatch


class AccountNotFound(Exception):
    '''Raised when the requested account isn't present in the data file.'''
    pass

class IncorrectPassword(Exception):
    '''Raised when the password is not correct for the requested account.'''
    pass

class AccountAlreadyExists(Exception):
    '''Raised when the user tries to create an account that already exists.'''
    pass

class UnmatchedPasswords(Exception):
    '''Raised when the confirmation password does not match.'''
    pass

class SelectionOutOfRange(Exception):
    '''Raised when the user selects an option not in the list.'''
    pass

class FieldEmpty(Exception):
    '''Raised when the user doesn't fill out a field.'''
    pass

class InvalidEmail(Exception):
    '''Raised when the email address is invalid.'''
    pass


class Interface:
    '''
    Collection of methods for displaying information to, and receiving
    information from, the user in a consistant and modifiable way. 
    '''

    def __init__(self) -> None:
        '''
        Empty meta method.
        '''
        
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

    def option(self, prompt_text: str, options: list[str]) -> int:
        '''
        Prompts the user to pick and option from a list, and returns the index
        of this option.
        '''

        # print the question
        print(f'{prompt_text}')
        # print options in a numbered list
        for option in options:
            print(f'{options.index(option)+1}) {option}')

        # retrieve choice
        choice = int(input('\nPlease enter a number: ')) - 1
        print()

        return choice

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

        # setup data file
        self.userdata_path = os.path.join(
            os.path.dirname(__file__),
            'userdata.json'
        )

        # create initial data file if not present
        if not os.path.exists(self.userdata_path):
            with open(self.userdata_path, 'w') as userdata_file:
                self.InterfaceObj.info(
                    'File `userdata.json` does not exist, creating now.'
                )
                
                # creates a blank file
                json.dump({}, userdata_file)

        # set current account
        self.current_user = None

        return

    def login(self) -> None:
        '''
        Method for processing a user login.
        '''

        # retrieve username and hash it
        username_hash = sha256(
            self.InterfaceObj.prompt(
                'Username: '
            ).encode()
        ).hexdigest()
        
        # compare credentials to data on file
        with open(self.userdata_path, 'r') as userdata_file:
            userdata = json.load(userdata_file)

        # if username is invalid
        if username_hash not in userdata:
            raise AccountNotFound()

        # retrieve password and hash it
        password_hash = sha256(
            self.InterfaceObj.prompt(
                'Password: ',
                hidden=True
            ).encode()
        ).hexdigest()

        # if password is incorrect
        if password_hash != userdata[username_hash]["password"]:
            raise IncorrectPassword()


        # set current account
        self.current_user = username_hash

        return
    
    def signup(self) -> None:
        '''
        Method for creating a new user.
        '''

        # retrieve a username and hash it
        username_hash = sha256(
            self.InterfaceObj.prompt(
                'Username: '
            ).encode()
        ).hexdigest()

        # load current data from file
        with open(self.userdata_path, 'r') as userdata_file:
            userdata = json.load(userdata_file)

        # check if user already exists
        if username_hash in userdata:
            raise AccountAlreadyExists()

        # retrieve a display name
        display_name = self.InterfaceObj.prompt(
            'Display Name: '
        )
        
        # retrieve an email address
        email_address = self.InterfaceObj.prompt(
            'Email Address: '
        )

        # check is the email is valid
        if not fullmatch(r'[^@]+@[^@]+\.[^@]+', email_address):
            raise InvalidEmail()

        # retrieve a password and hash it
        password_hash = sha256(
            self.InterfaceObj.prompt(
                'Password: ',
                hidden=True
            ).encode()
        ).hexdigest()

        # retrieve a confirmation of the password
        confirm_password_hash = sha256(
            self.InterfaceObj.prompt(
                'Confirm Password: ',
                hidden=True
            ).encode()
        ).hexdigest()

        # confirm the user has typed it correctly
        if password_hash != confirm_password_hash:
            raise UnmatchedPasswords()
      
        # add new user to data
        userdata[username_hash] = dict() 
        userdata[username_hash]["password"] = password_hash
        userdata[username_hash]["display_name"] = display_name
        userdata[username_hash]["email_address"] = email_address
    
        # write new data to file
        with open(self.userdata_path, 'w') as userdata_file:
            json.dump(userdata, userdata_file)

        # set current account
        self.current_user = username_hash

        return


def main() -> None:
    '''
    Controls the main program flow.
    '''

    # initialise object
    LoginObj = Login()
    
    # start auth
    choice = LoginObj.InterfaceObj.option(
        'What would you like to do?',
        ['Login', 'Sign Up']
    )
    match choice:
        case 0:
            LoginObj.login()
        case 1:
            LoginObj.signup()
        case _:
            pass

    return


# only execute if called directly
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit()
