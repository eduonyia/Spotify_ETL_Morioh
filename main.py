"""
we create a simple script using the Spotify API to extract the song titles and artists from a Spotify
playlist and save it to a nicely formatted csv file.

The following script can be used to extract the track names and artists and save into a CSV file
"""
import csv
import os
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OUTPUT_FILE_NAME = "track_info.csv"

# change for your target playlist
PLAYLIST_LINK = "https://open.spotify.com/playlist/6A55Qcqw5oM9quuG07oQGr?si=0383b0b9a79f43f8"

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist (note: max playlist length 100)
# tracks = session.playlist_tracks(playlist_uri)["items"]
tracks = session.playlist_items(playlist_uri)["items"]

# create csv file
with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
    writer = csv.writer(file)

    # write header column names
    writer.writerow(["track", "artist"])

    # extract name and artist
    for track in tracks:
        name = track["track"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )

        # write to csv
        writer.writerow([name, artists])