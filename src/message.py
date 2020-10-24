from error import InputError, AccessError
import data
import datetime

def message_send(token, channel_id, message):
    #Check if message length is not more than 1000.
    if len(message) > 1000:
        raise InputError

    #Check if user is a member of the channel.
    #If so, they are authorised to send messages to the channel. 
    user_id = data.data['tokens'][token]
    check_if_valid_channel_and_member(channel_id, user_id)

    #Assigning attribute data to message entity - to then later be stored in data.py 
    date = datetime.datetime.now() 
    time_created = date.timestamp() 
    data.message_id += 1
    message_id = data.message_id
    new_message = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created,
    }
    
    #Append the new_message to data
    for channel in data.data['channels']:
        if channel_id == channel['id']:
            channel['messages'].append(new_message)

    return {
        'message_id': message_id,
    }


def message_remove(token, message_id):

    #Check if message user is trying to remove no longer exists - if so, raise InputError
    check_if_message_exists(message_id)

    #Remove message - however if the user did not create the message OR is not an owner of the channel the message is in, raise AccessError 
    user_id = data.data['tokens'][token]
    for channel in data.data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id'] and user_id == message['u_id']: 
                channel['messages'].remove(message)
            elif check_if_user_is_owner(channel['id'], user_id) is True:
                channel['messages'].remove(message)
            else: #If neither of the above statements are True, the user is not authorised to remove the message
                raise AccessError
    return {}
    
def message_edit(token, message_id, message):

    if message is None or message is '':
        message_remove(token, message_id)
        return {}

    user_id = data.data['tokens'][token]
    for channel in data.data['channels']:
        for messages in channel['messages']:
            if message_id == messages['message_id'] and user_id == messages['u_id']:
                messages['message'] = message
            elif check_if_user_is_owner(channel['id'], user_id) is True:
                messages['message'] = message
            else: #User is not authorised to edit the message
                raise AccessError
    return {}

#Credit: Taken from channel.py - the file Shree and Vignaraj have worked on
#The function checks if the user is a member of the channel. 
def check_if_valid_channel_and_member(channel_id, u_id):
    # loop through channels to find channel with channel_id
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            # if u_id is not a member chuck an AccessError
            if not any(member['u_id'] == u_id for member in channel['members']):
                raise AccessError
            return

#Very similar to above function - however checks if a message exists in data
def check_if_message_exists(message_id): 
    for channel in data.data['channels']: 
        if not any(message['message_id'] == message_id for message in channel['messages']):
            raise InputError
        return

def check_if_user_is_owner(channel_id, user_id):
    for channel in data.data['channels']:
        if channel_id == channel['id']:
            if not any(owner['u_id'] == user_id for owner in channel['owners']):
                return False
    return True