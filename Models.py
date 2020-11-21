try:
    from sqlalchemy import Integer, String, Column, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker, backref
    from sqlalchemy import create_engine
except ImportError:
    print("sqlalchemy module is required")
    exit()

Base = declarative_base()

class PlayList(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class PLDetails(Base):
    __tablename__ = 'pldetails'

    id = Column(Integer, primary_key=True)
    element_path = Column(String(250))
    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    playlist = relationship("PlayList", backref=backref('pldetails'))

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    volume = Column(Integer)

def dbconnect():
    engine = create_engine('sqlite:///atomdb.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session
    