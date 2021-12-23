# Load csv's from 'get_spotify_data.py' to DataFrames

# Import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Assign file names
all_data_file = 'spotify_all_data_liked_songs.csv'
artists_file = 'spotify_artists_liked.csv'
tracks_file = 'spotify_tracks_liked.csv'

# Read files to DataFrames
all_data_df = pd.read_csv(all_data_file)
artist_data_df = pd.read_csv(artists_file)
tracks_data_df = pd.read_csv(tracks_file)

# Data Checks
print(all_data_df.head())
print(artist_data_df.head())
print(tracks_data_df.head())
#----------------------------------------------------------------------------------------------------------------------#

# Oldest song
oldest_song_date = all_data_df['release_date'].min()
print(all_data_df[all_data_df['release_date']==oldest_song_date]['name'] + ' '+ str(oldest_song_date))

# Newest Song
newest_song_date = all_data_df['release_date'].max()
print(all_data_df[all_data_df['release_date']==newest_song_date]['name'] + ' '+ str(newest_song_date))

# Average song length
song_length_analysis=all_data_df['length_mins'].agg([np.min, np.max, np.mean])
print(song_length_analysis)

#----------------------------------------------------------------------------------------------------------------------#
# Most Globally Popular Tracks, Artists & Songs in the Playlist
# Sorting Values to see most popular tracks
most_pop_tracks = all_data_df[['name','release_date','popularity_track','artist']].sort_values(['popularity_track', 'release_date'], ascending=[False, False], ignore_index=True) # Sort tracks by most popular and release date
print(most_pop_tracks[['name','popularity_track','artist']])

# Sorting Values to see most popular artists
most_pop_artists = artist_data_df.sort_values(['popularity', 'main_genre'], ascending=[False, True], ignore_index=True) # Sort artists by most popular and genre
print(most_pop_artists[['artist','popularity','main_genre']])

# create function to check location of song in popularity list
def track_popularity(name, sorted_pop_list):
    sorted_pop_list.index+=1
    print(sorted_pop_list.loc[sorted_pop_list['name']==name])

track_popularity('Unforgettable', most_pop_tracks)

#----------------------------------------------------------------------------------------------------------------------#
# My most popular genres based on counting
# Check most popular genres
genre_count_norm = all_data_df['main_genre'].value_counts(sort=True, normalize=True)
genre_count_over_1pc = genre_count_norm[genre_count_norm>=0.01]
genre_count_over_1pc.plot(xlabel='', ylabel='', title='Most Common Genres in My Liked Songs', kind='pie')
plt.show()

# Check most popular artists
artist_count = all_data_df['artist'].value_counts(sort=True, normalize=True)
artist_count_over_1pc = artist_count[artist_count>=0.01]
artist_count_over_1pc.plot(xlabel='Artist', ylabel='Proportion', title='Most Common Artists in My Liked Songs', kind='bar')
plt.show()

#----------------------------------------------------------------------------------------------------------------------#
# More detailed analysis
# Add a release year column to the all_data_df
all_data_df['release_year'] = pd.DatetimeIndex(all_data_df['release_date']).year

# Artist popularity by released track years
avg_artist_popularity_year = all_data_df.groupby('release_year')['popularity_artist'].agg([np.max])
avg_artist_popularity_year.plot(kind='line', xlabel='Year', ylabel='Max Popularity', title='Max artist popularity vs Time')
plt.show()

# Track popularity by released track years
most_pop_genre_year = all_data_df.groupby('release_year')['popularity_track'].agg([np.max])
most_pop_genre_year.plot(kind='line', xlabel='Year', ylabel='Max Popularity', title='Max track popularity vs Time')
plt.show()
#----------------------------------------------------------------------------------------------------------------------#
# Song Feature Trends over time
# Average energy by year
avg_energy_year = all_data_df.groupby('release_year')['energy'].agg([np.mean])
avg_energy_year.plot(kind='line')
plt.show()

# Average Acousticness by year
avg_acousticness_year = all_data_df.groupby('release_year')['acousticness'].agg([np.mean])
avg_acousticness_year.plot(kind='line')
plt.show()

def plot_timeseries(axes, y, color, xlabel, ylabel):
    axes.plot(y, color=color)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel, color=color)
    axes.tick_params('y', colors=color)

fig, ax = plt.subplots()
plot_timeseries(ax, avg_energy_year, 'blue', 'Year', 'Average Energy')
ax2 = ax.twinx()
plot_timeseries(ax2, avg_acousticness_year, 'red', 'Year', 'Average Acousticness')
plt.show()
fig.savefig('energy_acousticness_v_time.png')

#----------------------------------------------------------------------------------------------------------------------#
# Correlation Heatplot
# Remove columns that are not interesting for correlation from all data and save as new DF
corelation_df = all_data_df.drop(['Unnamed: 0', 'name', 'album', 'artist', 'release_date', 'length', 'genre', 'popularity_artist', 'followers', 'release_year'], axis=1)
# Plot correlation heatmap
sns.heatmap(corelation_df.corr(), annot=True)
plt.show()

avg_pop_genre = all_data_df.groupby('main_genre')['popularity_track'].max()
print(avg_pop_genre)

avg_pop_genre.plot(kind='bar', title='Most Popular Genres')
plt.show()

#----------------------------------------------------------------------------------------------------------------------#