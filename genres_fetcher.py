import pandas as pd
import ast
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                           client_secret=os.environ["SPOTIPY_CLIENT_SECRET"]))

spotify_data = pd.read_csv('data/data.csv')

artists_saved = {}
artist_genre = []


def print_info(i, track_id):
    print()
    print('track id', track_id)
    print('item no ' + str(i))
    print('porcentage ' + str(i / 174389))


for i in range(len(artist_genre), len(spotify_data)):

    track_id = spotify_data.iloc[i].id
    track = sp.track(track_id)

    print_info(i, track_id)

    if len(track['artists']) == 0:
        # chequeo si la API devuelve un track con artistas,
        # sigo al proximo elemento si esta vacio
        artist_genre.append([])
        continue

    else:

        aux_genres = []

        for artist in track['artists']:

            try:
                # chequeo si es un artista ya fetcheado,
                # asi no hago un llamado a la API devuelta

                artist_genre_saved = artists_saved[artist['id']]
                for s in artist_genre_saved:
                    aux_genres.append(s)
                continue
            except:
                None

            art_id = artist['id']
            artist_detail = sp.artist(art_id)

            if artist_detail['genres'] != []:
                # busco artista en API por ID

                artists_saved[art_id] = artist_detail['genres']

                for g in artist_detail['genres']:
                    aux_genres.append(g)

            else:

                # busco artista en API por NOMBRE

                artists_name = str(spotify_data.iloc[i].artists)
                artists_name = ast.literal_eval(artists_name)

                for artist_name in artists_name:
                    results = sp.search(q='artist:' + artist_name, type='artist')
                    items = results['artists']['items']
                    try:
                        for g in items[0]['genres']:
                            aux_genres.append(g)

                        artists_saved[art_id] = items[0]['genres']
                    except:
                        None

        aux_genres = list(set(aux_genres))
        artist_genre.append(aux_genres)
        print(aux_genres)

spotify_data['artist_genre'] = artist_genre
spotify_data.to_csv('data/data_with_genres.csv')