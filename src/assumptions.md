# Assumptions

## Auth.py

  1. When registering, the user is also automatically logged in.
  2. Invalid token when logging out raises an AccessError
  3. Input paramters are not None

## channels.py 
  1. Channel can only be created when user info in data exists 
  2. Owners are also apart of the members list 
 