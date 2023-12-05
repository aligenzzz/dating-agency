import os
from getpass import getpass
from colorama import Fore
from database import Database
from models import User
from tabulate import tabulate


def emphasis(content):
    return Fore.LIGHTMAGENTA_EX + content + Fore.RESET


def error(content):
    return Fore.RED + content + Fore.RESET


def hello():
    Database.connect()

    while True:
        os.system('cls')
        print('Welcome to ' + emphasis('DATING AGENCY\n'))

        print('What do you want?\n' +
            emphasis('1') + ' Login\n' +
            emphasis('2') + ' Register\n' +
            emphasis('3') + ' Exit\n')
        
        while True:
            choice = input('Enter ' + emphasis('here: '))

            if choice == '1' or choice == '2' or choice == '3':
                break
            else:
                print(error('\nInvalid data. Try again!\n'))

        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            Database.disconnect()
            break
    

def login():
    os.system('cls')

    while True:
        username = input('Enter ' + emphasis('username') + ': ')
        password = getpass('Enter ' + emphasis('password') + ': ')

        user = Database.get_user(username, password)

        if user is None:
            print(error('\nInvalid data. Try again!')) 
            e = input('Do you want exit? (1) ')
            if e == '1':
                break
            print('')
        else:
            break

    if user.role == "Client":
        client(user)
    elif user.role == "Moderator":
        moderator(user)
    elif user.role == "Admin":
        admin(user)


def register():
    os.system('cls')

    while True:
        print('Required fields are marked with ' + emphasis('*\n'))

        username = input('Enter ' + emphasis('username *') + ': ')
        password = getpass('Enter ' + emphasis('password *') + ': ')
        email = input('Enter ' + emphasis('email') + ': ')
        first_name = input('Enter ' + emphasis('first name *') + ': ')
        last_name = input('Enter ' + emphasis('last name *') + ': ')
        age = input('Enter ' + emphasis('age *') + ': ')
        hobbies = input('Enter ' + emphasis('hobbies') + ': ')
        occupation = input('Enter ' + emphasis('occupation') + ': ')
        other = input('Enter ' + emphasis('other information') + ': ')
        country = input('Enter ' + emphasis('country *') + ': ')
        city = input('Enter ' + emphasis('city') + ': ')

        if age.isnumeric() and age != '':
            client = Database.add_client(username, password, email, first_name, last_name,
                                        int(age), hobbies, occupation, other, country, city)
        else:
            client = None

        if client is None:
            print(error('\nInvalid data. Try again!')) 
            e = input('Do you want exit? (1) ')
            if e == '1':
                break
            print('')
        else:
            print('\nYou were succesfully ' + emphasis('registered') + '!\n')
            input('\n')
            break


def client(user: User):
    while True:
        os.system('cls')
        print('Hello, ' + emphasis('client') + '!\n')

        if Database.is_banned(user.username):
            print('You were ' + emphasis('banned') + '!\n')
            input('\n')
            break

        print('What do you want?\n' +
            emphasis('1') + ' View all clients\' profiles\n' +
            emphasis('2') + ' View some client\'s profile\n' +
            emphasis('3') + ' View all chats\n' +
            emphasis('4') + ' Open some chat\n' +
            emphasis('5') + ' Add chat\n' +
            emphasis('6') + ' View all meetings\n' +
            emphasis('7') + ' Make meeting\n' +
            emphasis('8') + ' Edit your profile\n' +
            emphasis('9') + ' Add complaint\n' +
            emphasis('10') + ' Exit\n')
    
        while True:
            choice = input('Enter ' + emphasis('here: '))

            if choice == '1' or choice == '2' or choice == '3' or \
            choice == '4' or choice == '5' or choice == '6' or \
            choice == '7' or choice == '8' or choice == '9' or choice == '10':
                break
            else:
                print(error('\nInvalid data. Try again!')) 
                e = input('Do you want exit? (1) ')
                if e == '1':
                    break
                print('')

        if choice == '1':
            os.system('cls')
            print(emphasis('View all clients\' profiles...\n'))

            clients = Database.get_clients()
            headers = ['FirstName', 'LastName', 'Age',
                       'Username', 'Email', 
                       'Hobbies', 'Occupation', 'Other',
                       'Country', 'City']
            
            print(tabulate(clients, headers=list(map(emphasis, headers))))
            input('\n')

        elif choice == '2':
            os.system('cls')
            print(emphasis('View some client\'s profile...\n'))

            while True:
                username = input('Enter ' + emphasis('username') + ': ')
                profile = Database.get_client_profile(username)
                print('')

                if profile is None:
                    print(error('Invalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    headers = ['FirstName', 'LastName', 'Age',
                               'Username', 'Email', 
                               'Hobbies', 'Occupation', 'Other',
                               'Country', 'City']
                    print(tabulate(profile, headers=list(map(emphasis, headers))))
                    input('\n')
                    break

        elif choice == '3':
            os.system('cls')
            print(emphasis('View all chats...\n'))

            chats = Database.get_client_chats(user.username)
            headers = ['Id', 'Name', 'Partner']
            print(tabulate(chats, headers=list(map(emphasis, headers))))
            input('\n')

        elif choice == '4':
            os.system('cls')
            print(emphasis('Open some chat...\n'))

            while True:
                id = input('Enter ' + emphasis('chat\'s id') + ': ')
                chat = Database.get_chat(id, user.username)

                if chat is None:
                    print(error('\nInvalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    while True:
                        chat = Database.get_chat(id, user.username)
                        print('\nChat ' + emphasis(chat.name) + ' with ' + emphasis(chat.partner) + ':\n')

                        headers = ['Content', 'Datetime', 'Sender']
                        print(tabulate(chat.messages, headers=list(map(emphasis, headers))))

                        print('\nWhat do you want?\n' +
                            emphasis('1') + ' Add message\n' +
                            emphasis('2') + ' Exit\n')
                        
                        while True:
                            choice = input('Enter ' + emphasis('here: '))

                            if choice == '1' or choice == '2':
                                break
                            else:
                                print(error('\nInvalid data. Try again!')) 
                                e = input('Do you want exit? (1) ')
                                if e == '1':
                                    break
                                print('')

                        if choice == '1':
                            while True:
                                content = input('Enter: ')
                                message = Database.add_message(content, user.username, int(id))

                                if message is None:
                                    print(error('\nInvalid data. Try again!')) 
                                    e = input('Do you want exit? (1) ')
                                    if e == '1':
                                        break
                                    print('')
                                else:
                                    break
                        elif choice == '2':
                            break

        elif choice == '5':
            os.system('cls')
            print(emphasis('Add chat...\n'))

            while True:
                partner = input('Enter ' + emphasis('partner\'s username') + ': ')
                name = input('Enter ' + emphasis('chat\'s name') + ': ')

                chat = Database.add_chat(user.username, partner, name)

                if chat is None:
                    print(error('\nInvalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    print('\nYou were succesfully ' + emphasis('added chat') + '!\n')
                    input('\n')
                    break

        elif choice == '6':
            os.system('cls')
            print(emphasis('View all meetings...\n'))

            meetings = Database.get_client_meetings(user.username)
            headers = ['Name', 'Datetime', 'Country', 'City', 'Address', 'Partner']
            print(tabulate(meetings, headers=list(map(emphasis, headers))))
            input('\n')

        elif choice == '7':
            os.system('cls')
            print(emphasis('Make meeting...\n'))

            while True:
                partner = input('Enter ' + emphasis('partner\'s username') + ': ')
                name = input('Enter ' + emphasis('meeting\'s name') + ': ')
                datetime = input('Enter ' + emphasis('datetime') + ': ')
                country = input('Enter ' + emphasis('country') + ': ')
                city = input('Enter ' + emphasis('city') + ': ')
                address = input('Enter ' + emphasis('address') + ': ')

                meeting = Database.add_meeting(user.username, partner, name,
                                               datetime, country, city, address)

                if meeting is None:
                    print(error('\nInvalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    print('\nYou were succesfully ' + emphasis('made meeting') + '!\n')
                    input('\n')
                    break

        
        elif choice == '8':
            os.system('cls')
            print(emphasis('Edit your profile...\n'))

            while True:
                print('What you don\'t want to change, just ' + emphasis('skip!\n'))

                username = input('Enter ' + emphasis('username') + ': ')
                password = getpass('Enter ' + emphasis('password') + ': ')
                email = input('Enter ' + emphasis('email') + ': ')
                first_name = input('Enter ' + emphasis('first name') + ': ')
                last_name = input('Enter ' + emphasis('last name') + ': ')
                age = input('Enter ' + emphasis('age') + ': ')
                hobbies = input('Enter ' + emphasis('hobbies') + ': ')
                occupation = input('Enter ' + emphasis('occupation') + ': ')
                other = input('Enter ' + emphasis('other information') + ': ')
                country = input('Enter ' + emphasis('country') + ': ')
                city = input('Enter ' + emphasis('city') + ': ')

                if age.isspace() or not age.isnumeric():
                    age = -1

                result = Database.edit_client(user, username, password, email, first_name,
                                            last_name, int(age), hobbies, occupation, other, country, city)

                if result is None:
                    print(error('\nInvalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    print('\nYou were succesfully ' + emphasis('edited profile') + '!')
                    input('\n')
                    break


        elif choice == '9':
            os.system('cls')
            print(emphasis('Add complaint...\n'))

            while True:
                content = input('Enter ' + emphasis('complaint\'s content') + ': \n')
                complaint = Database.add_complaint(user.username, content)

                if complaint is None:
                    print(error('\nInvalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    print('\nYou were succesfully ' + emphasis('complainted') + '!\n')
                    input('\n')
                    break

        elif choice == '10':
            break


def moderator(user: User):    
    while True:
        os.system('cls')
        print('Hello, ' + emphasis('moderator') + '!\n')

        print('What do you want?\n' +
            emphasis('1') + ' View all clients\n' +
            emphasis('2') + ' Ban/unban some client\n' +
            emphasis('3') + ' View all actions\n' +
            emphasis('4') + ' View some client\'s actions\n' +
            emphasis('5') + ' Exit\n')
    
        while True:
            choice = input('Enter ' + emphasis('here: '))

            if choice == '1' or choice == '2' or choice == '3' or \
            choice == '4' or choice == '5':
                break
            else:
                print(error('\nInvalid data. Try again!')) 
                e = input('Do you want exit? (1) ')
                if e == '1':
                    break
                print('')

        if choice == '1':
            os.system('cls')
            print(emphasis('View all clients...\n'))

            clients = Database.get_clients_with_banned()
            headers = ['FirstName', 'LastName', 'Age', 'Banned',
                       'Username', 'Email', 
                       'Hobbies', 'Occupation', 'Other',
                       'Country', 'City']
            
            print(tabulate(clients, headers=list(map(emphasis, headers))))
            input('\n')

        elif choice == '2':
            os.system('cls')
            print(emphasis('Ban/unban some client...\n'))

            while True:
                username = input('Enter ' + emphasis('username') + ': ')
                result = Database.ban_unban_client(username)
                print('')

                if result is None:
                    print(error('Invalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')  
                else:
                    break

            if result:
                print('This client was succesfully ' + emphasis('banned') + '!')
            else:
                print('This client was succesfully ' + emphasis('unbanned') + '!')
            input('\n')

        elif choice == '3':
            os.system('cls')
            print(emphasis('View all actions...\n'))

            actions = Database.get_actions()
            headers = ['Name', 'DateTime', 'Username']

            print(tabulate(actions, headers=list(map(emphasis, headers))))
            input('\n')

        elif choice == '4':
            os.system('cls')
            print(emphasis('View some client\'s actions...\n'))
            
            while True:
                username = input('Enter ' + emphasis('username') + ': ')
                actions = Database.get_client_actions(username)
                print('')

                if actions is None:
                    print(error('Invalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    headers = ['Name', 'DateTime']
                    print(tabulate(actions, headers=list(map(emphasis, headers))))
                    input('\n')
                    break

        elif choice == '5':
            break


def admin(user: User):
    while True:
        os.system('cls')
        print('Hello, ' + emphasis('admin') + '!\n')

        print('What do you want?\n' +
            emphasis('1') + ' View all complaints\n' +
            emphasis('2') + ' View some client\'s complaints\n' +
            emphasis('3') + ' Edit some client\'s role to moderator\n' +
            emphasis('4') + ' Exit\n')
    
        while True:
            choice = input('Enter ' + emphasis('here: '))

            if choice == '1' or choice == '2' or choice == '3' or choice == '4':
                break
            else:
                print(error('\nInvalid data. Try again!')) 
                e = input('Do you want exit? (1) ')
                if e == '1':
                    break
                print('')

        if choice == '1':
            os.system('cls')
            print(emphasis('View all complaints...\n'))

            complaints = Database.get_complaints()
            headers = ['Id', 'Content', 'Username']
            
            print(tabulate(complaints, headers=list(map(emphasis, headers))))
            input('\n')

        elif choice == '2':
            os.system('cls')
            print(emphasis('View some client\'s complaints...\n'))
            
            while True:
                username = input('Enter ' + emphasis('username') + ': ')
                complaints = Database.get_client_complaints(username)
                print('')

                if complaints is None:
                    print(error('Invalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    headers = ['Id', 'Content']
                    print(tabulate(complaints, headers=list(map(emphasis, headers))))
                    input('\n')
                    break

        elif choice == '3':
            os.system('cls')
            print(emphasis('Edit some client\'s role to moderator\n'))
            
            while True:
                username = input('Enter ' + emphasis('username') + ': ')
                print('')

                result = Database.edit_client_role(username)

                if not result:
                    print(error('Invalid data. Try again!')) 
                    e = input('Do you want exit? (1) ')
                    if e == '1':
                        break
                    print('')
                else:
                    print('This client was succesfully turned into ' + emphasis('moderator') + '!')
                    input('\n')
                    break

        elif choice == '4':
            break
