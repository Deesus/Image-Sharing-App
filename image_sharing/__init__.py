from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base
from flask.ext.seasurf import SeaSurf

#############################################

""" Image Sharing App
    (image_sharing.py)

    The Image Sharing App is a web app, similar to Flickr, Imgur, etc.,
    that allows users to upload and share images. The app allows users to
    create albums. The app implements OAuth2 to give ownership of albums
    to the creators/uploaders. Users can freely access and view images
    from any album, but only the authorized users may add/edit/delete their
    own images and albums.

    App Overview:
    -add album: user may add an album, which is simply a collection of images.
    -edit album: user may edit the name of album.
    -delete album: user may delete an album -- this will also delete all images
        within that album.
    -add image: once an album is created, a user may add images to his album.
        He may optionally add a title and description for that image.
    -edit image: user may edit the image's name and description.
    -delete image: user may delete an image.
    -retrieve JSON info: user may request a JSON output for albums and images.

    Quick Start:
    (See readme for detailed information on setting up the Image Sharing App.)
    -Setup the SQL database [image_sharing.sql] through Vagrant.
    -Run script, image_sharing.py from terminal.
"""
__author__ = ('Dee Reddy', 'eyeofpie@gmail.com')


#############################################
#            initialize framework           #
#############################################

app = Flask(__name__)
csrf = SeaSurf(app)

# create and bind ORM engine [SQLAlchemy]:
engine = create_engine(
    'postgresql+psycopg2://vagrant:pass@localhost/imagesharing')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#############################################
#             import sub-modules            #
#############################################


import image_sharing.views
import image_sharing.api_endpoints
import image_sharing.google_oauth


#############################################
#                    Main                   #
#############################################


if __name__ == '__main__':
    app.secret_key = 'simple_key'
    app.run(host='0.0.0.0', port=8000, debug=True)
