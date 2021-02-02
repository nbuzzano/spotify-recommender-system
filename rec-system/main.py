import os
import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from collections import defaultdict
from scipy.spatial.distance import cdist

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                           client_secret=os.environ["SPOTIPY_CLIENT_SECRET"]))

spotify_data = pd.read_csv('../data/data.csv')

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()),
                                  ('kmeans', KMeans(n_clusters=20,
                                   verbose=2, n_jobs=4))], verbose=True)

X = spotify_data.select_dtypes(np.number)
number_cols = list(X.columns)
#song_cluster_pipeline.fit(X)

def find_song(name, year):
    """search song in using spotify API"""

    song_data = defaultdict()
    results = sp.search(q='track: {} year: {}'.format(name,
                                                      year), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]

    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)


#number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
#               'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']


#https://api.spotify.com/v1/artists/{id}
df = find_song('Blackbird', '2018')
print('------------')
print(df)
print(df.columns)
print(df.loudness)
print('------------')


def get_song_data(song, spotify_data):
    """search song locally and if it isn't found, use spotify API"""
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name'])
                                 & (spotify_data['year'] == song['year'])].iloc[0]
        return song_data

    except IndexError:
        return find_song(song['name'], song['year'])


def get_mean_vector(song_list, spotify_data):
    """map song_list which is an arr of songs features into a mean vector, example:
        a = np.array([[1, 2], [3, 4]])
        np.mean(a, axis=0) -> array([2., 3.])
     """
    song_vectors = []

    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)

    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)


def flatten_dict_list(dict_list):
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []

    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)

    return flattened_dict


def recommend_songs(song_list, spotify_data, n_songs=10):
    metadata_cols = ['name', 'year', 'artists']
    song_dict = flatten_dict_list(song_list)

    """get mean vector of the user"""
    song_center = get_mean_vector(song_list, spotify_data)

    """get fitted scaler and scale spotify and user songs"""
    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))

    """ mesuring how closer is user data from another spotify's songs. (recommendation system maths)"""
    distances = cdist(scaled_song_center, scaled_data, 'cosine')

    """
    should measure different metrics like: 
    + manhattan, 
    + euclidean, 
    + the Pearson, 
    + and the cosine similarity scores.
    
    there is no right answer to which score is the best. 
    Different scores work well in different scenarios, and it is often a good idea to 
    experiment with different metrics and observe the results.

    Another thing that could be tested, is removing or adding features and checking if outputs improve.
    (this is, playing with the content of "number_cols" arr)
    
    Does it makes sense, modifying certain features in order to make them have more or less impact at 
    the time of measuring distances ???
    """

    index = list(np.argsort(distances)[:, :n_songs][0])
    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return rec_songs[metadata_cols].to_dict(orient='records')

#recommend_songs([{'name': 'Come As You Are', 'year':1991},
#                {'name': 'Smells Like Teen Spirit', 'year': 1991},
#                {'name': 'Lithium', 'year': 1992},
#                {'name': 'All Apologies', 'year': 1993},
#                {'name': 'Stay Away', 'year': 1993}],  spotify_data)

"""
Content Based Rec System - Output:
[
{'name': 'Dear Limmertz', 'year': 1990, 'artists': "['Azymuth']"},
{'name': 'When Will It Rain', 'year': 1992, 'artists': "['Jackyl']"},
{'name': 'Love Like This', 'year': 1998, 'artists': "['Faith Evans']"},
{'name': 'Kiss This Thing Goodbye', 'year': 1989, 'artists': "['Del Amitri']"},
{'name': 'Thank You', 'year': 1994, 'artists': "['Boyz II Men']"},
{'name': 'Dope Game', 'year': 2000, 'artists': "['South Park Mexican']"},
{'name': 'Fourth Of July', 'year': 1994, 'artists': "['Dave Alvin']"},
{'name': 'Brown Eyes', 'year': 2001, 'artists': '["Destiny\'s Child"]'},
{'name': 'Hello in There', 'year': 1971, 'artists': "['John Prine']"},
{'name': 'Seven Wonders - Early Version; 2017 Remaster', 'year': 1987, 'artists': "['Fleetwood Mac']"}
]
"""