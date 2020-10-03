import channel 
import auth
from error import InputError
import data

def channels_list(token):




    '''
    return {
        'channels': [
            {
                'channel_id': 2,
                'name': 'My Channel',
            }
        ],
    }
    '''

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }


def channels_create(token, name, is_public):
    #Check if name is more than 20 characters long and raise InputError
    if len(name) > 20: 
        raise InputError
    #Use token to get owner's u_id, name_first, and name_last
    channel_owner_user_id = data.data['tokens'][token]
    channel_owner_name_first = data.data['users'][channel_owner_user_id]['name_first']
    channel_owner_name_last = data.data['users'][channel_owner_user_id]['name_last']

    #Checks if data dictionary has a 'channels' key, if it doesn't -
    #The statement will add a new/empty 'channels' key accomponied by an empty list
    if data.data.get('channels') == None:
        data.data['channels'] = []

    #Initialisation of new channel with its name and is_public bool 
    new_channel = {
        'id': 1,
        'name': name,
        'members': [],
        'owners': [],
        'is public': is_public,
        'messages': {}, #Empty for Iteration 1
    }

    #Setting the owner's detail 
    owner_details = {
        'u_id': channel_owner_user_id,
        'name_first': channel_owner_name_first,
        'name_last': channel_owner_name_last,
    }

    #Add new_channel to 'channels' list:
        #if there are no channels add our new_channel created and 
        #else set a new unique channel id and then add the new_channel created above
        #in both cases, append the owner's details to both owners and members list 
    if data.data['channels'] is False:
        #Keeping track of channel_id to return it later
        channel_id = new_channel['id'] 
        data.data['channels'][0]['owners'].append(owner_details)
        data.data['channels'][0]['members'].append(owner_details)
        data.data['channels'].append(new_channel)
    else:
        #Check to see if channel id already exists - if it does:
            #keep adding 1 to new_channel id until it is unique
        for channel_id_searcher in data.data['channels'][channel_id_searcher]:
            if new_channel['id'] == data.data['channels'][channel_id_searcher]['id']:
                new_channel['id'] + 1
            else:
                channel_id = new_channel['id']
                data.data['channels'][channel_id_searcher]['owners'].append(owner_details)
                data.data['channels'][channel_id_searcher]['members'].append(owner_details)
                data.data['channels'].append(new_channel)

    return channel_id 

