#I download my music from a place called bandcamp, which delivers albums in the format 
#artist- album name - 01 first song in album, artist- album name - 02 second song in album, 
#artist- album name - 03 third song in album, cover.jpg
#each song references the cover file for their album cover

#I just got a cheap mp3 player which can track metadata, but it only lets you put music in one directory, 
#so those cover.jpg files overwrite one another when extract them to that one directory
#on top of that, this mp3 player does not respect the track number metadata, and puts tracks in alphabetical order (badly)
#essentially, the mp3 player strugles to put songs in the right order when the filename is
#artist- album name - 01 first song in album
#but the mp3 player does just fine ordering songs named like
#01 first song in album
#from my googling on the internet it seems that this has something to do with the mp3 player going off 
#ascii alphabetical order, but I really have no idea

#this code fixes these two problems by batch renaming files in a way compatible with the mp3 player
#and baking the image into each song individually.

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import os

os.chdir('/run/media/seatea/AGP-A02/Music')
album = input("Gib album name")
length = len(album)
for filename in os.listdir():
    if album in filename:        
        audio = MP3(filename, ID3=ID3) #https://askubuntu.com/a/789002
        
        try:
            audio.add_tags()
        except error:
            print("audio has tags")
        
        
        audio.tags.add(
           APIC(
              encoding=1,
              mime='image/jpg',
              type=3,
              desc=u'Cover (front)',
              data=open('/run/media/seatea/AGP-A02/Music/cover.jpg', 'rb').read()
           )
        )
        audio.save()
        
        os.rename(filename, filename[length+3:])
        
os.remove('cover.jpg')

print("done")
    