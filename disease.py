# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:57:47 2020

@author: ivpan
"""
#%% Import libraries
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
df.columns = ['DateRep','Day','Month','Year','New_Cases','New_Deaths','Countries and territories','GeoId','Alpha3','Population 2018','Continent']

df['DateOnly'] = df['DateRep'].dt.date
df['Frame'] = df['DateRep'].dt.strftime("%d-%b")
df['New_Deaths'] = df['New_Deaths'].abs()
df['New_Cases'] = df['New_Cases'].abs()

# Sort by date of report
df.sort_values(by=['DateRep'],ascending=True,inplace=True)

# Dictionary with the indeces corresponding to every country
by_country = df.groupby('Countries and territories').groups

# Get cumulative totals of cases and deaths (reversed due to ordering)
df['Total deaths'] = df.groupby('Countries and territories').New_Deaths.cumsum()[::-1]
df['Total cases'] = df.groupby('Countries and territories').New_Cases.cumsum()[::-1]
df['Cases per 100k'] = (100e3*df['Total cases']/df['Population 2018']).round(decimals=2)
df['Deaths per 100k'] = (100e3*df['Total deaths']/df['Population 2018']).round(decimals=2)
df['Population'] = (df['Population 2018']/1e6).round(decimals=2)


# Global totals (sum over all new cases and all new deaths)
all_deaths = df.New_Deaths.sum()
all_cases = df.New_Cases.sum()

#%% Plotting with matplotlib
plt.close('all')

countries = ['Italy','United_States_of_America','Spain','Netherlands','United_Kingdom']
fig,ax = plt.subplots(2,2,sharex=True)
for country in countries:
  ax[0,0].plot(df['DateOnly'][by_country[country]],df['New_Cases'][by_country[country]],label=country)
  ax[0,1].plot(df['DateOnly'][by_country[country]],df['New_Deaths'][by_country[country]],label=country)
  
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
# ctry = pd.read_csv("country_list.txt",
#                    sep='\t',
#                    header=None)
# ctry.columns = ['Name','Alpha2','Alpha3','Numeric']
# srs = []
# # Loop over all data entries in dataset and get 3-letter country code
# for i in iter(df.GeoId):
#   what = ctry.Alpha3[ctry.Alpha2.eq(i)].to_string()[-3::]
#   if what!=', )':
#     srs.append(what)
#   else:
#     srs.append(None)

# df['Alpha3']=srs
# # Fix UK and Greece as these appear wrong in the 2-letter combo in the original dataset
# df.loc[df['GeoId'].eq('UK'),'Alpha3'] = 'GBR'
# df.loc[df['GeoId'].eq('EL'),'Alpha3'] = 'GRC'
# df.loc[df['GeoId'].eq('PYF'),'Alpha3'] = 'PYF'
# df.loc[df['GeoId'].eq('XK'),'Alpha3'] = 'XKX'
# df.loc[df['Country code'].eq('NAM'),'Alpha3'] = 'NAM'

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

# Dataframe with most recent information (if used)
df3 = df[df.DateOnly.eq(yesterday)]

# Make a Scattergeo figure
fig2 = px.scatter_geo(df, locations="Alpha3", 
                      color="Total deaths", range_color = [0,20000],
                      size="Total cases",
                      hover_name="Countries and territories", 
                      hover_data=["New_Cases","New_Deaths","Population","Deaths per 100k","Cases per 100k"],
                      animation_frame = 'Frame',animation_group = 'DateOnly',
                      projection="natural earth")

# Add coutry coloring based on some data
# fig2.add_trace(go.Choropleth(locations=df3['Alpha3'],
#                               z=df['Total cases'].astype(float),
#                               colorbar_title='Total deaths'))

# Make a Choropleth figure
# fig3 = px.choropleth(data_frame = df,locations = "Alpha3",
#                      color = 'Total deaths',hover_name = "Countries and territories",
#                      hover_data=["New_Cases","New_Deaths","Population","Deaths per 100k","Cases per 100k"],
#                      animation_frame = 'Frame',animation_group='DateOnly',
#                      projection="natural earth")

# Layout for the scatter geo figure
fig2.update_geos(
    visible = False, resolution=110,
    showcountries = True, countrycolor = "RebeccaPurple",
    showframe = True,
    showland = True, landcolor = 'LightGray',
    showocean = True, oceancolor = 'LightBlue'
)
fig2.update_layout(
  title = go.layout.Title(text='Covid-19 spread <br>(size is total cases, color is total deaths)'))
# fig2.update_layout(
#     title = go.layout.Title(text = 'Covid-19 spread around the world'),
#     updatemenus = [
#       dict(
#         buttons=list([
#           dict(args=['type','scatter_geo'],
#                label='New deaths',
#                method='update'),
#           dict(args=['type','scatter_geo'],
#                label='New cases',
#                method='update'),
#           dict(args=['type','scatter_geo'],
#                label='Total deaths',
#                method='update'),
#           dict(args=['type','scatter_geo'],
#                label='Total cases',
#                method='update')]
#           ),
#         direction = "down",
#         pad = {"r" : 10,"t" : 10},
#         showactive=True,
#         x=0.1,
#         xanchor="left",
#         y=1.1,
#         yanchor="top"
#         )
#       ]
#     )
      

# Layout for choropleth figure
# fig3.update_geos(
#   resolution = 110,
#   showocean = True, oceancolor='LightBlue',
#   showframe = True)

# Show the figure from offline html
plotly.offline.plot(fig2, filename=f"covid19-{yesterday.strftime('%Y-%m-%d')}.html")

#%% Read BCG data from excel
# bcg_ceased = pd.read_excel("bcg_ceased.xlsx")
# bcg_ceased.columns = ["Country","Current BCG","Current Booster","Past Booster","Booster Timing","Year Booster Stopped"]

# bcg_continu = pd.read_excel("bcg_continuing.xlsx")
# bcg_continu.columns = ["Country","BCG 1st","BCG 2nd","BCG 3rd"]
# bcg_continu["Current BCG"] = "Yes"
# bcg_all = pd.concat([bcg_continu,bcg_ceased],ignore_index = True, sort = False)
# bcg_all.fillna(value = "No",inplace=True)

# del bcg_ceased, bcg_continu
# # TODO: either merge this into the main dataframe or use separately to only plot the available BCG policy data
# srs = []
# for i in iter(bcg_all.Country):
#   what = ctry.Alpha3[ctry.Name.eq(i)]
#   if len(what) != 0:
#     srs.append(what.item())
#   else:
#     srs.append(None)
# bcg_all["Alpha3"] = srs
# del srs

