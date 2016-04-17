import urllib
import urllib2
from bs4 import BeautifulSoup
import youtube_dl
import os
import re
import subprocess
from Name import Namer
MAX_LEN = 60 * 10
class YTDownloader:

	@staticmethod
	def fetch(textToSearch):
		query = urllib.quote(textToSearch)
		url = "https://www.youtube.com/results?search_query=" + query
		response = urllib2.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html)

		vids = []
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		    vids.append('https://www.youtube.com' + vid['href'])
		return vids

	@staticmethod
	def download(link):
		if('user' in link or 'list' in link ):
			return False
		try:
			r = youtube_dl.YoutubeDL().extract_info(link,download = False)
			title = re.sub(r'([^\s\w]|_)+', '', r['title'])
			savename = ("samp2/" + title +".%(ext)s")
			if (r['duration'] > MAX_LEN):	
				return False	
			subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "wav" ,"-o", savename,link])
			return True
		except youtube_dl.utils.DownloadError:
			return False
		except ExtractorError:
			return False

	@staticmethod
	def dl_some(count,links):
		for link in links:
			if(count == 0):
				return
			if(YTDownloader.download(link)):
				count -= 1


	@staticmethod
	def download_wav_to_samp2(band):
		YTDownloader.dl_some(1,YTDownloader.fetch(band))
		for f in os.listdir("samp2/"):
			new_name = f.split(".")[0].lower()
			for s in band.split():
				new_name = new_name.replace(s,'')
			new_name = Namer.vaporname(new_name).replace('(','').replace(')','')
			os.rename("samp2/"+f,"samp2/"+new_name)
