# Rea Parocaran

import json
import requests
import sqlite3
import spotipy
import spotipy.util as util
import matplotlib as plt
# import spotipy.oath2 as oath2


class main():

	def setUp(self):
		token = util.oauth2.SpotifyClientCredentials(client_id='c4377ae42ae849ca973e121a9758f7cb', client_secret='ee52c37877084564a31c99c3209714b2')

		cache_token = token.get_access_token()
		spotify = spotipy.Spotify(cache_token)
		user = input("Enter Username: ")
		results1 = spotify.user_playlists(user, limit=20, offset=0)

		for i in results1['items']:
			print(i['name'])		
		self.conn = sqlite3.connect('database.sqlite')
		self.cur = self.conn.cursor()

		#write to file
		file = open('playlists.json', 'w')
		f = json.dumps(results1)
		file.write(f)

		for i in range(5):
			choice = input('Enter playlist name: ')
			for x in results1['items']:
				if choice == x['name']:
					playlist_id = x['id']
					print('playlist_id')
					self.results2 = spotify.user_playlist_tracks(user, playlist_id = playlist_id, limit = 20, offset=0)
					file = open('songs.json', 'w')
					f = json.dumps(self.results2)
					file.write(f)
					self.songs = {}
					for item in self.results2['items']:
						if item['track']['name'] not in self.songs:
							self.songs[item['track']['name']] = item['track']['popularity']
					print(self.songs)
					self.cur.execute('''CREATE TABLE IF NOT EXISTS Songs
					(Title TEXT, Popularity INTEGER) ''')
					for item in self.songs.items():
						self.cur.execute('''INSERT INTO Songs (Title, Popularity) VALUES (?, ?)''', (item[0], item[1]))
					self.conn.commit()
					print('successful')
				else:
					pass
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




if __name__ == "__main__":
	m = main()
	m.setUp()
	#m.fillTable()