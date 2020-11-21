from Models import *
from os.path import isfile, join
from os import listdir

session = dbconnect()

def listPlayList():
    list_pl = session.query(PlayList).all()
    return list_pl

def createPlayList(plname):
    playList = PlayList(name=plname)
    session.add(playList)
    session.commit()
    added = session.query(PlayList).filter(PlayList.name==plname).order_by(PlayList.id.desc()).first()
    return f"CREATED // ID: {added.id} | Name: {added.name}"

def removePlayList(id_playlist):
    del_obj = session.query(PlayList).get(id_playlist)
    if del_obj == None:
        return "Playlist not Exist"
    session.delete(del_obj)
    session.commit()
    return "Playlist Deleted"

def addToPlayList(folder_path, playlist_id):
    pldetails = PLDetails(element_path=folder_path, playlist_id=playlist_id)
    session.add(pldetails)
    session.commit()

def findPlayList(id):
    count = session.query(PlayList).filter(PlayList.id==id).count()
    if count == 1:
        return True
    else:
        return False

def getPlayList(id):
    list_pl = []
    for record in session.query(PLDetails).filter(PLDetails.playlist_id == id):
        path = record.element_path
        for r in [i for i in listdir(path) if isfile(join(path, i))]:
            list_pl.append(join(path,r))
    return list_pl