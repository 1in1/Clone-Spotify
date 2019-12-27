import sys
import spotipy
import spotipy.util as util

clientID = '***REMOVED***'
clientSecret = '***REMOVED***'

def copyData(methodIn, methodOut, key, n):
    result = methodIn(n, 0)
    items = result['items']
    numLiked = result['total']
    i = n
    while i < numLiked:
        items += methodIn(n, i)['items']
        i += n
    ids = list(map(lambda x: x[key]['id'], sorted(items, key=lambda k: k['added_at'])))
    i = 0
    while i < numLiked:
        methodOut(ids[i:i+n])
        i += n


if not (len(sys.argv) == 1 or len(sys.argv) == 3):
    print("Usage: %s username_FROM username_TO\nOR\n%s" % (sys.argv[0], sys.argv[0]))
    sys.exit()

if len(sys.argv) == 0:
    print("Enter email or username for the account we want to copy FROM: ", end="")
    fromUser = input()
else:
    fromUser = sys.argv[1]
fromToken = util.prompt_for_user_token(fromUser,
            'user-library-read',
            clientID,
            clientSecret,
            'http://localhost'
            )
if not fromToken:
    print("Couldn't get token")
    sys.exit()

if len(sys.argv) == 0:
    print("Enter email or username for the account we want to copy TO: ", end="")
    toUser = input()
else:
    toUser = sys.argv[2]
toToken = util.prompt_for_user_token(toUser,
            'user-library-modify',
            clientID,
            clientSecret,
            'http://localhost'
            )
if not toToken:
    print("Couldn't get token")
    sys.exit()

print("Using token for %s: %s" % (fromUser, fromToken))
print("Using token for %s: %s" % (toUser, toToken))
mainsp = spotipy.Spotify(fromToken)
newsp = spotipy.Spotify(toToken)

copyData(mainsp.current_user_saved_tracks, newsp.current_user_saved_tracks_add, 'track', 50)
copyData(mainsp.current_user_saved_albums, newsp.current_user_saved_albums_add, 'album', 50)