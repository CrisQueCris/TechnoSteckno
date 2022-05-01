import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
import pandas as pd
from time import sleep
from random import randint
from IPython.display import IFrame
from GSA import authenticate



def get_song_df(trackName, ):
    
    global sp, sp_oauth
    authenticate()
    #artistName = 'track:' + input('The title of your song:')
    #trackName = input('The artist of your song:')
    
    
    q = trackName
    
    
    user_song_result = sp.search(q, limit = 1,  market = 'GB')
    column_names = ['TrackName', 'TrackID', 'SampleURL', 'ReleaseYear', 'danceability', 'energy', 
				'loudness', 'speechiness', 'acousticness', 'instrumentalness',
				'liveness', 'valence', 'tempo', 'key', 'mode', 'duration_ms', 'Popularity']
    user_song_df = pd.DataFrame(columns = column_names)
    sleep(randint(0,10) * 0.01)
    
    TrackName = user_song_result['tracks']['items'][0]['name']
    TrackID = user_song_result['tracks']['items'][0]['id']
    SampleURL = user_song_result['tracks']['items'][0]['external_urls'] ['spotify']
    ReleaseYear = user_song_result['tracks']['items'][0]['album']['release_date']
    Popularity = user_song_result['tracks']['items'][0]['popularity']
    
    user_song_audio_features = sp.audio_features(TrackID)

    danceability = user_song_audio_features[0]['danceability']
    energy = user_song_audio_features[0]['energy']
    key = user_song_audio_features[0]['key']
    mode = user_song_audio_features[0]['mode']
    speechiness= user_song_audio_features[0]['speechiness']
    acousticness= user_song_audio_features[0]['acousticness']
    loudness = user_song_audio_features[0]['loudness']
    instrumentalness= user_song_audio_features[0]['instrumentalness']
    liveness= user_song_audio_features[0]['liveness']
    valence= user_song_audio_features[0]['valence']
    tempo= user_song_audio_features[0]['tempo']
    duration_ms= user_song_audio_features[0]['duration_ms']
    
    user_song_df.loc[0, :] = [TrackName, TrackID, SampleURL, ReleaseYear, danceability, energy, 
				loudness, speechiness, acousticness, instrumentalness,
				liveness, valence, tempo, key, mode, duration_ms, Popularity]
    return user_song_df


def showID_in_player(track_id):
    player = IFrame(src="https://open.spotify.com/embed/track/"+track_id,
       width="320",
       height="80",
       frameborder="0",
       allowtransparency="true",
       allow="encrypted-media",
      )
    return player


def show_if_hot(result, user_input):
    """shows alternative from Top100 or if not hot get song data of user input"""
    if result['title'] !=[]:
        print('hot process')
        song_df = get_song_df(result['title'])
        print(f'This is your Hot song:')
        display(showID_in_player(hot_song.loc[0, 'TrackID']))
        print('Here is another song that was hot in the last 10 weeks:')
        # recommendation = get_random_hot_song(result)
        song_recommHot100 = load_billboard_csv().sample()
        hot_song_rec = get_song_df(song_recommHot100['title'])
        display(showID_in_player(hot_song_rec.loc[0, 'TrackID']))
    else:
        print('not hot process')
        song_df = get_song_df(user_input)
        
    return song_df