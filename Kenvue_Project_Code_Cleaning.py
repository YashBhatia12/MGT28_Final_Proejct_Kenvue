#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
#we import the dataset; header indicates that our first two rows are to be regarded/used a multi-level index
df_cus_DC_inventory = pd.read_csv('Customer DC Inventory.csv', header = [0,1])
#we set our indexes using the columns and the header function
df_cus_DC_inventory = df_cus_DC_inventory.set_index([('Fiscal Year  /  Fiscal Week', 'Need State'), ('Unnamed: 1_level_0', 'Unnamed: 1_level_1')])
#.T means Transpose it switches the rows and columns to our preference
df_cus_DC_inventory = df_cus_DC_inventory.T
#convert the columns to a single index 
df_cus_DC_inventory = df_cus_DC_inventory.stack(0)
#reset the index in the dataframe
df_cus_DC_inventory = df_cus_DC_inventory.reset_index()
df_cus_DC_inventory = df_cus_DC_inventory.rename_axis(None, axis=1)
df_cus_DC_inventory = df_cus_DC_inventory.rename(columns={df_cus_DC_inventory.columns[0]: "Year", df_cus_DC_inventory.columns[1]: "Week", df_cus_DC_inventory.columns[2]: "Need States"})
#we create a new column called Date, this allows us to do the final merge based on Date, so that allow local (ie. common) variables come in the final merge
df_cus_DC_inventory['Date'] = pd.to_datetime(df_cus_DC_inventory["Year"].astype(str) + "-" + df_cus_DC_inventory["Week"].astype(str) + "-1", format='%Y-%U-%w')
#Swap columns to make it match with our existing data; and drop nulls
df_cus_DC_inventory = df_cus_DC_inventory.reindex(columns=['Year','Week','Date','Need States','Dc Amount','Store Amt On Hand'])
df_cus_DC_inventory = df_cus_DC_inventory.replace(to_replace=0, value=pd.NA)
df_cus_DC_inventory = df_cus_DC_inventory.dropna(axis=0)
df_cus_DC_inventory
df_cus_DC_inventory.to_csv('Cust_Cleaned_1.csv')
#now we do the same thing for the others
dfEcommPOS = pd.read_csv('Total Ecomm POS (Factory $).csv', header = [0,1])
#use the melt feature we learned from pandas
dfEcommPOS = dfEcommPOS.melt(id_vars = [('Unnamed: 1_level_0', 'Fiscal Year'), ('Unnamed: 0_level_0', 'Need State')])
#Let's rename our columns
dfEcommPOS = dfEcommPOS.rename(columns = {dfEcommPOS.columns[0]: 'Year', dfEcommPOS.columns[1]: 'Need States', dfEcommPOS.columns[3]: 'Week',dfEcommPOS.columns[4]: 'Ecomm POS - Factory $'})
#there's an extra column, let's remove it
dfEcommPOS = dfEcommPOS.drop(columns = ['variable_0'])
#check for ints/string
dfEcommPOS.dtypes
#since week is an 'object' it might hurt us later, conver to int
dfEcommPOS = dfEcommPOS.apply(pd.to_numeric,errors = 'ignore')
#since week is an 'object' it might hurt us later, conver to int
dfEcommPOS = dfEcommPOS.apply(pd.to_numeric,errors = 'ignore')
#now we can use datetime
dfEcommPOS['Date'] = pd.to_datetime(dfEcommPOS["Year"].astype(str) + "-" + dfEcommPOS["Week"].astype(str) + "-1", format='%Y-%U-%w')
dfFactoryPOS = pd.read_csv('Factory POS.csv', header = [0,1])
#using the same melt function we used before hand
dfFactoryPOS = dfFactoryPOS.melt(id_vars=[('Unnamed: 0_level_0', 'Need State'), ('Unnamed: 1_level_0', 'Fiscal Week')], value_vars=[('Fiscal Year', '2021'), ('Fiscal Year', '2022'), ('Fiscal Year', '2023')])
dfFactoryPOS = dfFactoryPOS.rename(columns={dfFactoryPOS.columns[0]: "Need States", dfFactoryPOS.columns[1]: "Week", dfFactoryPOS.columns[3]: "Year", dfFactoryPOS.columns[4]: "Factory POS"})
#drop the unwanted column
dfFactoryPOS = dfFactoryPOS.drop(columns = ['variable_0'])
#since week is an 'object' it might hurt us later, conver to int
dfFactoryPOS = dfFactoryPOS.apply(pd.to_numeric,errors = 'ignore')
#datetime function
dfFactoryPOS['Date'] = pd.to_datetime(dfFactoryPOS["Year"].astype(str) + "-" + dfFactoryPOS["Week"].astype(str) + "-1", format='%Y-%U-%w')
#Now we have to swap our columns; sort by year; drop our null values
dfFactoryPOS = dfFactoryPOS.reindex(columns=['Year','Week','Date','Need States','Factory POS'])
dfFactoryPOS = dfFactoryPOS.sort_values(by=['Year', 'Week'])
dfFactoryPOS = dfFactoryPOS.reset_index(drop=True)
dfFactoryPOS = dfFactoryPOS.replace(to_replace=0, value=pd.NA)
dfFactoryPOS = dfFactoryPOS.dropna(axis=0)
dfFactoryPOS = pd.read_csv('Factory POS.csv', header = [0,1])
dfFactoryPOS = dfFactoryPOS.melt(id_vars=[('Unnamed: 0_level_0', 'Need State'), ('Unnamed: 1_level_0', 'Fiscal Week')], value_vars=[('Fiscal Year', '2021'), ('Fiscal Year', '2022'), ('Fiscal Year', '2023')])
dfFactoryPOS = dfFactoryPOS.rename(columns={dfFactoryPOS.columns[0]: "Need States", dfFactoryPOS.columns[1]: "Week", dfFactoryPOS.columns[3]: "Year", dfFactoryPOS.columns[4]: "Factory POS"})
dfFactoryPOS = dfFactoryPOS.drop(columns = ['variable_0'])
dfFactoryPOS = dfFactoryPOS.apply(pd.to_numeric,errors = 'ignore')
dfFactoryPOS['Date'] = pd.to_datetime(dfFactoryPOS["Year"].astype(str) + "-" + dfFactoryPOS["Week"].astype(str) + "-1", format='%Y-%U-%w')
dfFactoryPOS = dfFactoryPOS.reindex(columns=['Year','Week','Date','Need States','Factory POS'])
dfFactoryPOS = dfFactoryPOS.sort_values(by=['Year', 'Week'])
dfFactoryPOS = dfFactoryPOS.reset_index(drop=True)
dfFactoryPOS = dfFactoryPOS.replace(to_replace=0, value=pd.NA)
dfFactoryPOS = dfFactoryPOS.dropna(axis=0)
dfTotalSales = pd.read_csv('Total Sales - UTSC Lecture.csv')
#using the same melt function
dfTotalSales = dfTotalSales.melt(id_vars = ['Fiscal Year', 'Fiscal Week'])
#rename our colums to a similar format as last time
dfTotalSales = dfTotalSales.rename(columns={dfTotalSales.columns[0]: "Year", dfTotalSales.columns[1]: "Week", dfTotalSales.columns[2]: "Need States", dfTotalSales.columns[3]: "Sales"})
#same datetime function for future plotting
dfTotalSales['Date'] = pd.to_datetime(dfTotalSales["Year"].astype(str) + "-" + dfTotalSales["Week"].astype(str) + "-1", format='%Y-%U-%w')
#swapping columns
dfTotalSales = dfTotalSales.reindex(columns=['Year','Week','Date','Need States','Sales'])
dfTotalSales = dfTotalSales.sort_values(by=['Year', 'Week'])
dfTotalSales = dfTotalSales.reset_index(drop=True)
dfTotalSales = dfTotalSales.replace(to_replace=0, value=pd.NA)
dfTotalSales = dfTotalSales.dropna(axis=0)


# In[3]:


dfTotalSales


# In[4]:


dfFactoryPOS


# In[5]:


dfEcommPOS


# In[6]:


df_cus_DC_inventory


# In[ ]:




