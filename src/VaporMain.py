from VaporSong import VaporSong
from YTDownloader import YTDownloader
import os
import sys

def gen_vapor(query):
	# Make the proper folders for intermediate steps
	os.system("mkdir download/")
	os.system("mkdir beats/")

	# Delete stuff if there is anything left over.
	os.system("rm download/*")
	os.system("rm beats/*")

	# Download the youtube query's first result. Might be wrong but YOLO
	YTDownloader.download_wav_to_samp2(query)

	# For every song in download folder(just one for now)
	for fs in os.listdir("download/"):
		# Slow down the song.
		VaporSong.vaporize_song(query,"download/"+fs)
		pass
	# When we are finished, delete the old folders.
	os.system("rm -r download/")
	os.system("rm -r beats/")
	
## Makes this a command line tool: disable when we get the webserver going
sys.argv.pop(0)
name = ""
for s in sys.argv:
	name = name + s

gen_vapor(name)
