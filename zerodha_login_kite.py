# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 21:46:31 2019

@author: udish
"""

#This has to be run manually everyday in the morning
from kiteconnect import KiteConnect
import pickle

# The api_key and secret_key are fixed for a user 
# and are activated when we subscribe by paying monthly 2500
api_key="zka582z590jag8yh"

secret_key="9zdlmklim6rsakd2fkhay59hybsm5mw6"


# Connect with Zerodha API using Kite
kite = KiteConnect(api_key,secret_key)



# Click on the url after logging-in to zerodha kite to get the request token
print(kite.login_url())

# Saving the kite object now to access later 
# using the request_token generated from the link
with open("z.pkl",'wb') as z:
    pickle.dump(kite,z)
    
    




