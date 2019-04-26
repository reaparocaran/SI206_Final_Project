# Rea Parocaran

import json
import requests
import sqlite3
import spotipy
import spotipy.util as util
import matplotlib as plt


class main():
	def setUp(self):
		# username = input('Enter Spotify username: ')
		token = util.prompt_for_user_token(
			username = 'reaprince18', scope = 'user-top-read', client_id = 'c4377ae42ae849ca973e121a9758f7cb', 
			client_secret = 'f51fb405a4e949ec944ec9eae10137e1', 
			redirect_uri = 'https://www.si.umich.edu/')
		if token:
			print('token')
			self.spotify = spotipy.Spotify(auth = token)
			self.conn = sqlite3.connect('database.sqlite')
			self.cur = self.conn.cursor()
		else:
			print("Can't get token for " + username)
			return None

	def getTracks(self):
		tracks = self.spotify.current_user_top_tracks(limit=20, time_range='long_term')

		# write tracks to json
		print(type(tracks))
		file = open('top_tracks.json', 'w')
		f = json.dumps(tracks)
		file.write(f)
		songs = {}

		for item in tracks['items']:
			if item['name'] not in songs:
				songs[item['name']] = item['popularity']
		print(songs)



if __name__ == "__main__":
	m = main()
	m.setUp()
	m.getTracks()