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
		# date = datetime.datetime.now()
		# today_date = (str(date).split())[0]
		# past_week_dates = helper.getLast7Days(today_date)
		# time_accessed = (str(date.time()).split('.'))[0]
		# self.weekdays = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
		# day_iter = date.weekday()
		# self.curr_date_tracks = []

		# for item in tracks['items']:
		# 	played_date = helper.translateUTCtoEST(item['played_at'])
		# 	if past_week_dates[curr_date_iter] == played_date: #Correct
		# 		title = item['track']['name']
		# 		if item.get('context', "None:None") and item.get('context', "None:None").get('uri', "None:None"):
		# 			playlist = helper.getPlaylist(self.spotify, item['context']['uri'])
		# 		else:
		# 			playlist = "No Playlist"
		# 		track_info = {}
		# 		track_info[title]= {"artist" : item['track']['artists'][0]['name'], 
		# 		"album" : item['track']['album']['name'], "popularity" : item['track']['popularity'], 
		# 		"playlist" : playlist, "played" : self.weekdays[day_iter], "daily_repeats" : 0, "time_accessed": time_accessed}
				
		# 		if any(title in elt for elt in self.curr_date_tracks):
		# 			i = next((i for i, d in enumerate(self.curr_date_tracks) if title in d), None)
		# 			self.curr_date_tracks[i][title]['daily_repeats'] += 1
		# 		else:
		# 			self.curr_date_tracks.append(track_info)
		# 	else:
		# 		if curr_date_iter == 6:
		# 			curr_date_iter = 7
		# 			break
		# 		else:
		# 			curr_date_iter += 1

		# 		if day_iter == 0:
		# 			day_iter = 6
		# 		else:
		# 			day_iter -= 1



if __name__ == "__main__":
	m = main()
	m.setUp()
	m.getTracks()