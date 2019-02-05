from connector.configurator import Configurator

#on windows you will need to pass path to chromedriver to configurator,
# download the driver from https://chromedriver.storage.googleapis.com/index.html?path=2.46/
config = Configurator()
config.get_config()

#you can even create a new kite object using kite = KiteConnect(api_key,secret_key)
# and set the access token to config.access_token
NFO_data= config.kite.instruments("NFO")


fut_s={}
for i in range(len(NFO_data)):
    if((NFO_data[i]["tradingsymbol"].startswith("ICICI"))&(NFO_data[i]['instrument_type']=='FUT')):
        fut_s[NFO_data[i]["expiry"]]=NFO_data[i]["instrument_token"]

instrument_token=fut_s[max(fut_s.keys())]

print(instrument_token)