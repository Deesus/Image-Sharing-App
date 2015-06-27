from image_sharing import app, session
from database_setup import Album, Image
from flask import jsonify

#############################################
#                  JSON requests            #
#############################################


@app.route('/albums/JSON')
def albums_json():
    """List all albums as JSON."""

    albums = session.query(Album).all()
    return jsonify(Albums=[x.serialize for x in albums])


@app.route('/album/<int:album_id>/images/JSON')
def images_json(album_id):
    """List images for given album as JSON."""

    items = session.query(Image).filter_by(album_id=album_id).all()
    return jsonify(Images=[x.serialize for x in items])


@app.route('/album/<int:album_id>/images/<int:image_id>/JSON')
def image_items_json(album_id, image_id):
    """List image info for given image as JSON."""

    item = session.query(Image).filter_by(id=image_id).all()
    return jsonify(ImageItem=[x.serialize for x in item])
