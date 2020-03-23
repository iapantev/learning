# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:08:29 2020

@author: ivpan

Script to download youtube links based on a spotify playlist exported to a csv
"""

import pandas as pd
from os import path as ospath
from os import listdir
import urllib.request
from bs4 import BeautifulSoup

pathi = ospath.abspath('C:/PhD/Spotify_Playlists')
playlists = listdir(pathi)
current = playlists[-1]
df = pd.read_csv(ospath.join(pathi,current),index_col=None)

songs = [df["Artist Name"][i] + ' - ' + df["Track Name"][i]   for i in range(len(df))]
df["YT_link"] = None
count = 0
i = -1
for song in songs:
  i = i+1
  textToSearch = song
  query = urllib.parse.quote(textToSearch)
  url = "https://www.youtube.com/results?search_query=" + query
  response = urllib.request.urlopen(url)
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')
  vids = soup.findAll(attrs={'class':'yt-uix-tile-link'})
  #for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
  try:
    df["YT_link"][i] = ('https://www.youtube.com' + vids[0]['href'])
    count = count + 1
    print(f"{count} songs added")
  except:
    pass

df.to_csv(ospath.join(pathi,'steeps_yt.csv'))
