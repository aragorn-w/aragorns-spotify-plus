# aragorns-spotify-plus

## Motivation
This is just a spotipy python script I made to give me some extra features that the regular Spotify desktop app doesn't have, like checking what playlists of mine a song I want to add is already in (before I add it).

I am a particularly picky person about my music, since music is pretty much the only thing that keeps me consistently productive and happy.

## My Music Organizational System
As of June 19th, 2022, I am a CS-interested high school junior with a beginner/intermediate-level knowledge of AI/DL/ML, so I feel I can be just a little cocky enough to control the personal music data I feed to the Spotify algorithm by controlling what songs the algorithm sees me add, like, and listen to based on my following preference for organizing music:
* "Genres" playlists that only contain songs that strongly associate with a particular sub-genre identified by the Spotify clustering algoritm's label-creation (i.e. a "modern alt rock" sub-genre playlist) (I don't want the data from these playlists to be seen by the algorithm, since I'm aware that the algorithm gives weight to any song that you add to your playlists)
* "Mixtapes" playlists that contain songs I arbitrarily feel best suit the mixtape's mood (these are playlists that I actually listen to and want for its data to be fully fed to the Spotify algorithm) (i.e. a "Smooth Man" mixtape playlist whose songs' "moods" makes me feel like being the smoothest man alive)
* "Archived Mixtapes" playlists that are just mixtapes I no longer listen to but might have songs or general song-moods I could reference for making new mixtapes
* "Records" playlists that are the same as Mixtape playlists but just contain a single song that defines the mood
* "Artist Bests" playlists that only contain songs from a singular artist since there are a few artists I very much love more than at least 1 or 2 songs from, warranting a playlist dedicated to their "best" (IMO) songs
* "IMMEDIATE TO-SORT" playlist that has high-priority songs I really like and need to decide at a later time which sub-genres and mixtapes it best fits for my own listening purposes
* "LIBRARY TO-SORT" playlist that is the same as the IMMEDIATE TO-SORT playlist that just has lower-priority songs

## Application Structure
The structure of this perpetually-running personal "Spotify-plus" python project is pretty simple: A Typer CLI script that shares resources with a multi-threaded background daemon process (which is running continuously on an old Macbook Pro 15" of mine) that does things like fetch updates from my Spotify playlists.

### **\[1\]**
> To stop the Spotify algorithm from learning song recommendations from the songs (that I somewhat like in the moment) I add to sub-genre playlists, I will be storing my genre-playlists and archived mixtape-playlists on a second Spotify account (attached with the duo premium plan to my main account for both this and also because Tesla sucks at Telsa-iPhone Spotify relations) that I'll be accessing on my desktop via a virtual machine

## Interfaces Wishlist
As of June 19th, 2022, here are the interfaces I plan to have implemented, eventually:
* The .exe command-line interface mentioned above with access to all services
    * Maybe a basic-GUI desktop app interface as well
* A basic-GUI iOS app with the same access to the services (to make it easier to access both Spotify accounts on my iPhone without somehow remotely accessing the virtual machine mentioned in **\[1\]**
