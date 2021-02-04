import pandas as pd
import random
from random import randrange

spotify_data = pd.read_csv('data/data_with_genres.csv')

print('number of artists:', spotify_data['artists'].nunique())

# busco artistas "populares", consideramos popular los que tienen > 200 canciones en la plataforma.
n_popular = 200
spotify_data_count = spotify_data.groupby('artists').count()
artistas_populares = spotify_data_count[spotify_data_count.acousticness > n_popular].index.tolist()

# spotify_data_count[spotify_data_count.acousticness > 200].index.tolist()[0] == '[\'Aretha Franklin\']'

users = []
n_users = 20
for i_user in range(0, n_users):

    # creamos usuario con una cantidad de canciones user_range, de las cuales
    # el usuario tendra la mitad de sus canciones , sobre el mismo artista y el resto variado
    #

    history_size = 50
    cant_de_canciones = random.choice(range(history_size - 10, history_size))
    cant_de_canciones = round(cant_de_canciones / 2)

    artista_mas_escuchado = random.choice(artistas_populares)
    canciones_populares_artista = spotify_data[spotify_data.artists == artista_mas_escuchado]

    usuario_canciones = []
    df = pd.DataFrame()

    for i in range(0, cant_de_canciones):
        sample_song = canciones_populares_artista.sample()
        df = df.append(sample_song)

        sample_song = spotify_data.sample()
        df = df.append(sample_song)

    df_len = len(df)
    popularidad = []
    for i in range(0, len(df)):
        popularidad.append(randrange(10))
    df['popularity_per_user'] = popularidad

    csv_name = 'data/users/user_' + str(i_user) + '.csv'
    df.to_csv(csv_name)
    print(csv_name)