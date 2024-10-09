#!/usr/bin/env python3

'''
# Login Feature Project

A test project for my college course.

## TODO:

3. Create a menu of options for your user and display it if the user logins
successfully. Place this menu in a subroutine/procedure that can be called on
login happens.
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


# version check
if (sys.version_info[0] < 3
    or (sys.version_info[0] >= 3 and sys.version_info[1] < 10)):
    
    print("Must be running Python >= 3.10, please upgrade.")
    sys.exit()


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

    def info(self, message_text: str, title: bool = False,
             error: bool = False) -> None:
        '''
        Prints a message to user.

        Optionaly formats it as a title or an error.
        '''

        # format & print the message
        if title:
            print(f'# {message_text}\n')
        elif error:
            print(f'\nERROR: {message_text}\n')
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

        while True:
            # retrieve choice
            choice = int(input('\nPlease enter a number: ')) - 1
            
            # check selection in range
            if choice in range(len(options)):
                break
            else:
                self.InterfaceObj.info(
                    'Please choose an option from the list.',
                    error=True
                )
                continue

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

        # get credentials from file
        with open(self.userdata_path, 'r') as userdata_file:
            userdata = json.load(userdata_file)

        while True:
            # retrieve username and hash it
            username_hash = sha256(
                self.InterfaceObj.prompt(
                    'Username: '
                ).encode()
            ).hexdigest()

            # if username is invalid
            if username_hash in userdata:
                break
            else:
                self.InterfaceObj.info(
                    'Account does not exist, please try again.',
                    error=True
                )
                continue

        while True:
            # retrieve password and hash it
            password_hash = sha256(
                self.InterfaceObj.prompt(
                    'Password: ',
                    hidden=True
                ).encode()
            ).hexdigest()

            # check if password is correct
            if password_hash == userdata[username_hash]['password']:
                break
            else:
                self.InterfaceObj.info(
                    'Password is incorrect, please try again.',
                    error=True
                )
                continue

        # set current account
        self.current_user = username_hash
        
        self.InterfaceObj.info('\nLogged in successfully.')

        return
    
    def signup(self) -> None:
        '''
        Method for creating a new user.
        '''

        # get current credentials from file
        with open(self.userdata_path, 'r') as userdata_file:
            userdata = json.load(userdata_file)

        while True:
            # retrieve username and hash it
            username_hash = sha256(
                self.InterfaceObj.prompt(
                    'Username: '
                ).encode()
            ).hexdigest()

            # if username already exists
            if username_hash in userdata:
                self.InterfaceObj.info(
                    'Account already exists, please use a different name.',
                    error=True
                )
                continue
            else:
                break

        # retrieve a display name
        display_name = self.InterfaceObj.prompt(
            'Display Name: '
        )
        
        while True:
            # retrieve an email address
            email_address = self.InterfaceObj.prompt(
                'Email Address: '
            )

            # check is the email is valid
            if fullmatch(r'[^@]+@[^@]+\.[^@]+', email_address):
                break
            else:
                self.InterfaceObj.info(
                    'Email is invalid, please try again.',
                    error=True
                )
                continue

        while True:
            # retrieve password
            password = self.InterfaceObj.prompt(
                'Password: ',
                hidden=True
            )

            # check if password is valid
            if len(password) < 8:
                self.InterfaceObj.info(
                    'Password must be 8 or more characters, please try again.',
                    error=True
                )
                continue
            elif password.lower() == password:
                self.InterfaceObj.info(
                    'Password needs an uppercase, please try again.',
                    error=True
                )
                continue
            elif password.upper() == password:
                self.InterfaceObj.info(
                    'Password needs a lowercase, please try again.',
                    error=True
                )
                continue
            elif password.isalpha():
                self.InterfaceObj.info(
                    'Password needs a number, please try again.',
                    error=True
                )
                continue
            else:
                # if all requirements are met, hash the password
                password_hash = sha256(password.encode()).hexdigest()
                del password
                break


        # retrieve a confirmation of the password
        confirm_password_hash = sha256(
            self.InterfaceObj.prompt(
                'Confirm Password: ',
                hidden=True
            ).encode()
        ).hexdigest()

        # check if passwords match
        while password_hash != confirm_password_hash:
            self.InterfaceObj.info(
                'Passwords do not match, please try again.',
                error=True
            )

            # retrieve password
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

        # add new user to data
        userdata[username_hash] = dict() 
        userdata[username_hash]['password'] = password_hash
        userdata[username_hash]['display_name'] = display_name
        userdata[username_hash]['email_address'] = email_address
    
        # write new data to file
        with open(self.userdata_path, 'w') as userdata_file:
            json.dump(userdata, userdata_file)

        # set current account
        self.current_user = username_hash

        self.InterfaceObj.info('\nAccount created successfully.')

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
