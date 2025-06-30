# To get the flask session key, run this file and take the key printed on terminal
# Further, make a .env file in the same directory as this file and add the following line:
# SECRET_KEY=your_generated_key_here
# Replace 'your_generated_key_here' with the key printed by this script.

import secrets

session_key = secrets.token_hex(16)
print(session_key)