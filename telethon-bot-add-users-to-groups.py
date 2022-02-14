from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, ChatForbidden, UserStatusOffline
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import ReadHistoryRequest

import sys
import csv
import traceback
import time
import datetime
import random
import re


# App configuration
# App api_id:
# 13526775
# App api_hash:
# e240136f5a706ebceb86314b182e5440
# App title:
# Ares Protocol
# Short name:
# Ares12
# alphanumeric, 5-32 characters

api_id = 14775967        # YOUR API_ID
api_hash = '706ab27678d9ed45ca137ef253deddcb'        # YOUR API_HASH
phone = '+8618210008157'        # YOUR PHONE NUMBER, INCLUDING COUNTRY CODE
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

def add_users_to_group():
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            try:
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
            except IndexError:
                print ('users without id or access_hash')
            users.append(user)

    #random.shuffle(users)
    chats = []
    last_date = None
    chunk_size = 10
    groups=[]

    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True: # CONDITION TO ONLY LIST MEGA GROUPS.
                groups.append(chat)
        except:
            continue

    print('Choose a group to add members:')
    i=0
    for group in groups:
        print(str(i) + '- ' + group.title)
        i+=1

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]
    print('\n\nGrupo elegido:\t' + groups[int(g_index)].title)

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    error_count = 0

    for user in users:
        try:
            print ("Adding {}".format(user['username']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print("Waiting 60 Seconds...")
            time.sleep(60)
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            error_count += 1
            if error_count > 10:
                sys.exit('too many errors')
            continue

def list_users_in_group():
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)
    
    for chat in chats:
        try:
            print(chat)
            groups.append(chat)
            # if chat.megagroup== True:
        except:
            continue
    
    print('Choose a group to scrape members from:')
    i=0
    for g in groups:
        info = "[!!无权访问!!]" if isinstance(g, ChatForbidden) else ""
        print(str(i) + '- ' + g.title, info)
        i+=1
    
    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]

    print('\n\nGrupo elegido:\t' + groups[int(g_index)].title)
    print(target_group)
    print('Fetching Members... ')

    if isinstance(target_group, ChatForbidden):
        print("无权限访问")
        return

    # user_count = 0
    # for user in client.iter_participants(target_group):
    #     user_count+=1
    #     # print("测试：",user_count, user.id, user.username)
    #
    # print("测试结束 ………………………………………………………………")
    # return

    all_participants = []
    all_participants = client.get_participants(target_group)# aggressive=True

    print('Saving In file... count : ', len(all_participants))
    # with open("members-" + re.sub("-+","-",re.sub("[^a-zA-Z]","-",str.lower(target_group.title))) + ".csv","w",encoding='UTF-8') as f:
    with open( "members-{}-{}.csv".format(g_index, target_group.title), "w",
              encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username', 'name', 'group', 'status'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            if isinstance(user.status, UserStatusOffline):
                str_time_status = str(user.status.was_online)
                str_time = str_time_status.replace('+00:00', '')
                user_status = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
            else:
                user_status = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, name, target_group.title, user_status])
    print('Members scraped successfully.')

def printCSV():
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            users.append(user)
            print(row)
            print(user)
    sys.exit('FINITO')

# print('Fetching Members...')
# all_participants = []
# all_participants = client.get_participants(target_group, aggressive=True)
print('What do you want to do:')
mode = int(input("Enter \n1-List users in a group\n2-Add users from CSV to Group (CSV must be passed as a parameter to the script\n3-Show CSV\n\nYour option:  "))

if mode == 1:
    list_users_in_group()
elif mode == 2:
    add_users_to_group()
elif mode == 3:
    printCSV()
