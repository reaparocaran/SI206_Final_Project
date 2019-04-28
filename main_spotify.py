# Rea Parocaran

import json
import requests
import sqlite3
import spotipy
import spotipy.util as util
import matplotlib.pyplot as plt

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
	def createVisual(self):
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
		plt.show()



if __name__ == "__main__":
	m = main()
	m.setUp()
	m.getPlaylists()
	m.getSongs()
	m.createVisual()

# PAST CODE - IGNORE
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