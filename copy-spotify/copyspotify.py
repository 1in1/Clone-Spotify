####################################
########## copyspotify.py ##########
####################################
#
# Will copy over tracks, artists, albums,
# and playlists from one account to another.
# Permissions are granted by signing in
# in-browser.



import sys
#import spotipy
#import spotipy.util as util
import apiclient as spotipy
import util as util

clientID = '***REMOVED***'
clientSecret = '***REMOVED***'
PORTNO = 8070

def loadByOffset(methodIn, n):
    result = methodIn(n, 0)
    items = result['items']
    numLiked = result['total']
    i = n
    while i < numLiked:
        items += methodIn(n, i)['items']
        i += n
    return items

def sendOut(methodOut, n, data):
    i = 0
    while i < len(data):
        methodOut(data[i:i+n])
        i += n

def copyData(methodIn, methodOut, parse, n):
    #Parse strips down to the data methodOut wants to use
    sendOut(methodOut, n, parse(loadByOffset(methodIn, n)))

def copyFollowed(methodIn, methodOut, n):
    #Different loading method here
    result = methodIn(n)
    items = result['artists']['items']
    numFollowed = result['artists']['total']
    after = result['artists']['cursors']['after']
    while after:
        result = methodIn(n, after)
        items += result['artists']['items']
        after = result['artists']['cursors']['after']
    ids = list(map(lambda x: x['id'], items))
    sendOut(methodOut, n, ids)

def copyPlaylists(n, m):
    id = mainsp.current_user()['id']
    newid = newsp.current_user()['id']
    lists = loadByOffset(mainsp.current_user_playlists, n)
    for plist in lists:
        if plist['collaborative'] == False:
            if plist['owner']['id'] == id:
                #Rebuild the playlist
                newplID = newsp.user_playlist_create(newid, plist['name'], plist['public'], plist['description'])['id']
                copyData(lambda N, offset: mainsp.user_playlist_tracks(id, plist['id'], 'total,items(added_at,track(id),is_local)', N, offset),
                    lambda tracks: newsp.user_playlist_add_tracks(newid, newplID, tracks),
                    lambda items: list(map(lambda x: x['track']['id'], items)),
                    100)
            else:
                #We are just following, so follow from new account
                newsp.user_playlist_follow_playlist(plist['owner']['id'], plist['id'])
        else:
            #Rebuild the playlist, mark as collab
            newplID = newsp.user_playlist_create(newid, plist['name'], plist['public'], 'Collab PL Copy - ' + plist['description'])['id']
            copyData(lambda N, offset: mainsp.user_playlist_tracks(id, plist['id'], 'total,items(added_at,track(id),is_local)', N, offset),
                lambda tracks: newsp.user_playlist_add_tracks(newid, newplID, tracks),
                lambda items: list(map(lambda x: x['track']['id'], items)),
                100)



####################################
##### Script doing stuff begin #####
####################################


if not (len(sys.argv) == 1 or len(sys.argv) == 3):
    print("Usage: %s username_FROM username_TO\nOR\n%s" % (sys.argv[0], sys.argv[0]))
    sys.exit()

if len(sys.argv) == 1:
    fromUser = input("Enter email or username for the account we want to copy FROM: ")
else:
    fromUser = sys.argv[1]
fromToken = util.prompt_for_user_token(fromUser,
            'user-library-read user-follow-read playlist-read-private playlist-read-collaborative',
            clientID,
            clientSecret,
            'http://localhost:%d' % PORTNO
            )
if not fromToken:
    print("Couldn't get token")
    sys.exit()

if len(sys.argv) == 1:
    toUser = input("Enter email or username for the account we want to copy TO: ")
else:
    toUser = sys.argv[2]
toToken = util.prompt_for_user_token(toUser,
            'user-library-modify user-follow-modify playlist-modify-private playlist-modify-public',
            clientID,
            clientSecret,
            'http://localhost:%d' % PORTNO
            )
if not toToken:
    print("Couldn't get token")
    sys.exit()



print("Using token for %s: %s" % (fromUser, fromToken))
print("Using token for %s: %s" % (toUser, toToken))
mainsp = spotipy.Spotify(fromToken)
newsp = spotipy.Spotify(toToken)

print("Migrating liked tracks...")
copyData(mainsp.current_user_saved_tracks, newsp.current_user_saved_tracks_add, 
    #(Un)comment to sort by date added/don't sort. Think this one is correct behaviour
    lambda items: list(map(lambda x: x['track']['id'], sorted(items, key=lambda k: k['added_at']))),
    #lambda items: list(map(lambda x: x['track']['id'], items)),
    50)
print("Migrating saved albums...")
copyData(mainsp.current_user_saved_albums, newsp.current_user_saved_albums_add, 
    #lambda items: list(map(lambda x: x['album']['id'], sorted(items, key=lambda k: k['added_at']))),
    lambda items: list(map(lambda x: x['album']['id'], items)),
    50)
print("Migrating followed artists...")
copyFollowed(mainsp.current_user_followed_artists, newsp.user_follow_artists, 50)
print("Migrating playlists (this may take a while)...")
copyPlaylists(50, 100)
