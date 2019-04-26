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
	def fillTable(self):
		self.cur.execute('''CREATE TABLE IF NOT EXISTS Songs
			(Title TEXT, Popularity INTEGER) ''')
		for item in songs.items():
			self.cur.execute('''INSERT INTO Songs (Title, Popularity) VALUES (?, ?)''', (item[0], item[1]))
		self.conn.commit()
		print('successful')




if __name__ == "__main__":
	m = main()
	m.setUp()
	m.getTracks()
	songs = {'PILLOWTALK': 67, "iT's YoU": 44, '': 0, 'Hymn for the Weekend': 78, 'Remember Me (Dúo)': 65, 'Work': 69, 'History': 74, 'IV. Sweatpants': 49, 'YOUTH': 68, 'Carolina': 65, 'Party': 67, 'Lights Down Low': 48, 'DNA.': 81, 'Not Too Young': 5, 'Often': 11, 'Exchange': 80, 'wRoNg': 64, "Like I'm Gonna Lose You": 79, 'Kar Gayi Chull (From "Kapoor & Sons (Since 1921)")': 46, 'Sweet Life': 60}
	m.fillTable()