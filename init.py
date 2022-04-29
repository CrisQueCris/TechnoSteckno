from ScrapeLast10weeksBillboard import ScrapeLast10weeks

from CheckHotNot import check_if_hot

from songrecommender import get_song_df
from songrecommender import showID_in_player

from scalingclustering import load_pkl
from scalingclustering import predict_kmeans

import pandas as pd

scrape = input('Would you like to get the current Top 100 now?(Y/N)')
    if scrape = Y:
        ScrapeLast9weeks()

#Get user input and check if it is in billboard 100
result, user_input =  check_if_hot()
print(result, user_input)

#If song is hot right now: search it and play it


#If song is not not right now: get song information etc.
song_df = get_song_df(user_input['title'])
print(song_df)

#import model
scaler = load_pkl(filename='model/scalerKmeans.pickle')
kmeans = load_pkl(filename = 'model/modelKmeans.pickle')
X = load_pkl(filename=  'model/X.pickle')
X_scaled_df = load_pkl(filename ='model/X_scaled_df')
sp_library = load_pkl(filename ='model/sp_library.pickle')


#scale and predict song
song_df['Year'] = pd.to_datetime(song_df['ReleaseYear'], format='%Y-%m-%d')
song_df['Year'] = pd.DatetimeIndex(song_df['Year']).year

song_df_scaled = scaler.transform(song_df[X_scaled_df.columns])

song_label, song_cluster = predict_kmeans(song_df_scaled, X, kmeans)

song_df['label'] = song_label

# get song suggestion

song_suggest_cluster = sp_library[sp_library['label']==song_df['label'][0]]

song_suggest = song_suggest_cluster.sample()

song_suggest_TrackID = song_suggest_cluster['TrackID'].iloc[0]

#compare songs

df_compair = pd.concat([song_df, song_suggest], axis=0)
print(df_compair)
df_compair.iloc[:,0:9]

df_compair.iloc[:,10:19]

player_user_choice = showID_in_player(song_df.loc[0, 'TrackID'])
print(f'This is your recommendation:')
player_user_choice

player_recommendation = showID_in_player(song_suggest_TrackID)
print(f'This is your recommendation:')
player_recommendation
