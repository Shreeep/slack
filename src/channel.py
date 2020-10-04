import data
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError
    # check for valid u_id
    if not u_id in data.data['users']:
        raise InputError
    # find target user and token user
    target_user = data.data['users'][u_id]
    user_id = data.data['tokens'][token]
    # check if valid channel and user is member
    check_if_valid_channel_and_member(channel_id, user_id)
    # construct member entry
    member_dict = {
        'u_id': u_id,
        'name_first': target_user['name_first'],
        'name_last': target_user['name_last'],
    }
    # add member to channel if he is already not there
    all_channels = data.data['channels']
    for channel in all_channels:
        if channel['id'] == channel_id:
            if not any(u_id == member['u_id'] for member in channel['members']): 
                channel['members'].append(member_dict)        
    return {
    }

def channel_details(token, channel_id):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError
    # find user in token dictionary
    u_id = data.data['tokens'][token]
    # check if valid channel and user is member
    check_if_valid_channel_and_member(channel_id, u_id)
    # find channel and result it's details
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            result = {
                'name': channel['name'],
                'owner_members': channel['owners'],
                'all_members': channel['members'],
            }
            break
    return result

def channel_messages(token, channel_id, start):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError
    # find user in token dictionary
    u_id = data.data['tokens'][token]
    # check if valid channel and user is member
    check_if_valid_channel_and_member(channel_id, u_id)
    # find the messages list in specific channel
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            messages = channel['messages']
            break
    # find messages of span of start -> start + 50
    span = 50
    result = []
    # raise error if start index is outside range of messages
    if start >= len(messages):
        raise InputError
    # copy messages until reached 50 or end of messages list
    for i in range(span):
        index = i + start
        if index > len(messages) - 1:
            break
        result.append(messages[index])
    # if did not reach 50 then end is -1 other wise start + 50
    if (index - start) != 49:
        end = -1
    else:
        end = start + 50        
    return {
        'messages': result,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }

# test if channel exists and if u_id is in channel
def check_if_valid_channel_and_member(channel_id, u_id):
    # loop through channels to find channel with channel_id
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            # if u_id is not a member chuck an AccessError
            if not any(member['u_id'] == u_id for member in channel['members']):
                raise AccessError
            return
    raise InputError