# A Spotify song recommender

## The task is to recommend... 
    ... Songs that are actually similar to the ones the user picked from an acoustic point of view.
    ... Songs that are popular around the world right now, independently from the user's taste.

## Process

Main jupyter notebook: 

**songrecommender.ipynb**

In order to fullfill the tasks at hand this app does the following:

1. It asks the user to input a song title
2. The song title is compared with the current Top 100 Billboard Charts
3. If the song is currently in the Top 100 the user gets a random recommendation of the Top 100 songs plus songs that where popular in the last weeks (up to 10 weeks from now)
4. If the song is not in the current Top 100 the app gets the audio features of the song from spotify.
5. The song is clustered according to a Kmeans model of a database of currently around 5000 songs.
6. A random song recommendation of the same song is displayed

**Additional features:**

*tempo*

This app is designed to fit Djing purposes. For a smooth transition from one song to the next song it is necessary that both songs don't differ much in their tempo. Therefore the song recommendation will be maximum 8 beats per minute (BPM) faster or slower than the user input.

*harmony*

Two songs that are mixed will only sound nice to the human ear if their keys align. Therefore the song recommendation will follow the rules of harmonic mixing (see [Camelot Wheel](https://mixedinkey.com/camelot-wheel/)).

![Camelot Wheel](https://mixedinkey.com/wp-content/uploads/2020/04/Camelot-Wheel-Mixed-In-Key-Harmonic-Mixing.png)

The app takes the key and mode of the audio features, translates them into the camelot notation and outputs four different key, mode combinations. The output will be a song that is fit for harmonic mixing.


This repo contains:

- songrecommender.ipynb: the main notebook taking input and displaying the recommendation
- Get Playlist Data.ipynb: allows to search for playlist and save the audio features of the song contained
- ScrapeLast10weeksBillboard.py: Get song information on Billboard Top100 plus 10 weeks
- ScalingClustering.ipynb: The Kmeans model which is the basis for the song recommendation
- harmonicneighbours.py: Moduls for translating from pitch_scale to Camelot Notation and back and returning the harmonic sibblings to the input scale.




    

