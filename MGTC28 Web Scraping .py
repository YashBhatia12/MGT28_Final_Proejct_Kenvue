#!/usr/bin/env python
# coding: utf-8

# # Scrape historical air pollution data for Toronto from January 1, 2021, to December 31, 2023 from OpenWeather

# In[2]:


# Import necessary libraries
import requests
from datetime import datetime, timedelta


# Define a function to fetch air pollution data
def fetch_air_pollution_data(start_date, end_date, lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution/history"
    data = [] # List to store fetched data
    
    
    # Initialize the current date to the start date
    current_date = start_date
    # Using while loop to loop through each day between the start and end dates
    while current_date <= end_date:
        # Calculate the next day for fetching data in a daily interval
        next_date = current_date + timedelta(days=1)
        url = f"{base_url}?lat={LAT}&lon={LON}&start={int(current_date.timestamp())}&end={int(next_date.timestamp())}&appid={API_KEY}"
        
        response = requests.get(url)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # If so, extend the data list with the fetched data
            data.extend(response.json().get('list', []))
        # If not, print an error message with the date for which data couldn't be fetched
        else:
            print(f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')}")
            
        # now go to the next day
        current_date = next_date
    
    return data

LAT = '43.7' #latitude of Toronto
LON = '-79.42' #lontitude of Toronto
API_KEY = '68191121aa536ecdaafdd0a6108161dd'
START_DATE = datetime(2021, 1, 1) # Start date
END_DATE = datetime(2023, 12, 31) # End date

# Fetch the data
data = fetch_air_pollution_data(START_DATE, END_DATE, LAT, LON, API_KEY)

print(data[:5])  


# In[4]:


import pandas as pd


# In[6]:


rows = []
for entry in data:
    row = {**entry['main'], **entry['components'], 'dt': entry['dt']}
    rows.append(row)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(rows)

# Convert the 'dt' column to a readable datetime format
df['Date'] = pd.to_datetime(df['dt'], unit='s')

# Drop the 'dt' column if no longer needed
df.drop('dt', axis=1, inplace=True)

# Set the 'Date' column as the index of the DataFrame if desired
df.set_index('Date', inplace=True)

df


# In[8]:


# keep aqi information for further analysis
daily_aqi_averages = df['aqi'].resample('D').mean()
daily_aqi_averages


# In[9]:


# convert to a DataFrame 
daily_aqi_averages = pd.DataFrame(daily_aqi_averages)


# In[10]:


daily_aqi_averages


# In[11]:


# save to csv file
daily_aqi_averages.to_csv('AQI.csv')


# # Scrape historical weather data for Toronto from January 1, 2021, to December 31, 2023 from WorldWeatherOnline

# In[32]:


import requests
import pandas as pd
from datetime import timedelta

api_key = '815759e9d3904bbd83e180404242903'
location = "Toronto, Canada"
start_date = pd.to_datetime("2021-01-01")
end_date = pd.to_datetime("2023-12-31")

# Define a function to fetch the monthly weather data
def fetch_monthly_weather(api_key, location, start_date, end_date):
    monthly_data = [] # creat a list to store the fetched data
    
    # Initialize the current date to the start date
    current_date = start_date
    # Loop through each month in the date range
    while current_date <= end_date:
        end_of_month = current_date + pd.offsets.MonthEnd(1)
        print(f"Fetching data for: {current_date.strftime('%Y-%m')}")

        params = {
            "key": api_key,
            "q": location,
            "format": "json",
            "date": current_date.strftime('%Y-%m-%d'),
            "enddate": end_of_month.strftime('%Y-%m-%d'),
            "tp": "24"  # Daily averages
        }
        
        response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx", params=params)
        
        if response.status_code == 200:
            data = response.json()['data']['weather']
            monthly_data.extend(data)
        else:
            print(f"Error fetching data for {current_date.strftime('%Y-%m')}: {response.status_code}")
        
        # Move to the next month
        current_date = end_of_month + timedelta(days=1)

    return monthly_data


# Fetch the weather data
monthly_weather_data = fetch_monthly_weather(api_key, location, start_date, end_date)

# now we are able to print weather data for each month
for month_data in monthly_weather_data:
    print(month_data)


# In[34]:


# convert dictionary into DataFrame
df1 = pd.DataFrame(monthly_weather_data)


# In[38]:


# drop columns that unrelated with our analysis
df_weather = df1.drop(columns=['astronomy', 'maxtempF', 'mintempF', 'avgtempF', 'hourly'])


# In[39]:


df_weather


# In[40]:


# save to csv
df_weather.to_csv('weather_data.csv')

