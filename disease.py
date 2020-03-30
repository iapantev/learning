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
yesterday = date.today()-timedelta(days=1)

#%% Get data from link and read into file
baselnk = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"
fname = yesterday.strftime("%Y-%m-%d")+".xlsx"
lnk = baselnk+fname
r = requests.get(lnk,allow_redirects=True)
open(f'covid19_{fname}','wb').write(r.content)

#%% Read the file into pandas

df = pd.read_excel(f'covid19_{fname}')
df.columns = ['DateRep','Day','Month','Year','Cases','Deaths','Countries and territories','GeoId','Country code','Population 2018']

df['DateOnly'] = df['DateRep'].dt.date
df['Frame'] = df['DateRep'].dt.strftime("%d-%b")

# Sort by date of report
df.sort_values(by=['DateRep'],ascending=True,inplace=True)

# Dictionary with the indeces corresponding to every country
by_country = df.groupby('Countries and territories').groups

# Get cumulative totals of cases and deaths (reversed due to ordering)
df['Total deaths'] = df.groupby('Countries and territories').Deaths.cumsum()[::-1]
df['Total cases'] = df.groupby('Countries and territories').Cases.cumsum()[::-1]
df['Cases per 100k'] = (100e3*df['Total cases']/df['Population 2018']).round(decimals=2)
df['Deaths per 100k'] = (100e3*df['Total deaths']/df['Population 2018']).round(decimals=2)
df['Population'] = (df['Population 2018']/1e6).round(decimals=2)


# Global totals (sum over all new cases and all new deaths)
all_deaths = df.Deaths.sum()
all_cases = df.Cases.sum()

#%% Plotting with matplotlib
plt.close('all')

countries = ['Italy','United_States_of_America','Spain','India','United_Kingdom']
fig,ax = plt.subplots(2,2,sharex=True)
for country in countries:
  ax[0,0].plot(df['DateOnly'][by_country[country]],df['Cases'][by_country[country]],label=country)
  ax[0,1].plot(df['DateOnly'][by_country[country]],df['Deaths'][by_country[country]],label=country)
  
  ax[1,0].plot(df['DateOnly'][by_country[country]],df['Total cases'][by_country[country]],label=country)
  ax[1,1].plot(df['DateOnly'][by_country[country]],df['Total deaths'][by_country[country]],label=country)

ax[0,0].set_title('New Cases')
ax[0,1].set_title('New Deaths')
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
# Read country codes from txt file
ctry = pd.read_csv("country_list.txt",
                   sep='\t',
                   header=None)
ctry.columns = ['Name','Alpha2','Alpha3','Numeric']
srs = []
# Loop over all data entries in dataset and get 3-letter country code
for i in iter(df.GeoId):
  what = ctry.Alpha3[ctry.Alpha2.eq(i)].to_string()[-3::]
  if what!=', )':
    srs.append(what)
  else:
    srs.append(None)

df['Alpha3']=srs
# Fix UK and Greece as these appear wrong in the 2-letter combo in the original dataset
df.loc[df['GeoId'].eq('UK'),'Alpha3'] = 'GBR'
df.loc[df['GeoId'].eq('EL'),'Alpha3'] = 'GRC'
df.loc[df['GeoId'].eq('PYF'),'Alpha3'] = 'PYF'
df.loc[df['GeoId'].eq('XK'),'Alpha3'] = 'XKX'
df.loc[df['Country code'].eq('NAM'),'Alpha3'] = 'NAM'

#%% Add data for map hover
# df['text'] =  "Cases/100K=" + df['Cases per 100k'].round(decimals=2).astype(str) + '<br>' \
#               + "Deaths/100K=" + df['Deaths per 100k'].round(decimals=2).astype(str) + '<br>'\
#               + "Population=" + df['Population'].round(decimals=2).astype(str) + " M."

#%% Plot on map
import plotly
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = "browser"
# df2 = px.data.gapminder().query('year==2019')
df3 = df[df.DateOnly.eq(yesterday)] # Dataframe with most recent information
fig2 = px.scatter_geo(df, locations="Alpha3", color="Total deaths",
                      hover_name="Countries and territories", size="Total cases",
                      hover_data=["Population","Deaths per 100k","Cases per 100k"],
                      animation_frame = 'Frame',animation_group = 'DateOnly',
                      projection="natural earth")

# fig2.show()

# fig2 = go.Figure(go.Scattergeo())
# fig2.scatter_geo(df3, locations="Alpha3", color="Total deaths",
#                       hover_name="Countries and territories", size="Total cases",
#                       projection="natural earth")
fig2.update_geos(
    visible = False, resolution=110,
    showcountries = True, countrycolor = "RebeccaPurple",
    showframe = True,
    showland = True, landcolor = 'LightGray',
    showocean = True, oceancolor = 'LightBlue'
)
# fig2.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
plotly.offline.plot(fig2, filename=f"covid19-{yesterday.strftime('%Y-%m-%d')}.html")
# fig2.show()