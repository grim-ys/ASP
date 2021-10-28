#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import numpy as np
from BinomialPricing import BinomialTree

class TrinomialTree(BinomialTree):

    def _setup_parameters_(self):
        self.u = math.exp(self.sigma*math.sqrt(2.*self.dt))
        self.d = 1/self.u
        self.m = 1
        self.qu = ((math.exp((self.r-self.div) *
                             self.dt/2.) -
                    math.exp(-self.sigma *
                             math.sqrt(self.dt/2.))) /
                   (math.exp(self.sigma *
                             math.sqrt(self.dt/2.)) -
                    math.exp(-self.sigma *
                             math.sqrt(self.dt/2.))))**2
        self.qd = ((math.exp(self.sigma *
                             math.sqrt(self.dt/2.)) -
                    math.exp((self.r-self.div) *
                             self.dt/2.)) /
                   (math.exp(self.sigma *
                             math.sqrt(self.dt/2.)) -
                    math.exp(-self.sigma *
                             math.sqrt(self.dt/2.))))**2.

        self.qm = 1 - self.qu - self.qd

    def _initialize_stock_price_tree_(self):
        self.STs = [np.array([self.S0])]

        for i in range(self.N):
            prev_nodes = self.STs[-1]
            self.ST = np.concatenate(
                (prev_nodes*self.u, [prev_nodes[-1]*self.m,
                                     prev_nodes[-1]*self.d]))
            self.STs.append(self.ST)

    def _traverse_tree_(self, payoffs):
        for i in reversed(range(self.N)):
            payoffs = (payoffs[:-2] * self.qu +
                       payoffs[1:-1] * self.qm +
                       payoffs[2:] * self.qd) * self.df

            if not self.is_european:
                payoffs = self.__check_early_exercise__(payoffs,
                                                        i)

        return payoffs


# In[7]:


if __name__ == "__main__":
    from TrinomialPricing import TrinomialTree
    print("Price of European put:", TrinomialTree(
        100, 80, 0.06, 0.5, 2, {"sigma": 0.3, "is_call": False}).price())
    print("Price of American put:", TrinomialTree(
        100, 80, 0.06, 0.5, 2,  {"sigma": 0.3, "is_call": False, "is_eu": False}).price())


# In[ ]:




