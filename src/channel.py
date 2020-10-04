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
    messages = []
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            messages = channel['messages']
            break
    # find messages of span of start -> start + 50
    result = []
    # raise error if start index is outside range of messages
    if start >= len(messages):
        raise InputError
    # copy messages until reached 50 or end of messages list
    index = start
    for i in range(50):
        if index > len(messages) - 1:
            break
        result.append(messages[index])
        index += 1
    # if did not reach 50 then end is -1 other wise start + 50
    if ((index - start) == 50):
        end = start + 50
    else:
        end = -1        
    return {
        'messages': result,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    #acess error if token is not a valid token
    if not token in data.data['tokens']:
        raise AccessError

    auth_user_id = data.data['tokens'][token]

    #input error if channel_id is not a valid channel
    if not any(channel['id'] == channel_id for channel in data.data['channels']):
        raise InputError

    #access error auth_user is not a member of the channel with channel_id
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not any(auth_user_id == member['u_id'] for member in channel['members']):
                raise AccessError

    #searching for the correct channel
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            #remove the auth user from the channel
            for member in channel['members']:
                if member['u_id'] == auth_user_id:
                    #removing the user from the channel
                    channel['members'].remove(member)

            #if the user is an owner, also remove them from owners
            for owner in channel['owners']:
                if owner['u_id'] == auth_user_id:
                    #removing the user from the channel
                    channel['owners'].remove(owner)


    return {
    }


def channel_join(token, channel_id):
    #acess error if token is not a valid token
    if not token in data.data['tokens']:
        raise AccessError

    #retrieving user data
    auth_user_id = data.data['tokens'][token]
    name_first = data.data['users'][auth_user_id]['name_first']
    name_last = data.data['users'][auth_user_id]['name_last']

    #input error if channel_id is not a valid channel
    if not any(channel['id'] == channel_id for channel in data.data['channels']):
        raise InputError
    #access error when channel_id refers to a channel that
    #is private (when the authorised user is not a global owner)
    #if user is not global owner
    if not data.data['users'][auth_user_id]['is_global_owner']:
        #search for the channel
        for channel in data.data['channels']:
            if channel['id'] == channel_id:
                #if this channel is private, raise an accessError
                if channel['is_public'] == False:
                    raise AccessError

    new_member = {
        'u_id' : auth_user_id,
        'name_first': name_first,
        'name_last': name_last
    }

    #searching for the correct channel
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            #add user to this channel
            channel['members'].append(new_member)
            #if user is global_owner, also add auth user as owner
            if data.data['users'][auth_user_id]['is_global_owner']:
                channel['owners'].append(new_member)
    return {
    }

def channel_addowner(token, channel_id, u_id):

    #acess error if token is not a valid token
    if not token in data.data['tokens']:
        raise AccessError

    auth_user_id = data.data['tokens'][token]

    #input error when a)channel ID is not a valid channel
    if not any(channel['id'] == channel_id for channel in data.data['channels']):
        raise InputError
    #input error when b) u_id is already an owner of the channel
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if any(u_id == owner['u_id'] for owner in channel['owners']):
                raise InputError
    #access error when auth_user is not an owner of the channel or a global owner
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not ((any(auth_user_id == owner['u_id'] for owner in channel['owners'])) or (data.data['users'][auth_user_id]['is_global_owner'])):
                raise AccessError

    name_first = data.data['users'][u_id]['name_first']
    name_last = data.data['users'][u_id]['name_last']

    new_owner = {
        'u_id' : u_id,
        'name_first': name_first,
        'name_last': name_last
    }
    ## TODO: if user wasn't previously a member, add them as a member
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not any(u_id == member['u_id'] for member in channel['members']):
                channel['members'].append(new_owner)

    #add auth user to owers list
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            channel['owners'].append(new_owner)


    return {
    }

def channel_removeowner(token, channel_id, u_id):
    
    #acess error if token is not a valid token
    if not token in data.data['tokens']:
        raise AccessError

    auth_user_id = data.data['tokens'][token]

    #input error when a)channel ID is not a valid channel
    if not any(channel['id'] == channel_id for channel in data.data['channels']):
        raise InputError
    #input error when b) u_id is not an owner of the channel
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not any(u_id == owner['u_id'] for owner in channel['owners']):
                raise InputError
    #access error when auth_user is not an owner of the channel or global owner
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not ((any(auth_user_id == owner['u_id'] for owner in channel['owners'])) or (data.data['users'][auth_user_id]['is_global_owner'])):
                raise AccessError

    #search for channel with channel_id
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            #remove the user with u_id as a member
            for member in channel['members']:
                if member['u_id'] == u_id:
                    channel['members'].remove(member)

            #remove the user with u_id as an owner
            for owner in channel['owners']:
                if owner['u_id'] == u_id:
                    channel['owners'].remove(owner)


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
