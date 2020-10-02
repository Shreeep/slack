#Notes for channels_* functions: 
    #channels_list is a subset of channels_listall
    #channels_list and channels_listall return a list of dictionaries, where each dictionary contains {channel_id, name}
    #Test Cases for channels_list(): 
        #User is apart of a channel - returns that channel 
        #No channels the user is apart of - returns an empty list 
        #User is apart of all channels - returns list of all channels 
        #User is apart of some channels, not all - returns list which is subset of all channels 
    #Test Cases for channels_listall():
        #No channels asscociated with the token - returns empty list
    #Test Cases for channels_create(): 
        #Channels can have same name - their differing quality is their channel ID
        #Channel name is above 20 characters 
        #Assumption: whoever creates the channel is already a member (quite obvious)
