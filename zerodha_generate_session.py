# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:34:52 2019

@author: udish
"""
from kiteconnect import KiteConnect
import pickle



# After opening the kite website and logging in we get the request key
# We will now generate a session using the request_token generated
api_key="zka582z590jag8yh"

secret_key="9zdlmklim6rsakd2fkhay59hybsm5mw6"


# Load the pickle object saved earlier
with open("z.pkl",'rb') as z:
    kite=pickle.load(z)
    
# Generate the session using the request_token from the websites URL
data = kite.generate_session(api_secret=secret_key,request_token="UqlNvvBih68Tdp8Fsb5IApEYPrwyBk65")
kite.set_access_token(data["access_token"])

# Save the kite object for further use
with open("z.pkl",'wb') as z:
    pickle.dump(kite,z)