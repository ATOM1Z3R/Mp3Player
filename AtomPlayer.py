# simpleaudio and ffmpeg required
from Models import *
from playlistlib import *
from audiolib import *
from settingslib import setVolume
from os import listdir, system
from os.path import isdir
import sys
import getopt

def usage():
    print("""AtomPlayer
    
Usage: atomplayer.py -p [playlist_id/catalog/audio_file]
-l --list - list playlists
-c --create [playlist_name] - create playlist with given name
-a --add [playlist_id] -f --folder [catalog_path] - add catalog to playlist
-r --remove [playlist_id] - remove playlist with given id
-v --volume [value] - set volume to given value

Controlls:
alt+\\ - pause/resume audio
alt+] - next audio
alt+; - quit program

Examples:
atomplayer.py -p audio.mp3
atomplayer.py -a 4 c:\\audio\\playlist
atomplayer.py -r 9
""")

def getAudioList(catalog_path):
    audioList = listdir(catalog_path)
    return [catalog_path+"\\"+s for s in audioList]

def main():
    folder_path = ""
    clear = lambda:system("cls")
    add_flag = False

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlc:r:a:f:p:v:",
            ["help","list","create","folder","add","remove", "volume", "play"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--list"):
            for item in listPlayList():
                print(f"ID: {item.id} | {item.name}")
        elif o in ("-c", "--create"):
            print(createPlayList(a))
        elif o in ("-r", "--remove"):
            print(removePlayList(int(a)))
        elif o in ("-v", "--volume"):
            print(setVolume(int(a)))
        elif o in ("-f", "--folder"):
            folder_path = a
        elif o in ("-a", "--add"):
            add_flag = True
            playlist_id = a
        elif o in ("-p", "--play"):
            try:
                if a.isdigit() and int(a) >= 0:
                    startPlayList(getPlayList(int(a)))
                elif isdir(a):
                    startPlayList(getAudioList(a))
                else:
                    startPlayList([a])
            except KeyboardInterrupt:
                print("ERROR | Invalid argument. If file name contains spaces use quote: \"file name\".")
        
        if add_flag == True and folder_path != "":
            addToPlayList(folder_path, playlist_id)
            print("Catalog has been added")
            add_flag = False

if __name__=="__main__":
    main()
