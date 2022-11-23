# Clone Spotify

Short script to clone spotify accounts. It will copy over liked tracks, saved albums, followed artists, and playlists from the first account to the second. Playlists are copied in the correct order. Nothing in the either account will be deleted.

Will take as input either the two accounts (username or email) you want to copy between, or will prompt for the user to enter these. Permissions are granted via the Spotipy `util` class, so it launches the default browser to let you sign in to Spotify to grant. Keep an eye on who you're signed in as, needs to be the 'from' account first then the 'to'; might help to not hit 'remember me'.


There is currently no API support for podcasts, so I haven't implemented this myself. There is also no API support for adding/removing accounts from private collaborative playlists, so at present it just rebuilds collab playlists in the new account. 

Built with https://github.com/plamere/spotipy, a python wrapper for the Spotify API.

## Installing

<s>**You should just be able to download the folder and run copyspotify.py**</s> **You need requests installed to be able to run this.** If you have pip installed, this is as simple as 
```bash
pip install requests
```
Then you can run it from the directory with 
```bash
python .\copyspotify.py
```
This requires and ships with a very modified version version of spotipy 2.10.0, so there should be no further installation needed. It should also ignore other installations of spotipy (current `pip` version is out of date, for example). Recent versions of spotipy also require `six` be installed, so the file is included here.

## To run

Navigate to the directory `copy-spotify`, and run ``` python .\copyspotify.py ```
