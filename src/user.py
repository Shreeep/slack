import data
import re
import copy
import urllib.request
import os
from PIL import Image
from error import InputError, AccessError


def user_profile(token, u_id):
    
    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid u_id
    if u_id not in data.data['users']:
        raise InputError

    if data.data['tokens'][token] != u_id:
        raise AccessError

    u_id = data.data['tokens'][token]

    profile = data.data['users'][u_id]

    # profile = copy.deepcopy(data.data['users'][u_id])

    # result = {}

    # for key in profile:
    #     if key != 'password' and key != 'is_global_owner':
    #         result[key] = profile[key]

    profile.pop('password')
    profile.pop('is_global_owner')


    return profile

def user_profile_setname(token, name_first, name_last):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # first name is between 1 - 50
    if len(name_first) < data.MIN_NAME_LEN or len(name_first) > data.MAX_NAME_LEN: 
        raise InputError

    # last name is between 1 - 50
    if len(name_last) < data.MIN_NAME_LEN or len(name_last) > data.MAX_NAME_LEN:
        raise InputError

    user_id = data.data['tokens'][token]
    profile = data.data['users'][user_id]

    profile['name_first'] = name_first
    profile['name_last'] = name_last

    return {
    }

def user_profile_setemail(token, email):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid email
    if not re.search(data.EMAIL_REGEX,email):
        raise InputError

    # checking if email has been used
    for user in data.data['users']:
        if email == data.data['users'][user]['email']:
            raise InputError
       
    user_id = data.data['tokens'][token]
    profile = data.data['users'][user_id]

    profile['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    if len(handle_str) > data.MAX_HANDLE_LEN or len(handle_str) < data.MIN_HANDLE_LEN:
        raise InputError

    # check if handle is used
    if handle_str in data.data['handles']:
        raise InputError
    
    # Saves the handle name
    user_id = data.data['tokens'][token]
    
    profile = data.data['users'][user_id]

    profile['handle_str'] = handle_str
    data.data['handles'][handle_str] = True

    return {
    }   


def user_profile_upload_photo(token, img_url, x_start, y_start, x_end, y_end):
  
    # create folder called if not found
    if os.path.exists('src/static') is False:
        os.mkdir('src/static')

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    u_id = data.data['tokens'][token] 

    # check img is a jpg
    if '.jpg' not in img_url:
        raise InputError

    # get img and open it
    urllib.request.urlretrieve(img_url, f'src/static/{u_id}.jpg')
    img = Image.open(f'src/static/{u_id}.jpg')

    # crop image
    cropped = img.crop((x_start, y_start, x_end, y_end))

    # check crop size is within image
    if x_start < 0 or x_start > img.size[0]:
        raise InputError

    if y_start < 0 or y_start > img.size[1]:
        raise InputError

    if x_end < 0 or x_end > img.size[0]:
        raise InputError

    if y_end < 0 or y_end > img.size[1]:
        raise InputError

    # save img in the folder
    cropped.save(f'src/static/{u_id}.jpg')

    # print(profile_img_url)

    data.data['users'][u_id]['profile_img_url'] = str(f'localhost:/static/{u_id}.jpg')

    # print(data.data)


# import auth
# ret = auth.auth_register('test@email.com', 'password', 'test', 'user')
# token = ret['token']
# print(token)
# user_profile_upload_photo(token, 'https://www.courant.com/resizer/D9qmAnzR8PY5q-GBdUBBVuNVUTs=/415x311/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/NTWCZKYTDJBI7CASRJ32F2RN6E.jpg', 0, 0, 200, 200)

# user_profile_upload_photo(token, 'https://pngimg.com/uploads/shrek/shrek_PNG40.png', 0, 0, 200, 200)

# print(user_profile_upload_photo)




