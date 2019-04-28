# Rea Parocaran

import json
import requests
import sqlite3
import spotipy
import spotipy.util as util
import matplotlib.pyplot as plt
import matplotlib
import re
import plotly


class main():

	'''
	The function below is the setUp definition that allows the user to retrieve their access token
	using the client ID and client Secret provided by Spotify developer. 
	This function also creates and connects a file called database.sqlite which serves as the database 
	for the foundation of data retrieval and hold the three tables of the three APIs used in this project.
	'''
	def setUp(self):
		token = util.oauth2.SpotifyClientCredentials(client_id='c4377ae42ae849ca973e121a9758f7cb', client_secret='ee52c37877084564a31c99c3209714b2')

		cache_token = token.get_access_token()
		self.spotify = spotipy.Spotify(cache_token)
		self.user = input("Enter Username: ")
				
		self.conn = sqlite3.connect('database.sqlite')
		self.cur = self.conn.cursor()
		self.apikeymusix='e760df8ff23a565c9d73a6118db8a6e0'

	'''
	The function below makes a request to the Spotify API to retrieve the playlist information of the
	username provided above. This function prints out a list of 25 of those playlists for the user to choose from. 
	It also writes the results into a json file called playlists. 
	'''
	def getPlaylists(self):
		self.results1 = self.spotify.user_playlists(self.user, limit=25, offset=0)

		for i in self.results1['items']:
			print(i['name'])
		print(' ')
		#write to file
		file = open('playlists.json', 'w')
		f = json.dumps(self.results1)
		file.write(f)

	'''
	This function ultimatly creates a dictionary of 20 songs from 5 playlists. With the keys as the song title
	and the values as the popularity rating. This code runs 5 times to retrieve a total of 100 objects in the database.
	The code collects the name and popularity information from the playlist ID. 
	The playlist ID information is used to created the songs json file with the information of the songs in the playlist. 
	From here, the name and popularity information is stored in the Songs table of the database Database. 
	'''
	def getSongs(self):
		print("You will now be choosing 5 playlists to choose songs from.")
		for i in range(5):
			choice = input('Enter playlist name: ')
			for x in self.results1['items']:
				if choice == x['name']:
					playlist_id = x['id']
					self.results2 = self.spotify.user_playlist_tracks(self.user, playlist_id = playlist_id, limit = 20, offset=0)
					file = open('songs.json', 'w')
					f = json.dumps(self.results2)
					file.write(f)
					self.songs = {}
					for item in self.results2['items']:
						if item['track']['name'] not in self.songs:
							self.songs[item['track']['name']] = item['track']['popularity']
					print('Collected information for 20 songs in entered playlist.')
					self.cur.execute('''CREATE TABLE IF NOT EXISTS Songs
					(Title TEXT, Popularity INTEGER) ''')
					for item in self.songs.items():
						self.cur.execute('''INSERT INTO Songs (Title, Popularity) VALUES (?, ?)''', (item[0], item[1]))
					self.conn.commit()
					print('Success!')
				else:
					pass	

	'''
	This function creates a data visual with a range of different popularities and how many songs 
	are within that range. This is a bar graph. 
	'''
	def createSpotifyVisual(self):
		popularity = self.cur.execute('''SELECT Popularity FROM Songs''')
		list_pop = list(popularity)
		final_pop = []
		for i in list_pop:
			final_pop.append(i[0])

		dictionary = {'0-24': 0, '25-49': 0, '50-74':0, '75-100': 0}
		for num in final_pop:
		 	if num <= 24:
		 		dictionary['0-24'] += 1
		 	elif num >= 25 and num <= 49:
		 		dictionary['25-49'] += 1
		 	elif num >= 50 and num <= 74:
		 		dictionary['50-74'] += 1
		 	else:
		 		dictionary['75-100'] += 1
		
		labels = dictionary.items()
		
		x_nums = [1,2,3,4]
		LABELS = ['0-24', '25-49', '50-74', '75-100']

		y_nums = []
		for item in labels:
			y_nums.append(item[1])

		plt.bar(x_nums, y_nums, align = 'center', color = ['#ff4d4d', '#884dff', '#ff80bf', '#cc0066'])
		plt.xticks(x_nums, LABELS)
		plt.xlabel("Popularity Ranges")
		plt.ylabel("Number of Songs")
		plt.title("Number of Songs with Spotify Popularity")
		plt.savefig("spotify_bargraph.png")

		plt.show()
	
	# ##BEGINNING OF LINDSAY'S CODE
	

	def call4_id(self, songname):
	    search=requests.get('http://api.musixmatch.com/ws/1.1/track.search?apikey=e760df8ff23a565c9d73a6118db8a6e0&q_track='+songname)
	    search1=search.json()
	    trackobj=search1['message']['body']['track_list'] 
	    try:
	    	song_id=trackobj[0]['track']['commontrack_id']
	    	return song_id
	    except:
	    	pass


	def call4_lyric(self, song_id):
	    id=str(song_id)
	    search=requests.get('http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey=e760df8ff23a565c9d73a6118db8a6e0&track_id='+id)
	    songinfo=search.json()
	    try:
	        lyrics=songinfo['message']['body']['lyrics']['lyrics_body']
	        return lyrics
	    except:
	        pass

	def create_wordcount_dict(self):
	    list=self.cur.execute('SELECT Title from Songs')
	    songlist=[]
	    for x in list:
	    	songlist.append(x[0])
	    word_dict={}
	    for x in songlist:
	        song_id=self.call4_id(x)
        	lyricsraw=self.call4_lyric(song_id)
	        if lyricsraw!=None:
	            words=[]
	            lyrics_only=lyricsraw.replace('******* This Lyrics is NOT for Commercial use *******','')
	            lyrics_only=lyrics_only.replace('(1409618364852)','')
	            lyrics_only=lyrics_only.replace('...','')
	            lines=lyrics_only.split('\n')
	            wordlist1=[]
	            for x in lines:
	                wordlist1+=x.split(' ')
	            for x in wordlist1:
	                justword=x.strip('?')
	                justword=justword.strip('"')
	                justword=justword.lower()
	                words.append(justword)
	            for x in words:
	                if x not in word_dict:
	                    word_dict[x]=1
	                else:
	                    word_dict[x]+=1
	        else:
	            pass
	    print("Created word dictionary!")
	    self.data = sorted(word_dict.items(), key=lambda x: x[1],reverse=True)
	    self.cur.execute('CREATE TABLE IF NOT EXISTS Words (Word TEXT, Wordcount INTEGER)')

	    for x in self.data:
	        word=x[0]
	        wordcount=x[1]
	        self.cur.execute('INSERT INTO Words (Word, Wordcount) VALUES (?,?)', (word, wordcount))
	    self.conn.commit() ##needs rea connection
	    print("Added new word table in database!")
	    return self.data

	def create_visual1(self):
	    labels=[]
	    x_nums=[1,2,3,4,5,6,7,8,9,10]
	    topten=self.data[1:11]
	    for x in topten:
	        labels.append(x[0])

	    counts=[]
	    for x in topten:
	        counts.append(x[1])

	    plt.bar(x_nums, counts, align='center', color=["red", "yellow","green","blue","purple","red","yellow","green","blue","purple"])
	    plt.xticks(x_nums, labels)
	    plt.xlabel("Top 10 Most Common Words")
	    plt.ylabel("Number of Occurences")
	    plt.title("Top 10 Most Common Words in Rea's Top Spotify Songs")
	    plt.savefig("words_bargraph.png")
	    plt.show()
	    return labels 

	# ###BEGINNING OF PRIYAS CODE
	



if __name__ == "__main__":
	m = main()
	m.setUp()
	m.getPlaylists()
	m.getSongs()
	m.createSpotifyVisual()
	m.create_wordcount_dict()
	m.create_visual1()
	

# REA'S PAST CODE - IGNORE
		#write to file
		# file = open('songs.json', 'w')
		# f = json.dumps(self.results2)
		# file.write(f)

		#get the songs and popularity
		# songs = {}
		# for item in self.requests2['items']:
		# 	if item['name'] not in self.songs:
		# 		songs[item['name']] = item['popularity']


	# def setUp(self):
	# 	user = input('Enter Spotify username: ')
	# 	token = util.prompt_for_user_token(
	# 		username = user, scope = 'user-top-read', client_id = 'c4377ae42ae849ca973e121a9758f7cb', 
	# 		client_secret = 'ee52c37877084564a31c99c3209714b2', 
	# 		redirect_uri = 'https://www.amazon.com/', show_dialog = 'true')
	# 	if token:
	# 		print('token')
	# 		self.spotify = spotipy.Spotify(auth = token)
	# 		self.conn = sqlite3.connect('database.sqlite')
	# 		self.cur = self.conn.cursor()
	# 	else:
	# 		print("Can't get token for " + user)
	# 		return None

	# def getTracks(self):
	# 	tracks = self.spotify.current_user_top_tracks(limit=20, time_range='long_term')

	# 	# write tracks to json
	# 	print(type(tracks))
	# 	file = open('top_tracks.json', 'w')
	# 	f = json.dumps(tracks)
	# 	file.write(f)
	# 	self.songs = {}

	# 	for item in tracks['items']:
	# 		if item['name'] not in self.songs:
	# 			self.songs[item['name']] = item['popularity']
	# 	print(self.songs)

	# def fillTable(self):
	# 	self.cur.execute('''CREATE TABLE IF NOT EXISTS Songs
	# 		(Title TEXT, Popularity INTEGER) ''')
	# 	for item in self.songs.items():
	# 		self.cur.execute('''INSERT INTO Songs (Title, Popularity) VALUES (?, ?)''', (item[0], item[1]))
	# 	self.conn.commit()
	# 	print('successful')