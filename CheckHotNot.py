import pandas as pd
import os
from datetime import datetime
from difflib import get_close_matches
from IPython.display import IFrame
from songrecommender import showID_in_player


def load_billboard_csv():
    #Load billboard top 100
    billboard_files = os.listdir("billboard") 
    billboard10 = pd.DataFrame()

    for i in billboard_files: 
        if i.endswith('.csv'):
            df = pd.read_csv('billboard/'+i)
            billboard10 = pd.concat([billboard10, df], axis=0)
    return billboard10

def get_iso_week():
    # Get current week to only compare with current Top 100
    iso_week = datetime.now().isocalendar().week
    return iso_week

def check_if_hot():
    #Get song input from user
    billboard10 = load_billboard_csv()
    iso_week = get_iso_week()
    user_check = False
    while user_check == False:
        user_input={}
        user_input['title']= input('Give me your song title!')    

        #Check if song title is in billboard10
        result={}
        result['title'] = get_close_matches(user_input['title'], billboard10[(billboard10['week_nr'] == (iso_week-1))]['title'], n=1) #get closest (n=1)  match of only the last week (billboard10 has the last 10 weeks)
        if result['title']==[]:
            print(f"No song similar to {user_input['title']} is hot right now.")
            break              
        result['title']=result['title'][0]    
        result['artist'] = billboard10[(billboard10['week_nr'] == (iso_week-1))\
                                       & (billboard10['title'] == result['title'])]['interpret'].to_string(index=False)

        result['pos'] = billboard10[(billboard10['week_nr'] == (iso_week-1))\
                                    & (billboard10['title'] == result['title'])]['position'].to_string(index=False)

        user_check = input(f"""Is it \"{result['title']}\" by {result['artist']}
        that you're looking for?\n It is currently on number {result['pos']}.\n  (Y/N)""")
        if user_check in ['Y','y','yes']:
            user_check = True
            hot_var=True

        elif user_check in ['N','n','no']:
            user_check = False
            hot_var=True
        else: 
            print('Input not readable. Please enter Y or N.')
    if user_check == True:
        print(f'This song is hot right now!') 
    return result, user_input

def get_random_hot_song(song_result):
    """Takes a dictionary of format 
    {'title': 'title',
    'artist': 'artist',
    'pos': 'position'} 
    loads dataframe from billboard. User selects which timeframe(up to 10 weeks from current week). Recomments random song from timefram."""
    timeframe = int(input(f'I want my song recommendation from the last ________ weeks. (max. 10)'))
    billboard10 = load_billboard_csv()
    current_week = max(billboard10['week_nr'])
    week_before = current_week - timeframe
    billboard_timeframe = billboard10[billboard10['week_nr'] <= current_week & billboard10['week_nr'] >= week_before]
    recommendation = billboard_timeframe.sample()
    return recommendation
   
    
