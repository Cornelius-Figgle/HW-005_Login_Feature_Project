#!/usr/bin/env python3

'''
# Login Feature Project

A test project for my college course.

## TODO:

3. Create a menu of options for your user and display it if the user
logins successfully. Place this menu in a subroutine/procedure that can
be called on login happens.
'''

__version__ = '1.0.0'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2024 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison']

# source: https://github.com/Cornelius-Figgle/HW-005_Login_Feature_Project


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
            print(f'\n\tERROR: {message_text}\n')
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
        Prompts the user to pick and option from a list, and returns the
        index of this option.
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
                self.info(
                    'Please choose an option from the list.',
                    error=True
                )
                continue

        print()

        return choice

class Login:
    '''
    Collection of methods for generating a login window for an
    application.
    '''

    def __init__(self) -> None:
        '''
        Initialises the object.
        '''
        
        # create object for the interface
        self.InterfaceObj = Interface()

        # print a title and description
        self.InterfaceObj.info('Login Feature Project', title=True)
        self.InterfaceObj.info('Simple login feature that could be implemented'
            +'into another program.')

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

            # if username is not valid
            if username_hash not in userdata:
                self.InterfaceObj.info(
                    'Account does not exist, please try again.',
                    error=True
                )
                continue
            # if field is blank
            elif not username_hash:
                self.InterfaceObj.info(
                    'Field blank, please enter a username.',
                    error=True
                )
                continue
            else:
                break

        for i in range(3):
            # retrieve password and hash it
            password_hash = sha256(
                self.InterfaceObj.prompt(
                    'Password: ',
                    hidden=True
                ).encode()
            ).hexdigest()

            # check if password is correct
            if password_hash != userdata[username_hash]['password']:
                if i < 2:
                    self.InterfaceObj.info(
                        'Password is incorrect, please try again.',
                        error=True
                    )
                else:
                    self.InterfaceObj.info(
                        'Too many incorrect attempts. Exiting progam.',
                        error=True
                    )
                    return 
                continue
            else:
                break
        
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
            # if field blank
            elif not username_hash:
                self.InterfaceObj.info(
                    'Field blank, please enter a username.',
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

    def main_menu(self) -> None:
        '''
        Method for displaying the landing page after a successful login. 
        '''
        
        # get user info from file
        with open(self.userdata_path, 'r') as userdata_file:
            userdata = json.load(userdata_file)

        # print welcome message
        self.InterfaceObj.info(
            f'Hello {userdata[self.current_user]["display_name"]}!'
        )

        # loop
        while True:
            # print title
            self.InterfaceObj.info(
                'Main Menu',
                title=True
            )

            # menu
            choice = self.InterfaceObj.option(
                'What would you like to do?',
                ['Account Options', 'Version Info', 'Quit']
            )
            match choice:
                case 0:
                    self.account_options()
                case 1:
                    self.version_info()
                case 2:
                    return

    def account_options(self) -> None:
        '''
        Method for changing account information.
        '''

        while True:
            # get current credentials from file
            with open(self.userdata_path, 'r') as userdata_file:
                userdata = json.load(userdata_file)

            # print title
            self.InterfaceObj.info(
                'Account Options',
                title=True
            )

            # submenu
            choice = self.InterfaceObj.option(
                'What would you like to do?',
                [
                    'Change Username',
                    'Change Display Name',
                    'Change Email Address', 
                    'Change Password',
                    'Back to Main Menu'
                ]
            )
            match choice:
                case 0:
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
                                'Account already exists, please use a'
                                    +'different name.',
                                error=True
                            )
                            continue
                        # if field blank
                        elif not username_hash:
                            self.InterfaceObj.info(
                                'Field blank, please enter a username.',
                                error=True
                            )
                            continue
                        else:
                            break

                    # move current user details to new username
                    userdata[username_hash] = userdata[self.current_user].copy()
                    userdata.pop(self.current_user)
                    self.current_user = username_hash

                    # write new data to file
                    with open(self.userdata_path, 'w') as userdata_file:
                        json.dump(userdata, userdata_file)

                    self.InterfaceObj.info('\nUsername changed successfully.')
                case 1:
                    # retrieve a display name
                    display_name = self.InterfaceObj.prompt(
                        'Display Name: '
                    )
                    
                    # change stored name
                    userdata[self.current_user]['display_name'] = display_name

                    # write new data to file
                    with open(self.userdata_path, 'w') as userdata_file:
                        json.dump(userdata, userdata_file)

                    self.InterfaceObj.info('\nDisplay Name changed successfully.')
                case 2:
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

                    # change stored email
                    userdata[self.current_user]['email_address'] = email_address

                    # write new data to file
                    with open(self.userdata_path, 'w') as userdata_file:
                        json.dump(userdata, userdata_file)

                    self.InterfaceObj.info('\nEmail Address changed successfully.')
                case 3:
                    for i in range(3):
                        # retrieve password and hash it
                        password_hash = sha256(
                            self.InterfaceObj.prompt(
                                'Current Password: ',
                                hidden=True
                            ).encode()
                        ).hexdigest()

                        # check if password is correct
                        if password_hash != userdata[self.current_user]['password']:
                            if i < 2:
                                self.InterfaceObj.info(
                                    'Password is incorrect, please try again.',
                                    error=True
                                )
                            else:
                                self.InterfaceObj.info(
                                    'Too many incorrect attempts. Exiting progam.',
                                    error=True
                                )
                                return 
                            continue
                        else:
                            break

                    while True:
                        # retrieve password
                        password = self.InterfaceObj.prompt(
                            'New Password: ',
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
                            'Confirm New Password: ',
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
                                'New Password: ',
                                hidden=True
                            ).encode()
                        ).hexdigest()

                        # retrieve a confirmation of the password
                        confirm_password_hash = sha256(
                            self.InterfaceObj.prompt(
                                'Confirm New Password: ',
                                hidden=True
                            ).encode()
                        ).hexdigest()
                        
                    # change stored password
                    userdata[self.current_user]['password'] = password_hash

                    # write new data to file
                    with open(self.userdata_path, 'w') as userdata_file:
                        json.dump(userdata, userdata_file)

                    self.InterfaceObj.info('\nPassword changed successfully.')
                case 4:
                    return

    def version_info(self) -> None:
        '''
        Method for fetching and displaying version info.
        '''

        # print title
        self.InterfaceObj.info(
            'Version Info',
            title=True
        )

        # get python version major.minor.micro
        python_version = '.'.join(
            str(sys.version_info[i]) for i in range(3)
        )

        # display
        self.InterfaceObj.info(
            f'> {os.path.basename(__file__)} {__version__}' \
            f'\n> Python {python_version}'
        )

        while True:
            # submenu
            choice = self.InterfaceObj.option(
                'What would you like to do?',
                ['Back to Main Menu']
            )
            match choice:
                case 0:
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

    # if successful login
    if LoginObj.current_user:
        # display program main menu
        LoginObj.main_menu()
    
    return


# only execute if called directly
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit()
