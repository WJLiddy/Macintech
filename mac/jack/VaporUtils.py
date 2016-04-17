import os
import subprocess
import re
from random import randint

CONFIDENCE_THRESH = 0.02

class VaporSong:
	# Slows downs src by rate and returns it in dest.
	@staticmethod
	def slow_down(src, rate, dest):
		cmd = "sox " + src + " " + dest + " speed " + str(rate)
		os.system(cmd)
		return dest

	# There are a LOT of reverb options. This is basic but it works for now.
	@staticmethod
	def reverbize(src, dest):
		cmd = "sox " + src + " " + dest + " reverb 100"
		os.system(cmd)
		return dest

	@staticmethod
	def crop(src,dest,start,dur):
		cmd = "sox " + src + " " + dest + " trim " + " " + str(start) + " " + str(dur)
		os.system(cmd)

	@staticmethod
	def random_crop(src, max_sec_len, dest):
		out = subprocess.check_output(["soxi","-D",src]).rstrip()
		f_len = int(float(out))
		if (f_len <= max_sec_len):
			os.system("cp " + src + " " + dest)
			return
		else:
			start_region = f_len - max_sec_len
			start = randint(0,start_region)
			cmd = "sox " + src + " " + dest + " trim " + " " + str(start) + " " + str(max_sec_len)
			os.system(cmd)

	@staticmethod
	def fetchbeats(src):
		beat_matrix = []
		beats = subprocess.check_output(["./get-beats",src]).rstrip()
		beats_ary = beats.splitlines()
		for i in beats_ary:
			record = i.split()
			record[0] = float(record[0])/1000.0
			record[1] = float(record[1])
			beat_matrix.append(record)
		return beat_matrix

	@staticmethod
	def split(src,beat_matrix):
		split_files = []
		for i in range(0,len(beat_matrix)-1):
			if(beat_matrix[i] > CONFIDENCE_THRESH):
				dur = (beat_matrix[i+1][0] - beat_matrix[i][0])
				out = src.split(".")[0]+str(i)+".wav"
				VaporSong.crop(src,out,beat_matrix[i][0],dur)
				split_files.append(out)
		return split_files

	@staticmethod
	def combine(sections,dest):
		tocomb = []
		tocomb.append("sox")
		for section in sections:
			for sample in section:
				tocomb.append(sample)
		tocomb.append(dest)
		subprocess.check_output(tocomb)
		return dest

	@staticmethod
	def generate_sections(ary):
		sections = []
		beats = [4,6,8,9]
		index = 0
		while(index != len(ary)):
			current_beat = beats[randint(0,len(beats)-1)]
			new_section = []
			while((current_beat != 0) and (index != len(ary))):
				new_section.append(ary[index])
				current_beat -= 1
				index += 1
			sections.append(new_section)
		return sections

	@staticmethod
	def dup_sections(sections):
		new_section = []
		for section in sections:
			new_section.append(section)
			if(randint(0,1) == 0):
				new_section.append(section)
		return new_section

	@staticmethod
	def make_passages(sections):
		passages = []
		index = 0
		while(index != len(sections)):
			passage_len = randint(1,4)
			passage = []
			while(index != len(sections) and passage_len > 0):
				passage.append(sections[index])
				index += 1
				passage_len -= 1
			passages.append(passage)
		return passages

	@staticmethod
	def loop_passages(passages):
		new_passages = []
		passage_count = randint(5,12)
		while(passage_count != 0):
			passage = passages[randint(0,len(passages)-1)]
			passage_count -= 1
			dup = randint(1,4)
			while(dup != 0):
				dup -= 1
				new_passages.append(passage)
		return new_passages

	@staticmethod
	def flatten(passages):
		sections = []
		for passage in passages:
			for section in passage:
				sections.append(section)
		return sections

	@staticmethod
	def vaporize_song(bandname,fname):
		# Slow down sample by 30%
		#name here

		print "~Slowing down the music"
		VaporSong.slow_down(fname, 0.7, "mac/jack/samp/out.wav")
		# Randomly crop to a minute of the song
		print "~Cropping"
		VaporSong.random_crop("mac/jack/samp/out.wav",60,"mac/jack/samp/outcrop.wav")
		# Get a list of beats
		print "~Doing Beat Analysis"
		bm = VaporSong.fetchbeats("mac/jack/samp/outcrop.wav")
		# Split into an array of strings repping beats
		print "~Split into beats"
		splitd = VaporSong.split("mac/jack/samp/outcrop.wav",bm)
		#group beats to sections
		print "~Divide into sections"
		sections = VaporSong.generate_sections(splitd)
		#loop a couple
		print "~Duping Sections"
		sdup = VaporSong.dup_sections(sections)
		#group secs to passages
		paslist = VaporSong.make_passages(sdup)
		#Reorder packages
		pasloop = VaporSong.loop_passages(paslist)
		sectionflat = VaporSong.flatten(pasloop)
		print "~Mastering & Reverbing"
		VaporSong.combine(sectionflat,"mac/jack/samp/out_norev.wav")
		preface = "mac/templates/mac/" + bandname
		os.system("mkdir " + preface)
		VaporSong.reverbize("mac/jack/samp/out_norev.wav",preface+"/"+fname.split("/")[1]+".wav")
		os.system("rm mac/jack/samp/*")
