# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from spotica.analysisFlow.analysis import Sentiment
from spotica.analysisFlow.lyrics import Song
import re
import json

from django.core.cache import cache
import logging
import spotipy
from datetime import datetime
from datetime import timedelta

# Initialize our django application for this external usage
from django.conf import settings

from micro.models import Post, SongPost

# This task will be triggered when a user plays a song

@shared_task
def run_analysis_on_song(spotify_uri):
	spotify_id = re.sub(r'spotify:track:', '', spotify_uri)
	sentiment = check_for_cached_sentiment(spotify_id)
	if sentiment is None:
		sp = spotipy.Spotify()
		tcks = sp.track(spotify_uri)
		name = tcks['name']
		artists = tcks['artists']
		if len(artists) > 0:
			artist = artists[0]['name']
		else:
			artist = artists['name']
		s = Song(artist=artist, title=name)
		lyrics = s.lyrics()
		if lyrics is None:
			sentiment = 0.0
		else:
			sentiment_object = Sentiment(lyrics)
			sentiment = sentiment_object.get_sentiment_score()
		cache_sentiment(spotify_id, sentiment)
	return sentiment
	# sentiment = function(song_id)

	# song.sentiment = sentiment
	# song.save()

# This task will be triggered when a user plays a song possibly by the above task
@shared_task
def update_user_timeseries(user_id):
	return
	# insert either function call or code here

# This task will be triggered once per hour as a celery-beat task
@shared_task
def update_global_timeseries():
	calculate_hourly_sentiment()
	hour = 0


def calculate_hourly_sentiment():
	# make array of all SongPosts made in the last hour
	startdate = datetime.now() - timedelta(hours=2)
	array_of_songs = SongPost.objects.filter(pub_date__gt=startdate)
	count = 0
	array_of_sentiments = []
	for song in array_of_songs:
		# convert to regular id from uri
		spotify_uri = song.spotify_uri
		spotify_id = re.sub(r'spotify:track:', '', spotify_uri)
		# cache sentiment
		#TODO: switch to redis
		sentiment = check_for_cached_sentiment(spotify_id)
		if sentiment is None:
			sentiment = run_analysis_on_song(spotify_id)
		array_of_sentiments.append(sentiment)
		count += 1
	# sum up all sentiment values
	total = 0
	for sentiment in array_of_sentiments:
		total += sentiment
	print(total)
	average_sentiment = total / (len(array_of_sentiments))
	# ADD TO THE JSON file
	to_add_to_json = {"time": str(startdate), "sentiment": average_sentiment}
	data = []
	path = settings.MEDIA_ROOT + 'global_sentiment.json'
	with open(path) as f:
		data = json.load(f)
	data.append(to_add_to_json)
	with open(path, 'w') as f:
		json.dump(data, f)


# CACHE - temporary location

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Obivously this code won't live here, just examples

# Cache sentiment for a particular song
def cache_sentiment(spotify_track_id, sentiment):
	if spotify_track_id is None or sentiment is None:
		logger.error('Trying to cache sentiment with no track id or sentiment')
		return
	cache.set('song-sentiment-' + spotify_track_id, sentiment)

# Check cache for sentiment for a particular song and returns it if found
# Returns None if not found
def check_for_cached_sentiment(spotify_track_id):
	if spotify_track_id is None:
		logger.error('Trying get song sentiment from cache with no track id')
		return
	return cache.get('song-sentiment-' + spotify_track_id)

def cache_user_sentiment_json(path, user_id):
	if path is None or user is None:
		logger.error('Trying to cache user sentiment file location with no path or user_id')
		return
	cache.set('user-sentiment-' + user_id, path)

# Get cache location of user's json
def json_file_for_user(user):
	if user is None:
		logger.error('Trying get user sentiment file location from cache with no user')
		return
	return cache.get('user-sentiment-' + user_id)

# Cache location of global sentiment
def cache_global_sentiment_json(path):
	if path is None:
		logger.error('Trying to cache global sentiment file location with no path')
		return
	cache.set('global-sentiment', path)

# Get cache location of global sentiment
def cache_global_sentiment_json():
	return cache.get('global-sentiment')