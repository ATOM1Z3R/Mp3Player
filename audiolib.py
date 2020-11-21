try:
    from pydub import AudioSegment
    from pydub.playback import play
except ImportError:
    print("pydub and simpleaudio module is required")
    print("ffmpeg app is required")
    exit()
try:
    from tqdm import tqdm
except ImportError:
    print("tqdm module is required")
    exit()
try:
    import keyboard
except ImportError:
    print("keyboard module is required")
    exit()
try:
    import psutil
except ImportError:
    print("psutil module is required")
    exit()
from multiprocessing import Process, Queue
from settingslib import getVolume
from os import getpid, kill, path
import time


def createAudioSegment(file_path):
    file_format = "".join(file_path.split('.')[-1:])
    audio = AudioSegment.from_file(file_path, file_format)
    return audio

def audioInfo(audio_segment, file_path):
    duration = int(audio_segment.duration_seconds)
    file_name = "".join((path.basename(file_path)).split('.')[:1])
    
    print(f"Now Playing: {file_name}")
    for _ in tqdm(range(duration), ncols=85):
        time.sleep(1)
    print("\033[A\033[A                                                       \033[A")
        
def audioStart(audio_segment):
    audio = audio_segment + getVolume()
    play(audio)

def audioController(audio_proc, status_proc, queue):
    paused = False
    terminate = False
    procs = (psutil.Process(audio_proc), psutil.Process(status_proc))
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed('alt+\\'):
            if paused == False:
                paused = True
                for p in procs:
                    p.suspend()
                time.sleep(0.3)
            else:
                paused = False
                for p in procs:
                    p.resume()
                time.sleep(0.3)
        elif keyboard.is_pressed('alt+;'):
            for p in procs:
                kill(p.pid, 9)
            print('\nTerminated by User')
            terminate = True
            break
        elif keyboard.is_pressed('alt+]'):
            print("\033[A                                                       \033[A")
            for p in procs:
                kill(p.pid, 9)
            break
    queue.put(terminate)

def startPlayList(audioList):
    for i in audioList:
        if "".join(i.split('.')[-1:]) in ['wav', 'mp3', 'mp4', 'm4a', 'flac', 'ogg']:
            try:
                terminate = Queue()
                play = Process(target=audioStart, args=(createAudioSegment(i),))
                info = Process(target=audioInfo, args=(createAudioSegment(i),i))
                play.start()
                info.start()
                ac = Process(target=audioController, args=(play.pid, info.pid, queue))
                ac.start()
                play.join()
                info.join()
                ac.terminate()
                if terminate.get():
                    break
            except FileNotFoundError:
                continue

