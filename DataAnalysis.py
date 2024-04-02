#!/usr/bin/env python
# coding: utf-8

# In[1]:


#in this document we will check for correlation; Tableau is mostly used for Graphs
import pandas as pd


# In[2]:


#first we merge our file with our AirQuality webscraping
mergedFile = pd.read_csv('finalMerge.csv')
AirPol = pd.read_csv('AQI.csv')


# In[3]:


mergedFile.head()


# In[4]:


AirPol.head()


# In[5]:


#we will merge our files with our airpollution data
dfData = pd.merge(mergedFile,AirPol, on = 'Date', how = 'inner' )


# In[6]:


dfData.head()


# In[8]:


#ok now let's remove the unnamed column
dfData.drop(columns = 'Unnamed: 0', inplace  = True)
dfData.head()


# In[9]:


#rename our air quality column
dfData.rename(columns={'aqi': 'Air Quality Index'}, inplace=True)
dfData.head()


# In[10]:


#we will now create a correlation matrix

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[11]:


#first let's see what values are strings or floats
dfData.dtypes


# In[12]:


Nums = dfData.select_dtypes(include=['number'])
CorMat = Nums.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(CorMat, vmax=1, square=True);


# In[13]:


dfData['Need States'] = dfData['Need States'].str.extract('(\d+)').astype(int)


# In[14]:


dfData.head()


# In[15]:


#now we upload our weather data and do the same merge
weathData = pd.read_csv('weather_data.csv')
weathData.head()


# In[16]:


weathData.rename(columns={'date': 'Date'}, inplace=True)


# In[17]:


dfData = pd.merge(dfData,weathData, on = 'Date', how = 'inner')


# In[18]:


dfData.head()


# In[19]:


dfData.to_csv('allData.csv')


# In[20]:


dfData.dtypes


# In[21]:


dfData.drop(columns = 'Unnamed: 0', inplace  = True)
dfData.head()


# In[22]:


Nums = dfData.select_dtypes(include=['number'])
CorMat = Nums.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(CorMat, vmax=1, square=True);


# In[23]:


CorMat.round(4)


# In[24]:


#let's see if we can find some correlation with each specific need state
NeedState1 = dfData[dfData['Need States']==1]
NeedState1


# In[25]:


dfwd = pd.get_dummies(dfData, columns = ['Need States'])


# In[26]:


dfwd = dfwd.applymap(lambda x: 1 if x is True else (0 if x is False else x))


# In[27]:


#we are adding dummies
dfwd


# In[28]:


Nums = dfwd.select_dtypes(include=['number'])
CorMat = Nums.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(CorMat, vmax=1, square=True);


# In[29]:


#correlation matrix for Need State 1

NS1Nums = NeedState1.select_dtypes(include=['number'])
CorMatNS1 = NS1Nums.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(CorMatNS1, vmax=1, square=True);


# In[30]:


NeedState2 = dfData[dfData['Need States']==2]
NeedState2


# In[31]:


NS2Nums = NeedState2.select_dtypes(include=['number'])
CorMatNS2 = NS2Nums.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(CorMatNS2, vmax=1, square=True);


# In[32]:


dfwd.to_csv('Final Data Set with Dummies.csv')


# In[ ]:




