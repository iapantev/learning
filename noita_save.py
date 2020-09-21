# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:47:38 2020

@author: ivpan

Noita backup:
  This file is used to backup
"""
import tkinter as tk
import shutil
from tkinter import filedialog
import datetime
from os import path as ospath
from os import listdir
import os

#%% Functions to save and restore saves

def save_player():
  original = 'C:\\Users\\ivpan\\AppData\\LocalLow\\Nolla_Games_Noita\\save00\\player.salakieli'
  if ospath.isfile(original):
    # folder_path = filedialog.askdirectory(initialdir = "C:\\Games\\Noita",title = "Select folder")
    file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    target = 'C:\\Games\\Noita\\Player_Backup\\' + 'Player-' + file_name + '.salakieli'
    shutil.copyfile(src = original,
                    dst = target)
  else:
    pass
  print('Player information saved!')


def save_full():
  original = 'C:\\Users\\ivpan\\AppData\\LocalLow\\Nolla_Games_Noita\\save00'
  file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
  target = 'C:\\Games\\Noita\\Full_backup\\'+file_name
  if ospath.exists(target):
    shutil.rmtree(target)
  shutil.copytree(src = original,
                  dst = target)
  print('Full game information saved!')


def restore_player():
  # Ask user for savefile to restore
  original = filedialog.askopenfilename()
  target = 'C:\\Users\\ivpan\\AppData\\LocalLow\\Nolla_Games_Noita\\save00\\player.salakieli'
  if ospath.exists(target):
    os.remove(target)
  shutil.copyfile(src = original,
                  dst = target)
  print('Player restored!')

def restore_full():
  original = filedialog.askdirectory(initialdir = "C:\\Games\\Noita\\Full_backup",title = "Select backup to restore")
  target = 'C:\\Users\\ivpan\\AppData\\LocalLow\\Nolla_Games_Noita\\save00'
  if ospath.exists(target):
    shutil.rmtree(target)
  shutil.copytree(src = original,
                  dst = target)
  print('Game restored!')

#%% Create buttons
master = tk.Tk()

exit_button = tk.Button(master, text='Exit Application', command=master.destroy)

save_all_button = tk.Button(master, text='Save ALL', command = save_full)

save_player_button = tk.Button(master, text='Save Player', command = save_player)

restore_player_button = tk.Button(master, text='Restore Player', command = restore_player)

restore_all_button = tk.Button(master, text = 'Restore All', command = restore_full)

#%% Place buttons in the grid
save_player_button.grid(row=0,column=0)
restore_player_button.grid(row=0,column=1)
save_all_button.grid(row=1,column=0)
restore_all_button.grid(row=1,column=1)
exit_button.grid(row=2,columnspan=2)

# Start the interface
master.mainloop()
