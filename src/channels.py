from error import InputError, AccessError
import data

def channels_list(token):

    if not token in data.data['tokens']:
        raise AccessError

    #Intialise an empty dictionary that has a 'channels' list
    user_channels = {
        'channels':[]
    }

    #Get user's id, name_first, name_last to see if they are a member of a channel
    user_id = data.data['tokens'][token]
    user_info = {
        'u_id': user_id,
        'name_first': data.data['users'][user_id]['name_first'],
        'name_last': data.data['users'][user_id]['name_last'],
        'profile_img_url': data.data['users'][user_id]['profile_img_url']
    }
    

    #Search through each channel in data
    for channel in data.data['channels']:
        #Keep track of the current channel id and channel name
        #If we find that the user is apart of a particular channel - append it to our user_channels list
        channel_details = {
            'channel_id': channel['id'],
            'name': channel['name'],
        }
        #Look through members list since it covers all users
        for user_search in channel['members']:
            #Statement is true if the user in question is a member
            if user_info == user_search: 
                user_channels['channels'].append(channel_details)

    return user_channels
    


def channels_listall(token):

    if not token in data.data['tokens']:
        raise AccessError

    #Intialise an empty dictionary that has a 'channels' list
    all_channels = {
        'channels': []
    }

    #Search through each channel in data
    for channel in data.data['channels']:
        #Store the current channel's name and id
        channel_details = {
            'channel_id': channel['id'],
            'name': channel['name'],
        }
        #Add it to the all_channels list
        all_channels['channels'].append(channel_details)

    return all_channels


def channels_create(token, name, is_public):

    if not token in data.data['tokens']:
        raise AccessError
    #Check if name is more than 20 characters long and raise InputError
    if len(name) > 20:
        raise InputError
    #Use token to get owner's u_id, name_first, and name_last
    channel_owner_user_id = data.data['tokens'][token]
    channel_owner_name_first = data.data['users'][channel_owner_user_id]['name_first']
    channel_owner_name_last = data.data['users'][channel_owner_user_id]['name_last']
    channel_owner_profile_img_url = data.data['users'][channel_owner_user_id]['profile_img_url']

    #Initialisation of new channel with its name and is_public bool
    new_channel = {
        'id': 1,
        'name': name,
        'members': [],
        'owners': [],
        'is_public': is_public,
        'messages': [], #Empty for Iteration 1
        'is_active': False,
        'time_finish': 0,
        'standup_message': '',
    }

    #Setting the owner's detail
    owner_details = {
        'u_id': channel_owner_user_id,
        'name_first': channel_owner_name_first,
        'name_last': channel_owner_name_last,
        'profile_img_url': channel_owner_profile_img_url,
    }

    new_channel['members'].append(owner_details)
    new_channel['owners'].append(owner_details)

    #Add new_channel to 'channels' list:
    while any(channel['id'] == new_channel['id'] for channel in data.data['channels']):
        new_channel['id'] += 1
    data.data['channels'].append(new_channel)
    channel_id = new_channel['id'] 
    return {
        'channel_id': channel_id,
    } 
