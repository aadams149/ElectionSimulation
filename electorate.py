#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Electorate:
    
    def __init__(self,demographic_groups,proportions):
        self._demographic_groups = demographic_groups
        self._proportions = proportions
        
    def create_electorate(n_voters,demographic_groups,proportions):
        
        if sum(proportions) != 1:
            raise ValueError('Proportions do not sum to 1.')
        if len(demographic_groups) != len(proportions):
            raise ValueError('Number of demographic groups must equal number of proportions')
        
        proportions = [int(round(x*n_voters,0)) for x in proportions]
        electorate = dict(zip(demographic_groups,proportions))
        return(electorate)

