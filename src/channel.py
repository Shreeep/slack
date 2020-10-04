import data
import error


def channel_invite(token, channel_id, u_id):
    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):

    auth_user_id = data.data['tokens'][token]


    #input error if channel_id is not a valid channel
    if not any(channel['id'] == channel_id for channel in data.data['channels']):
        raise InputError

    #access error auth_user is not a member of the channel with channel_id
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not any(auth_user_id == member['u_id'] for member in channel['members']):
                raise AccessError

    #acess error if token is not a valid token
    if not token in data.data['tokens']:
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
                if channel[is_public] == False:
                    raise AccessError

    #acess error if token is not a valid token
    if not token in data.data['tokens']:
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
                channel['owner'].append(new_member)
    return {
    }

def channel_addowner(token, channel_id, u_id):

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


    #acess error if token is not a valid token
    if not token in data.data['tokens']:
        raise AccessError

    name_first = data.data['users'][u_id][name_first]
    name_last = data.data['users'][u_id][name_last]

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
    for channel in data.data['channels']
        if channel['id'] == channel_id:
            channel['owners'].append(new_owner)


    return {
    }

def channel_removeowner(token, channel_id, u_id):

    auth_user_id = data.data['tokens'][token]

    #input error when a)channel ID is not a valid channel
    if not any(channel['id'] == channel_id for channel in data.data['channels']):
        raise InputError
    #input error when b) u_id is already an owner of the channel
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if any(u_id == owner['u_id'] for owner in channel['owners']):
                raise InputError
    #access error when auth_user is not an owner of the channel or global owner
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not (any(auth_user_id == owner['u_id'] for owner in channel['owners'])) or (data.data['users'][auth_user_id]['is_global_owner']):
                raise AccessError

    #acess error if token is not a valid token
    if not token in data.data['tokens']:
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
