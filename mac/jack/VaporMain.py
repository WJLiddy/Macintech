from VaporUtils import VaporSong
from YTDownloader import YTDownloader
import os
import sys

def gen_vapor(bandname):
	os.system("rm mac/jack/album/*")
	os.system("rm mac/jack/samp2/*")
	YTDownloader.download_wav_to_samp2(bandname)
	for fs in os.listdir("mac/jack/samp2/"):
		VaporSong.vaporize_song(bandname,"mac/jack/samp2/"+fs)
		pass
