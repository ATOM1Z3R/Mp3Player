from Models import *

session = dbconnect()

def getVolume():
    volume = session.query(Settings).first()
    return volume.volume

def setVolume(value):
    if value < 101 and value > 0:
        if value == 50:
            vol = 0
        else:
            vol = value - 50
        volume = session.query(Settings).first()
        volume.volume = vol 
        session.commit()
        return f"Volume set to {value}"
    else:
        return "ERROR | Type value between 1 and 100"