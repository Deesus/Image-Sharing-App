from image_sharing import app, session
from database_setup import Album, Image
from flask import jsonify, render_template, make_response

#############################################
#                  JSON requests            #
#############################################


@app.route('/albums/JSON')
@app.route('/albums/json')
def albums_json():
    """List all albums as JSON."""

    albums = session.query(Album).all()
    return jsonify(Albums=[x.serialize for x in albums])


@app.route('/album/<int:album_id>/images/JSON')
@app.route('/album/<int:album_id>/images/json')
@app.route('/album/<int:album_id>/JSON')
@app.route('/album/<int:album_id>/json')
def images_json(album_id):
    """List images for given album as JSON."""

    items = session.query(Image).filter_by(album_id=album_id).all()
    return jsonify(Images=[x.serialize for x in items])


@app.route('/album/<int:album_id>/images/<int:image_id>/JSON')
@app.route('/album/<int:album_id>/images/<int:image_id>/json')

def image_items_json(album_id, image_id):
    """List image info for given image as JSON."""

    item = session.query(Image).filter_by(id=image_id).all()
    return jsonify(ImageItem=[x.serialize for x in item])


#############################################
#                 XML requests              #
#############################################


@app.route('/albums/XML')
@app.route('/albums/xml')
def albums_xml():
    """List all albums as XML."""

    albums = session.query(Album).all()
    data = [x.serialize for x in albums]
    template = render_template("xmlEndpoint.xml", data=data, wrap="all_albums")
    response_ = make_response(template)
    response_.headers['Content-Type'] = 'application/xml'
    return response_

@app.route('/album/<int:album_id>/images/XML')
@app.route('/album/<int:album_id>/images/xml')
@app.route('/album/<int:album_id>/XML')
@app.route('/album/<int:album_id>/xml')
def images_xml(album_id):
    """List images for given album as XML."""

    items = session.query(Image).filter_by(album_id=album_id).all()
    data = [x.serialize for x in items]    
    template = render_template("xmlEndpoint.xml", data=data, wrap="album")
    response_ = make_response(template)
    response_.headers['Content-Type'] = 'application/xml'
    return response_


@app.route('/album/<int:album_id>/images/<int:image_id>/XML')
@app.route('/album/<int:album_id>/images/<int:image_id>/xml')
def image_items_xml(album_id, image_id):
    """List image info for given image as XML."""

    item = session.query(Image).filter_by(id=image_id).all()
    data = [x.serialize for x in item]
    template = render_template("xmlEndpoint.xml", data=data, wrap="image")
    response_ = make_response(template)
    response_.headers['Content-Type'] = 'application/xml'
    return response_
