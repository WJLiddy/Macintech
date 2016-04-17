from VaporUtils import VaporSong
from YTDownloader import YTDownloader
import os
import sys

def gen_vapor(bandname):
	os.system("rm album/*")
	os.system("rm samp2/*")
	YTDownloader.download_wav_to_samp2(bandname)
	for fs in os.listdir("samp2/"):
		VaporSong.vaporize_song(bandname,"samp2/"+fs)
		pass
		
sys.argv.pop(0)
name = ""
for s in sys.argv:
	name = name + s

gen_vapor(name)
