# import auth
# import json
# from echo_http_test import url
# import server
# # import data
# from flask import Flask, request


# @APP.route("/auth/register", methods=['POST'])
# def register():
#     # get the info
#     user_info = request.get_json()

#     password = hashlib.sha256(user_info['password'].encode()).hexdigest()
#     user_token = auth.auth_register(user_info['email'], password, user_info['name_first'], user_info['name_last'])

#     encoded_jwt = jwt.encode(user_token['token'], password, algorithm='HS256')

#     return encoded_jwt
    

# @APP.route("/auth/login", methods=['POST'])
# def login():

#     # get user info
#     user_info = request.get_json()
    
#     # login
#     password = hashlib.sha256(user_info['password'].encode()).hexdigest()
#     user_token = auth.auth_login(user_info['email'], password)

#     encoded_jwt = jwt.encode(user_token['token'], password, algorithm='HS256')

#     return encoded_jwt


# @APP.route("/auth/logout", methods=['POST'])
# def logout():
    
#     return ""
#     # check generated token?
#     # decode generated token
#     # check if decoded token matches DB?

#     # get user info
#     user_info = request.get_json()

#     unique_token = generate_token(user_info['password'])

#     # how to check the user token??
#     # user_token = 

#     success = auth.auth_logout(user_token)

#     return success


