# Macintech Plus
A ｖａｐｏｒｗａｖｅ generator hacked together at UncommonHacks 2016. Downloads audio from a video on youtube and turns it into vaporwave, and also gives it a vaporwave name. Uses python 2.7 with a bunch of dependencies. Now you too can slow some music down and call yourself an artist!

# Installation
This was only ever tested on Ubuntu 15. You'll need these dependencies:

```
sudo apt-get install sox
sudo apt-get install python-pip
sudo pip install beautifulsoup4
sudo pip install youtube-dl
sudo add-apt-repository ppa:heyarje/libav-11
sudo apt-get update
sudo apt-get install libav-tools
```

# Usage
From the root folder of this project:

```
python src/VaporMain.py youtube_query_to_vaporize
```

For example, `python src/VaporMain.py Rebecca Black Friday` will generate a WAV in a folder called rebeccablackfriday/ that sounds something like [this](https://www.youtube.com/watch?v=vn-kloj0tKc).

I put up a bandcamp with some sample songs [here](https://macintech.bandcamp.com/album/macintech-i).

