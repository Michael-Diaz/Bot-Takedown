import sys
import fbchat
from getpass import getpass
from random import seed
from random import random
import time


# Login
username = input("Username: ")
client = fbchat.Client(username, getpass())


# User Search
target_name = input('\nWho will recieve the text: ')
print()
possible_targets = client.searchForUsers(target_name)

friends = [];
for people in possible_targets:
    if people.is_friend == True:
        friends.append(people)

if len(friends) == 0:
    sys.exit(f'\n**No friend results found for {target_name}**\nShutting down...')

j = 1;
for friend in friends:
    print(f'{j}. {friend.name}')
    j += 1


# Recipent Selection
index = int(input('\nWhich person is the recipient [#, -1 to cancel]: '))

if index == -1:
    sys.exit('\n**Cancelled**\nShutting down...')
elif index > len(friends) or index < -1:
    sys.exit('\n**Invalid selection**\nShutting down...')

recipient = friends[index - 1]

print(f'\nSelected: [{recipient.name}]')
confirmation = input(f'Please confirm that you wish to send a message to {recipient.first_name} [Y/n]: ').lower()

if confirmation == 'n':
    sys.exit('\n**Cancelled**\nShutting down...')
elif confirmation != 'y':
    sys.exit('\n**Invalid Input**\nShutting down...')


# Package Selection
# NOTE: If you wish to add your own custom text, create a text file in the "packages" folder
#       and add an entry to the list in the format shown below
packages = [
    {'name': 'The Entire Bee Movie Script', 'abr_name': 'Bee Movie Script', 'file_name': 'Bee_Movie.txt'}
    {'name': 'The Entire Shrek Script', 'abr_name': 'Shrek Script', 'file_name': 'Shrek.txt'}
]

k = 1
print()
for package in packages:
    print(f'{k}. {packages[k - 1]["name"]}')
    k += 1

index = int(input(f'\nSelect the text to be sent to {recipient.name} [#, -1 to cancel]: '))
if index == -1:
    sys.exit('\n**Cancelled**\nShutting down...')
elif index > len(packages) or index < -1:
    sys.exit('\**Invalid selection**\nShutting down...')

package = packages[index - 1]

print(f'\nConfirm the following:\nTo {recipient.first_name} <- \"{package["abr_name"]}\"')
confirmation = input('\n[Y/n]: ').lower()

if confirmation == 'n':
    sys.exit('\n**Cancelled**\nShutting down...')
elif confirmation != 'y':
    sys.exit('\n**Invalid Input**\nShutting down...')


# Transmission
payload = 'packages/' + package["file_name"]
file = open(payload, 'r')

pause = 0.0
for line in file:
    for word in line.split():
        pause = random() * 2.5
        sent = client.sendMessage(word, thread_id = recipient.uid)
        if not sent:
            sys.exit('\n**Error in sending message**\nShutting down...')
        time.sleep(pause)

print('\n**Message sent successfully**\nShutting down...')
file.close()
