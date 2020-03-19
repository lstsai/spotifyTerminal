import os
import sys
import json
import spotipy 
import webbrowser 
import spotipy.util as util
from json.decoder import  JSONDecodeError

#get the username from the terminal
username=sys.argv[1]

scope='user-read-private user-read-playback-state user-modify-playback-state'

#erase the cache and prompt for user permission

try:
	token=util.prompt_for_user_token(username, scope)
except:
	os.remove(f".cache-{username}")
	token=util.prompt_for_user_token(username, scpoe)
#create the spotifyObject

spotifyObject=spotipy.Spotify(auth=token)

#get the current device
devices=spotifyObject.devices()
# print(json.dumps(devices, sort_keys=True, indent=4))
deviceID =devices['devices'][0]['id']

#get track information
track=spotifyObject.current_user_playing_track()
# print(json.dumps(track, sort_keys=True, indent=4))
artist=track['item']['artists'][0]['name']
track=track['item']['name']

if artist != "":
	print()
	print("+++ Currently Playing: "+artist+" - "+track+" +++")
	print()




user= spotifyObject.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))

displayName=user['display_name']

while True:
	print(">>>Welcome to Spotipy "+displayName+"!<<<")
	print()
	print("0 - Search for an artist")
	print("1 - Exit")
	print()
	choice=input("Your Choice: ")

	#search for the artist
	if choice=='0':
		print()
		searchQuery= input("Ok, what's the name of the artist? :")
		print()

		#search for the artist
		searhResults= spotifyObject.search(searchQuery, 1, 0, "artist")
		#print(json.dumps(searhResults, sort_keys=True, indent=4))

		#artist details
		artist=searhResults['artists']['items'][0]
		print("*** "+artist['name']+" ***")
		print("Followers:"+str(artist['followers']['total']))
		print("Genre: "+artist['genres'][0])
		print()
		webbrowser.open(artist['images'][0]['url'])
		artistID=artist['id']

		#get album details from artist
		trackURIs =[]
		trackArt=[]
		albumID= []
		albumArt=[]
		z=1

		#extract album data
		albumResults=spotifyObject.artist_albums(artistID)
		albumResults=albumResults['items']

		albumSet= set({''})
		print("ALBUMS: ")
		for item in albumResults:
			#print if not a duplicate album name
			if item['name'] not in albumSet:
				albumSet.add(item['name']) 
				print(str(z)+": "+item['name'])
				albumID.append(item['id'])
				albumArt.append(item['images'][0]['url'])
				z+=1
		print()
		
		#ask for album to be displayed 
		while True:
			albumSelection= input("Enter the album number to be displayed (x to exit): ")
			if albumSelection =='x':
				break

			while not albumSelection.isnumeric() and int(albumSelection)>=z:
				albumSelection= input("Enter the album number to be displayed: ")

			#extract track data
			trackResults=spotifyObject.album_tracks(albumID[int(albumSelection)-1])
			trackResults=trackResults['items']

			n=1

			#prints all the songs in the album
			print()
			for item in trackResults:
				print(str(n)+": "+item['name'])
				trackURIs.append(item['uri'])
				n+=1
			print()

			#display the album cover
			webbrowser.open(albumArt[int(albumSelection)-1])

			songSelection= input("Enter the song number to be played (x to exit): ")
			if songSelection =='x':
				break

			while not songSelection.isnumeric() and int(songSelection)>=n:
				songSelection= input("Enter the song number to be played (x to exit): ")

			trackSelectionList=[]
			trackSelectionList.append(trackURIs[int(songSelection)-1])
				
			#comment out this line if not a premium user
			spotifyObject.start_playback(deviceID, None, trackSelectionList)	
			
			webbrowser.open(trackArt[int(songSelection)-1])

	#end the program
	if choice =='1':
		break
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))