# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 20:29:30 2019

@author: udish
"""
import pickle

def load_model(model_saved_name):
    # Open the file containing the model with the mentioned name on the local machine
    with open(model_saved_name, 'rb') as file:
        # Load the model and assign it to a variable
        model=pickle.load(file)
        # Return the model
        return model