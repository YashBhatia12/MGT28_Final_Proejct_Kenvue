#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd


# In[5]:


#This is the merge; we will import all our cleaned datasets
dfCustClean = pd.read_csv('Cust_Cleaned_1.csv')
dfEcommClean = pd.read_csv('Cleaned_Ecomm_POS-1.csv')
dfFactoryClean = pd.read_csv('Factor_Cleaned_1.csv')
dfTotalSalesClean = pd.read_csv('TotalSales_Cleaned_1.csv')


# In[6]:


dfEcommClean


# In[7]:


dfCustClean


# In[8]:


dfEcommClean


# In[9]:


dfFactoryClean


# In[10]:


dfTotalSalesClean


# In[11]:


#when we see our data, note that Need State 6 is missing in Total Sales; for this reason we will drop it in the other data sets
#We'll just use != expression for this


# In[12]:


#there are some columns which need a case change, let's rename them
dfCustClean = dfCustClean.rename(columns={'year': 'Year', 'week':'Week'})
#We need to get rid of need state 6, it is not in the Total Sales csv
dfCustClean = dfCustClean[dfCustClean['Need States'] != 'Need State 6']
dfCustClean


# In[13]:


dfFactoryClean = dfFactoryClean[dfFactoryClean['Need States'] != 'Need State 6']
dfFactoryClean


# In[14]:


dfEcommClean = dfEcommClean.rename(columns={'Need State': 'Need States'})
dfEcommClean = dfEcommClean[dfEcommClean['Need States'] != 'Need State 6']
dfEcommClean


# In[15]:


#let's drop the 'Unnamed: 0 ' column
dfEcommClean = dfEcommClean.drop(columns=['Unnamed: 0'])
dfFactoryClean = dfFactoryClean.drop(columns=['Unnamed: 0'])
dfCustClean = dfCustClean.drop(columns=['Unnamed: 0'])
dfTotalSalesClean = dfTotalSalesClean.drop(columns=['Unnamed: 0'])


# In[16]:


#we start merging, we do not need to identify inner/outer bc it's already sorted on date and it would merge based on that
merger = pd.merge(dfCustClean,dfFactoryClean)
merger


# In[17]:


#we repeat until we get all the merges
merger = pd.merge(merger,dfEcommClean)
merger


# In[18]:


merger = pd.merge(merger,dfTotalSalesClean)


# In[19]:


merger


# In[20]:


merger.to_csv('finalMerge.csv')


# In[ ]:




