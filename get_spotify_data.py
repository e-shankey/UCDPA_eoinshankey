# Install Packages

# import pandas
import pandas as pd

# Connect to the Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'd1a0446a370141a5a86c01e177eb4a49'
client_secret = 'c5b08a014375450f826687c8b3857e71'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#----------------------------------------------------------------------------------------------------------------------#
# Playlist info
username = '1165512397'
playlist_id = '6agdxWOT4dqZcoUnIEMVbf'

# Get track information from playlist

# First get tracks from the user's playlist
def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

playlist_tracks = get_playlist_tracks(username, playlist_id)

# Loop through all tracks to get track ids
track_ids=[]
for item in playlist_tracks:
    track = item['track']
    track_ids.append(track['id'])

# Data Checks
print(track_ids)
print(len(track_ids))

# Use id's to get track meta data and audio features
def getTrackFeatures(id):
  meta = sp.track(id)
  features = sp.audio_features(id)

  # meta
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']

  # features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']

  track = [name, album, artist, release_date, length, popularity, acousticness, danceability, energy,
           instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
  return track


# loop over track ids to get features for all tracks
tracks = []
for i in range(len(track_ids)):
    track = getTrackFeatures(track_ids[i])
    tracks.append(track)

# create track DataFrame
track_df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

# Create CSV with track DF
track_df.to_csv('spotify_tracks_liked.csv', sep = ',')

# Data Checks
# Track DF Checks
print(track_df.head())
print(track_df.columns)
print(track_df.index)
print(track_df.info()) # Show info on the data

#Check missing values
print(track_df.isna().sum())

#----------------------------------------------------------------------------------------------------------------------#
# Get Artist information associated with a playlist

# First get the artist info from playlist tracks
art_info = []
for item in playlist_tracks:
    artist = item['track']
    art_info.append(artist['artists'])

print(art_info)

# Second get the artist id's from the sub dictionary for every track
def getArtistIDs(art_info):
    art_ids = []
    for item in art_info:
        art_ids.append(item[0]['id'])
    return art_ids

art_ids = getArtistIDs(art_info)

# Data Checks
print(art_ids)
print(len(art_ids))

# Use artist id's to get artist meta data
def get_artist_attributes(id):
  meta = sp.artist(id)

  # meta
  name = meta['name']
  followers = meta['followers']['total']
  genre = meta['genres']
  popularity = meta['popularity']

  artist = [name, followers, genre, popularity]
  return artist

# loop over artist ids
artists = []
for i in range(len(art_ids)):
  artist = get_artist_attributes(art_ids[i])
  artists.append(artist)

# Create artist DataFrame
art_df = pd.DataFrame(artists, columns = ['name', 'followers', 'genre', 'popularity'])

# Add new column which contains the first genre item in the genre column
art_df['main_genre']=art_df['genre'].str[0]

# Rename name column to artist so it can be joined
art_df_named = art_df.rename(columns={'name': 'artist'})

# Drop duplicates from artist
art_df_named_dd = art_df_named.drop_duplicates(subset='artist')

# Create CSV with artist DF
art_df_named_dd.to_csv('spotify_artists_liked.csv', sep = ',')

# Artist DF Checks
print(art_df_named.head())
print(art_df_named.columns)
print(art_df_named.index)
print(art_df_named.info())

#Check missing values
print(art_df.isna().sum())

#----------------------------------------------------------------------------------------------------------------------#
# Combine the Dataframes

# Left Join tracks and artist data
all_data = track_df.merge(art_df_named_dd, on='artist', how='left', suffixes=('_track','_artist'))

# Add new columns to all data with song length in mins
all_data["length_mins"] = all_data['length']/60000

# Checks
print(all_data.head())
print(all_data.shape)
print(all_data.values)
print(all_data.columns)

#Check missing values
print(all_data.isna().sum())

# Create CSV with all data
all_data.to_csv('spotify_all_data_liked_songs.csv', sep = ',')

#----------------------------------------------------------------------------------------------------------------------#