import pandas as pd
import numpy as np
from scipy import spatial

users = []
for i in range(0, 20):
    user = pd.read_csv('../data/users/user_' + str(i) + '.csv')
    users.append(user)

songs = []
for u in users:
    song_id = u.id.tolist()

    for i in range(0,len(u)):
        u_song = u.iloc[0]

for u in users:
    p_mean = np.mean(u.popularity_per_user)
    u.popularity_per_user = (u.popularity_per_user - p_mean)

pivot_user = users[0]
users = users[1:]

test_u = users[1]
a = spatial.distance.cosine(pivot_user.popularity_per_user, test_u.popularity_per_user)
print(a)