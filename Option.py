#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import numpy as np
import matplotlib.pyplot as plt

class Option(object):
    def __init__(self, S0, K, r, T, N, params):
        self.S0 = S0 
        self.K = K
        self.r = r
        self.T = T
        self.N = max(1, N) 
        self.STs = None # Stock Price Tree
        
        # These parameters will be inherited to BinomialPricing and trinomialpricing codes
        self.pu = params.get("pu", 0)  #Up state probability 
        self.pd = params.get("pd", 0)  #Down state prob
        self.div = params.get("div", 0)  #Dividend yield
        self.sigma = params.get("sigma", 0)  #Volatility
        self.is_call = params.get("is_call", True)  # Type of option(call or put)
        self.is_european = params.get("is_eu", True)  #Type of option(European or American)

        self.dt = T/float(N)  # time steps
        self.df = math.exp(
            -(r-self.div) * self.dt)  # Discount factor


# In[ ]:




