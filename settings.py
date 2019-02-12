start_time = (9, 30, 0)
end_time = (15, 30, 0)

def keys ():
    return [{'api_key': "zka582z590jag8yh", 'secret_key': "9zdlmklim6rsakd2fkhay59hybsm5mw6", 'u_id': "RD0291",
         'password': "Divakar@1983"}]

def get_tradables():
    return [{"symbol_name": "ICICI","interval" : "minute" ,"model_path": "../resources/pkls/icici.pkl","instrument_type":"FUT" , "transformation" : "icic_fut_transform" }]

chrome_driver_path = None
#if there are multiple instruments being traded ata a time , usually a lapse time is set between each to reduce overload on the network connections.
intra_action_delta =15
#runs pending jobs every one second  or so you dont want this to be too frequent
execution_heart_beat= 1
#time between two pings to the server for updating data
schedule_heart_beat = 60
info_log_path= '../logger/logs/info.log'
debug_log_path='../logger/logs/debug.log'
error_log_path='../logger/logs/error.log'