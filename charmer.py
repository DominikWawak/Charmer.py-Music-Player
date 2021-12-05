
# Created By:  Dominik Wawak 


# REQUIREMENTS 
# 
# If there is a error with the dislikes or some youtube fetch,
# edit the "backend_youtube_dl.py" in the pip installation and comment out the "self._dislikes = self._ydl_info['dislike_count']"
# Install Requirements
# pip3 install python-vlc
# pip3 install pafy
# pip3 install youtube-dl
# pip3 install youtube-search-python


# >>> player.pause() #-- to pause video
# >>> player.play()  #-- resume paused video. On older versions, 
#                    #     this function was called resume
# >>> player.stop()  #-- to stop/end video

class Tune():
    

    def __init__(self,tName,tGroup,tYear,tGenre,tPlaylist,tLink):
        self.tuneName=tName
        self.tuneGroup=tGroup
        self.tuneYear=tYear
        self.tuneGenre=tGenre
        self.tunePlaylist = tPlaylist
        self.tuneLink= tLink

    def printDetails(self):
        print(self.tuneName + " - "+self.tuneGroup+" - "+str(self.tuneYear) )
    
    def toJsonFormat(self):
        return{
            "tuneName": self.tuneName,
            "tuneGroup": self.tuneGroup,
            "tuneYear": self.tuneYear,
            "tuneGenre": self.tuneGenre,
            "tunePlaylist": self.tunePlaylist,
            "tuneLink":self.tuneLink
        }


from os import linesep, truncate
import re
import pafy
import vlc
import json
from contextlib import contextmanager
import sys, os
import subprocess
import threading
import time 
from youtubesearchpython import VideosSearch


os.environ["VLC_VERBOSE"] = str("-1")
Instance = vlc.Instance('--no-xlib -q > /dev/null 2>&1')
Instance.log_unset()
player = Instance.media_player_new()
clear = "\n" * 100

FILENAME="musicLibrary.json"
library=[]
currentPlaylist=[]
musicPlying = False
nowPlaying=""



def playSong(url):
    global musicPlying
    musicPlying=True
    url = url
    video = pafy.new(url)
    # best = video.getbest()
    best=video.getbestaudio()
    playurl = best.url

   
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    
    

def searchSong(query):
    
    results = VideosSearch(query,limit=1)
    # print(results.result()['result'][0]['link'])
    # print(results.result()['result'][0])
    return results.result()['result'][0]

def playSongChoice(tuneList):
      global nowPlaying
      while True:
            choice = input("would you like to play a song? (Y/N) ")
            if(choice.upper()=="Y"):
                index = int(input("Enter the song index --> "))
                # print(library[index-1].tuneLink)
                nowPlaying=tuneList[index-1].tuneName
                playSong(tuneList[index-1].tuneLink)
                break
            elif(choice.upper()=="N"):
                break

def searchOutput():
    searchString= input("enter song you want to search for --> ")
    res = searchLibrary(searchString)
    c=1
    for t in res:
        print(c,end =" ")
        print(t.tuneName + " "+t.tuneGroup+ " " + t.tuneGenre)
        c+=1
    return res
# url = "https://www.youtube.com/watch?v=QPsQ04HolFs"
# video = pafy.new(url)
# best = video.getbest()
# playurl = best.url

# os.environ["VLC_VERBOSE"] = str("-1")
# Instance = vlc.Instance('--no-xlib -q > /dev/null 2>&1')
# Instance.log_unset()
# player = Instance.media_player_new()
# Media = Instance.media_new(playurl)
# Media.get_mrl()
# player.set_media(Media)
# player.play()


# t=threading.Thread(target=playSong)
# t.start()


# Validate Input function checks the choice the user gave in a menu and checks if it is in a certain range
#
#The return is a boolean
#
def validateInput(choice,min,max):
    if(choice in range(min,max)):
        return True
    else: 
        return False


def validateStringInput(choice):
    if(re.match(r"[\s\w]+$",choice)):
        return True
    else: 
        return False



def addToFile(data):

    with open('musicLibrary.json',"r") as openfile:
        json_obj= json.load(openfile)
        
    json_obj.append(data)
    with open("musicLibrary.json","w") as outfile:
       json.dump(json_obj,outfile,indent=4)


def readFromFile():
    
    with open('musicLibrary.json',"r") as openfile:
            json_obj= json.load(openfile)
            # print(json.dumps(json_obj, indent=1))
            #make into objects 
    for l in json_obj:
        library.append(Tune(l["tuneName"],l["tuneGroup"],l["tuneYear"],l["tuneGenre"],l["tunePlaylist"],l["tuneLink"]))
        # print(l["tuneName"])
    return json_obj

def searchLibrary(searchString):
    readFromFile()
    
    found = []
    for i in library:
        
        if searchString in i.tuneName or searchString in i.tuneGenre:
            found.append(i)
    return found



def loadAnimation():
    animation = [
                "[        ]",
                "[=       ]",
                "[===     ]",
                "[====    ]",
                "[=====   ]",
                "[======  ]",
                "[======= ]",
                "[========]",
                "[ =======]",
                "[  ======]",
                "[   =====]",
                "[    ====]",
                "[     ===]",
                "[      ==]",
                "[       =]",
                "[        ]",
                "[        ]"
                ]

    notcomplete = True

    i = 0

    while notcomplete:
        print(animation[i % len(animation)], end='\r')
        time.sleep(.1)
        i += 1
        if i>17:
            notcomplete=False

        
def menu():
    global musicPlying,nowPlaying
    print(r""" 
 ________  ___  ___  ________  ________  _____ ______   _______   ________      ________  ___    ___ 
|\   ____\|\  \|\  \|\   __  \|\   __  \|\   _ \  _   \|\  ___ \ |\   __  \    |\   __  \|\  \  /  /|
\ \  \___|\ \  \\\  \ \  \|\  \ \  \|\  \ \  \\\__\ \  \ \   __/|\ \  \|\  \   \ \  \|\  \ \  \/  / /
 \ \  \    \ \   __  \ \   __  \ \   _  _\ \  \\|__| \  \ \  \_|/_\ \   _  _\   \ \   ____\ \    / / 
  \ \  \____\ \  \ \  \ \  \ \  \ \  \\  \\ \  \    \ \  \ \  \_|\ \ \  \\  \| __\ \  \___|\/  /  /  
   \ \_______\ \__\ \__\ \__\ \__\ \__\\ _\\ \__\    \ \__\ \_______\ \__\\ _\|\__\ \__\ __/  / /    
    \|_______|\|__|\|__|\|__|\|__|\|__|\|__|\|__|     \|__|\|_______|\|__|\|__\|__|\|__||\___/ /     
                                                                                        \|___|/                                                                                     
    """)

    print("""
    1) add to library
    2) show the library
    3) Search for a song
    4) Search by Genre
    5) Delete Song
    6) 
    7) Play playlist
    8) Play any song
    9)
    10) exit
    
    """)

    
   

    if musicPlying:
        print("Now playing....  " + nowPlaying )
        print(r"""     
       _________
     _|_________|_              11 -pause 
    /             \             12 -stop
   | ###       ### |            22 -play
   | ###       ### |
    \_____________/
        """)
  
    
    opt = int(input(" -->"))
    while(not validateInput(opt,1,23)):
        opt = int(input(" -->"))
    
    if(opt == 1):
        title= input("Enter Song title ")
        while not validateStringInput(title):
             title= input("Enter Song title ")
        artist = input("Enter Artist ")
        while not validateStringInput(artist):
              artist = input("Enter Artist ")
        genre= input("Enter Genre ")
        while not validateStringInput(genre):
              genre= input("Enter Genre ")
        year = int(input("Enter song year "))
        while not validateInput(year,1500,3000):
             year = int(input("Enter song year "))
        playList=input("Enter Playlist Name ")
        while not validateStringInput(playList):
             playList=input("Enter Playlist Name ")

       



        print("adding...")
        tune =Tune(searchSong(title)["title"],artist,2021,genre,playList,searchSong(title)["link"])
        tune.printDetails()
        addToFile(tune.toJsonFormat())

        
    elif(opt== 2):
        print("This is your entire library ")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print()
        readFromFile()
        c=1
        for i in library:
            print(c,end=" ")
            i.printDetails()
            c+=1
        print()
        print()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        playSongChoice(library)



    elif(opt== 3):
        res = searchOutput()
        playSongChoice(res)


    elif(opt== 4):
        print()
    elif(opt== 5):
        res = searchOutput()
        index = int(input("Enter the index of the song you want to delete --> "))
        while not validateInput(index,0,len(res)+1):
            index = int(input("Enter the index of the song you want to delete --> "))
            if index == 0:
                break
        fullLib = readFromFile()
        print(fullLib.pop(index-1))
        print()
        print(fullLib)
        with open("musicLibrary.json","w") as outfile:
            json.dump(fullLib,outfile,indent=4)

        print("Deletig...")
    elif(opt== 6):
        
        print()
    elif(opt== 7):
        
        print()
    elif(opt== 8):
        query = input("Enter any song to play ==>")
        nowPlaying = searchSong(query)['title']
        player.stop()
        playSong(searchSong(query)['link'])
    elif(opt== 9):
        print()
    elif(opt== 11):
        player.pause()
    elif(opt== 22):
        player.play()
    elif(opt== 12):
        player.stop()
        musicPlying = False
    elif(opt== 10):
        exit()



def main():
     while True:
        print(clear)
        menu()
        t=threading.Thread(target=loadAnimation())
        t.start()
    


if __name__ =="__main__":
    main()

# notes 
# make them all into objects
# sort
# play from youtube!!!!!






