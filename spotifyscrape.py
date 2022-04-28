import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
import pandas as pd
from time import sleep
from random import randint

def get_tracklist(playlist_id, sp):
    """Get list of dictionaries containing id, name, popularity spotify playlist id"""
    track_id_list=[]
    playlist_tracks = sp.user_playlist_tracks("spotify", playlist_id, market="GB")
    while playlist_tracks['next']:
        playlist_tracks = sp.next(playlist_tracks)
        print(playlist_tracks['items'][0]['track']['id'])
        track_id_list.append([dict((key, playlist_tracks['items'][i]['track'][key]) for key in ['id', 'name', 'popularity'])\
                              for i in range(0,len(playlist_tracks['items']))])
        sleep(randint(1,3))
    return track_id_list


def get_df_out(track_id_list):
    """ returns dataframe from list of list of dictionaries"""
    df_out = pd.DataFrame(columns=track_id_list[0][0].keys())
    for item_list in track_id_list:
        df_in = pd.DataFrame(columns=track_id_list[0][0].keys())
        for item in item_list:
            df_in = pd.concat( [df_in, pd.DataFrame(item, index=[0])])
        df_out = pd.concat([df_out, df_in])
    return df_out