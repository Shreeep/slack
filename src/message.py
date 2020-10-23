from error import InputError, AccessError
import data
import datetime

'''
Assumptions:
    - message_id's are only unique in the scope of their respective channels
'''

def message_send(token, channel_id, message):
    if len(message) > 1000:
        raise InputError
    is_authorised = False
    #Check if user/token is allowed to message in channel/channel_id
    #i.e. check if user is a member or owner of the channel
    user_id = data.data['tokens'][token]
    for channel in data.data['channels']:
        if channel_id == channel['id']:
            for users in channel['members']:
                if user_id == users['u_id']:
                    is_authorised = True
                    break
        else:
            is_authorised = False
    if is_authorised is False:
        raise AccessError
    date = datetime.datetime.now() #datetime object
    time_created = date.timestamp() #converting to unix integer
    data.message_id += 1
    message_id = data.message_id
    new_message = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created
    }
    
    #Append new_message to specified channel
    for channel in data.data['channels']:
        if channel_id == channel['id']: #Find channel to append new_message to
            channel['messages'].append(new_message)

    return {
        'message_id': message_id
    }


def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }
