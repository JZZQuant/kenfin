# # -*- coding: utf-8 -*-
# """
# Created on Thu Feb  7 20:31:04 2019
#
# @author: udish
# """
#
# import pandas as pd
# import talib as ta
# from load_model import load_model
# import pickle
# import get_data_first_time as g
#
# with open("z.pkl",'rb') as z:
#     kite=pickle.load(z)
#
# # You need to provide the name for the model that you us eon your lcoal machine
#
#
# if signal==1:
#     g.trade_ce=True
#     g.trade_pe=False
#
# elif signal==-1:
#     g.trade_pe=True
#     g.trade_ce=False
#
# # Need to work on the exit
# if g.trade_ce==True:
#     if g.order_id==None:
#         g.order_id=kite.place_order(tradingsymbol=g.options_ce,quantity =g.contract['lot_size'],
#                               order_type="LIMIT",exchange="NSE",price=g.df.close.iloc[-1],
#                               transaction_type="BUY",product="MIS")
#
#
# if g.trade_pe==True:
#     if g.order_id==None:
#         g.order_id=kite.order_place(tradingsymbol=g.options_pe,quantity =g.contract['lot_size'],
#                               order_type="LIMIT",exchange="NSE",price=g.df.close.iloc[-1],
#                               transaction_type="BUY",product="MIS")