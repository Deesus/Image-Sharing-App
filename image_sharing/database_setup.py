from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# for deleting content in "./uploaded" folder:
import os
import shutil

#############################################

""" Database setup for Image Sharing App.

    "database_setup.py" defines the classes/objects -- i.e. tables/columns
    that will be used by the ORM. There is no need to execute this script.
    Simply run the main module: "image_sharing.py".
"""
__author__ = ('Dee Reddy', 'eyeofpie@gmail.com')


#############################################
#                   Tables                  #
#############################################


# create instance:
Base = declarative_base()


class User(Base):
    """A table of all the users registered to use the app."""

    __tablename__ = 'user'

    # columns:
    id       = Column(Integer, primary_key=True)
    name     = Column(String(250), nullable=False)
    email    = Column(String(250), nullable=False)
    picture  = Column(String(250))


class Album(Base):
    """An album is a collection of images."""

    __tablename__ = 'album'

    # columns:
    id          = Column(Integer, primary_key=True)
    name        = Column(String(250), nullable=False)
    file_path   = Column(String)

    # foreign key relationships:
    user_id     = Column(Integer, ForeignKey('user.id'))
    user        = relationship(User)

    # for JSON/XML endpoint data:
    @property
    def serialize(self):
        return {'id':    self.id,
                'name':  self.name
                }


class Image(Base):
    """A table of images and descriptions of each image."""

    __tablename__ = 'image'

    # columns:
    id           = Column(Integer, primary_key=True)
    name         = Column(String(128))
    description  = Column(String)
    file_name    = Column(String, nullable=False)

    # foreign key relationships:
    album_id    = Column(Integer, ForeignKey('album.id'))
    album       = relationship(Album)
    user_id     = Column(Integer, ForeignKey('user.id'))
    user        = relationship(User)

    # for JSON/XML endpoint data:
    @property
    def serialize(self):
        return {'id':           self.id,
                'name':         self.name,
                'description':  self.description,
                'file name':    self.file_name
                }


#############################################
#         Finalize and Prepare App:         #
#############################################


# create engine instance and point it to the database:
engine = create_engine(
	'postgresql+psycopg2://vagrant:pass@localhost/imagesharing')
Base.metadata.create_all(engine)
