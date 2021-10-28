#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import numpy as np
import matplotlib.pyplot as plt
from Option import Option


# This code is for comparison with Trinomial Tree pricing method and inheriting parameters and methods,
#which are common in both methods

class BinomialTree(Option):

    def _setup_parameters_(self):
        self.u = 1 + self.pu  
        self.d = 1 - self.pd  
        self.qu = (math.exp((self.r-self.div)*self.dt) -
                   self.d)/(self.u-self.d)
        self.qd = 1-self.qu

    def _initialize_stock_price_tree_(self):
        
        self.STs = [np.array([self.S0])]

        
        for i in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate((prev_branches*self.u,
                                 [prev_branches[-1]*self.d]))
            self.STs.append(st)  

    def _initialize_payoffs_tree_(self):
        
        return np.maximum(
            0, (self.STs[self.N]-self.K) if self.is_call
            else (self.K-self.STs[self.N]))

    def __check_early_exercise__(self, payoffs, node):
        early_ex_payoff =             (self.STs[node] - self.K) if self.is_call             else (self.K - self.STs[node])

        return np.maximum(payoffs, early_ex_payoff)

    def _traverse_tree_(self, payoffs):
        for i in reversed(range(self.N)):
            
            payoffs = (payoffs[:-1] * self.qu +
                       payoffs[1:] * self.qd) * self.df

            
            if not self.is_european:
                payoffs = self.__check_early_exercise__(payoffs,
                                                        i)

        return payoffs

    def __begin_tree_traversal__(self):
        payoffs = self._initialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)

    def price(self):
        self._setup_parameters_()
        self._initialize_stock_price_tree_()
        payoffs = self.__begin_tree_traversal__()

        return payoffs[0]


# In[6]:


if __name__ == "__main__":
    from BinomialPricing import BinomialTree
    am_option = BinomialTree(
        100, 80, 0.06, 0.5, 2,
        {"pu": 0.2, "pd": 0.2, "is_call": False, "is_eu": False})
    print("Price of American option:", am_option.price())


# In[ ]:




