import channel 
import auth
import error 
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

    #Parameters: 
        #a string token which is associated with the user creating the channel
        #a string name which is name of the channel
        #a boolean is_public which is whether the channel is public or private
    #A channel has the following characteristics: 
        #channel id
        #name of the channel
        #its members 
        #its owners 
        #should be both in members and owners list 
        #if its public or not
        #messages (can be blank for now)
    #Assumption: owners and members are together
    #Purpose of this function:
    #Parameters --> Characteristics of channel --> Return channel_id 

    #Step 1: Find the user id associated with the token in data
    channel_owner_user_id = data.data['tokens'][token]
    #Step 2: set channel id to some number (discuss with team)
    channel_id = data.data['channels']
    #Step 3: Add this user to owner AND members list within channel 

    #Step 4: set is_public in data = is_public passed thru this function
    #Step 5: set channel name to 'name' passed thru this function
    #Step 6: return this channel id 


    '''
    return {
        'channel_id': 1,
    }
    '''
