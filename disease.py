# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:57:47 2020

@author: ivpan
"""

import  requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

#%% Get today's date

today = date.today()
yesterday = today-timedelta(days=1)

#%% Get data from link and read into file
baselnk = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"
fname = yesterday.strftime("%Y-%m-%d")+".xlsx"
lnk = baselnk+fname
r = requests.get(lnk,allow_redirects=True)
open(f'covid19_{fname}','wb').write(r.content)

#%% Read the file into pandas

df = pd.read_excel(f'covid19_{fname}')

# Sort by date of report
df.sort_values(by=['DateRep'],ascending=True,inplace=True)

# Dictionary with the indeces corresponding to every country
by_country = df.groupby('Countries and territories').groups

# Get cumulative totals of cases and deaths (reversed due to ordering)
df['Total deaths'] = df.groupby('Countries and territories').Deaths.cumsum()[::-1]
df['Total cases'] = df.groupby('Countries and territories').Cases.cumsum()[::-1]

# Global totals (sum over all new cases and all new deaths)
all_deaths = df.Deaths.sum()
all_cases = df.Cases.sum()

#%% Plotting with matplotlib
plt.close('all')

countries = ['Italy','United_Kingdom','China']
fig,ax = plt.subplots(2,2,sharex=True)
for country in countries:
  ax[0,0].plot(df['DateRep'][by_country[country]],df['Cases'][by_country[country]],label=country)
  ax[0,1].plot(df['DateRep'][by_country[country]],df['Deaths'][by_country[country]],label=country)
  ax[0,0].set_title('New Cases')
  ax[0,1].set_title('New Deaths')
  
  ax[1,0].plot(df['DateRep'][by_country[country]],df['Total cases'][by_country[country]],label=country)
  ax[1,1].plot(df['DateRep'][by_country[country]],df['Total deaths'][by_country[country]],label=country)
  ax[1,0].set_title('Total Cases')
  ax[1,1].set_title('Total Deaths')

fig.suptitle(f"Covid-19 data for {countries} from {yesterday.strftime('%Y-%m-%d')}")
ax[0,0].legend(loc='upper left')

[[i.grid('on'),
  i.set_xlabel('Date'),
  i.set_ylabel('Number of people')] for i in ax.flatten()]

fig.autofmt_xdate()
plt.tight_layout()


#%% Better country indications
ctry = pd.read_csv("country_list.txt",
                   sep='\t',
                   header=None)
ctry.columns = ['Name','Alpha2','Alpha3','Numeric']
srs = []
for i in df.GeoId:
  what = ctry.Alpha3[ctry.Alpha2.eq(i)].to_string()[-3::]
  if what!=', )':
    srs.append(what)
  else:
    srs.append(None)
df['Alpha3']=srs
# Fix UK and Greece
df.Alpha3[df.GeoId.eq('UK')] = 'GBR'
df.Alpha3[df.GeoId.eq('EL')] = 'GRC'

#%% Plot on map
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
df2 = px.data.gapminder().query('year==2019')
df3 = df[df.DateRep.eq(yesterday)] # Dataframe with most recent information
fig2 = px.scatter_geo(df3, locations="Alpha3", color="Total deaths",
                      hover_name="Countries and territories", size="Total cases",
                      projection="natural earth")
fig2.show()