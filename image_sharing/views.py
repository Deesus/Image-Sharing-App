from image_sharing import app, session
from database_setup import Album, Image, User
from sqlalchemy.exc import IntegrityError

from flask import render_template, flash
from flask import request, redirect, url_for
from flask import session as login_session

# imports for file [image] upload:
from flask import send_from_directory, send_file
from werkzeug import secure_filename
import os
import shutil         # for deleting a directory (N.b. only works in unix)


#############################################
#            handlers for pages             #
#############################################


# routing for album pages:
# ______________________

@app.route('/')
@app.route('/index/')
@app.route('/home/')
@app.route('/albums/')
def show_albums():
    """The main/home page where user sees all created albums."""

    albums = session.query(Album).all()

    # if logged in, render the page where user has add/delete/edit options:
    if 'username' not in login_session:
        return render_template('publicAlbums.html', albums=albums)
    else:
        return render_template('albums.html', albums=albums)


@app.route('/album/new/', methods=['GET', 'POST'])
def new_album():
    """Page for creating new album."""

    # protect page from those not logged in:
    if ('username' not in login_session):
        return redirect('/login')

    if request.method == 'POST':
        # if empty name field (i.e. user cancelled):
        if request.form['name'].strip() == '':
            return redirect(url_for('show_albums'))

        add_album = Album(name=request.form['name'],
                          user_id=login_session['user_id']
                          )
        # try committing changes:
        if not commit_changes(add_album, 'add'):
            return redirect(url_for('show_albums'))

        # create new subdirectory for images:
        add_album.file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                           str(add_album.id))
        os.makedirs(add_album.file_path)
        session.commit()

        # flash message:
        flash("New album successfully created")

        return redirect(url_for('show_albums'))
    else:
        return render_template('newAlbum.html')


@app.route('/album/<int:album_id>/edit/', methods=['GET', 'POST'])
def edit_album(album_id):
    """Page for editing album name."""

    album = session.query(Album).filter_by(id=album_id).one()

    # protect page from those not logged in:
    if 'username' not in login_session:
        return redirect('/login')
    # protect page from unauthorized people using url to directly access:
    if login_session['user_id'] != album.user_id:
        return alert_script("edit this album")

    if request.method == 'POST':
        if request.form['name']:
            album.name = request.form['name']
            # flash message:
            flash("Album successfully edited")
            return redirect(url_for('show_albums'))
    else:
        return render_template('editAlbum.html', album=album)


@app.route('/album/<int:album_id>/delete/', methods=['GET', 'POST'])
def delete_album(album_id):
    """Page for deleting an album."""

    album = session.query(Album).filter_by(id=album_id).one()

    # protect page from those not logged in:
    if 'username' not in login_session:
        return redirect('/login')
    # protect page from unauthorized people using url to directly access:
    if login_session['user_id'] != album.user_id:
        return alert_script("delete this album")

    if request.method == 'POST':

        # we want to delete all items recursively when we delete a album:
        album_images = session.query(Image).filter_by(album_id=album_id).all()
        for x in album_images:
            session.delete(x)

        # try committing changes:
        if not commit_changes(album, 'delete'):
            return redirect(url_for('show_albums'))

        # delete media folder:
        shutil.rmtree(album.file_path)

        # flash message:
        flash("Album successfully deleted")

        return redirect(url_for('show_albums'))
    else:
        return render_template('deleteAlbum.html', album=album)


# routing for image pages:
# ___________________________

@app.route('/album/<int:album_id>/')
@app.route('/album/<int:album_id>/images/')
def show_images(album_id):
    """Page that shows all images in the album."""

    album = session.query(Album).filter_by(id=album_id).one()
    images = session.query(Image).filter_by(album_id=album_id).all()

    # check to see if images belong to creator of the images:
    creator = get_user_info(album.user_id)

    # if user is creator, render the page where he has add/delete/edit options:
    if 'username' not in login_session or \
            (creator.id != login_session['user_id']):
        return render_template('publicImages.html', album=album, images=images)
    else:
        return render_template('images.html', album=album, images=images)


@app.route('/album/<int:album_id>/image/new/', methods=['GET', 'POST'])
def new_image(album_id):
    """Page for adding image to album."""

    album = session.query(Album).filter_by(id=album_id).one()

    # protect page from those not logged in:
    if 'username' not in login_session:
        return redirect('/login')
    # protect page from unauthorized people using url to directly access:
    if login_session['user_id'] != album.user_id:
        return alert_script("create a new image")

    if request.method == 'POST':

        # for handling image upload:
        file_ = request.files['file_']
        # check if a file was uploaded and filename is valid:
        if file_ and allowed_file(file_.filename):
            file_name = secure_filename(file_.filename)
            file_path = album.file_path + "/" + file_name
            file_.save(file_path)

        else:
            flash("Please select a valid file to upload")
            return redirect(url_for('show_images', album_id=album_id))

        # create Image object with all fields [name, description, file_name]
        item = Image(name         =request.form['itemName'],
                     description  =request.form['itemText'],
                     file_name    =file_name,
                     album_id     =album_id,
                     user_id      =album.user_id
                     )
        # try committing changes:
        if not commit_changes(item, 'add'):
            return redirect(url_for('show_albums'))

        # flash message:
        flash("New image successfully created: %s" % item.file_name)

        return redirect(url_for('show_images', album_id=album_id))
    else:
        return render_template('newImage.html', album=album)


@app.route('/album/<int:album_id>/image/<int:image_id>/edit/',
           methods=['GET', 'POST'])
def edit_image(album_id, image_id):
    """Page for editing image's name and description."""

    item = session.query(Image).filter_by(id=image_id).one()

    # protect page from those not logged in:
    if 'username' not in login_session:
        return redirect('/login')
    # protect page from unauthorized people using url to directly access:
    if login_session['user_id'] != item.user_id:
        return alert_script("edit this image")

    if request.method == 'POST':

        # make changes to items:
        item.name        = request.form['itemName']
        item.description = request.form['itemText']

        # try committing changes:
        if not commit_changes(item, 'add'):
            return redirect(url_for('show_albums'))

        # flash message:
        flash("Image successfully edited")

        return redirect(url_for('show_images', album_id=album_id))
    else:
        return render_template('editImage.html', album_id=album_id, item=item)


@app.route('/album/<int:album_id>/image/<int:image_id>/delete/',
           methods=['GET', 'POST'])
def delete_image(album_id, image_id):
    """Page for deleting image from album."""

    item = session.query(Image).filter_by(id=image_id).one()
    album = session.query(Album).filter_by(id=album_id).one()

    # protect page from those not logged in:
    if 'username' not in login_session:
        return redirect('/login')
    # protect page from unauthorized people using url to directly access:
    if login_session['user_id'] != item.user_id:
        return alert_script("delete this image")

    if request.method == 'POST':

        # delete image, if exits:
        if item.file_name:
            os.remove(os.path.join(
                app.config['UPLOAD_FOLDER'], str(album_id), item.file_name))

        # try committing changes:
        if not commit_changes(item, 'delete'):
            return redirect(url_for('show_albums'))

        # flash message:
        flash("Image successfully deleted")

        return redirect(url_for('show_images', album_id=album_id))
    else:
        return render_template('deleteImage.html', album=album, item=item)


# routing for image upload/retrieval:
# ______________________


@app.route('/media/<album_id>/<file_name>')
def media(album_id, file_name):
    """Returns file to browser -- i.e. allows access to static files"""

    return send_file(("uploaded/%s/" + file_name) % str(album_id))


#############################################
#               helper functions            #
#############################################


# specify save folder and acceptable file types:
UPLOAD_FOLDER = './image_sharing/uploaded'
ALLOWED_EXTENSIONS = frozenset(['jpg', 'jpeg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(file_name):
    """Checks if file is an allowed file extension.

        If '.' is in the filename and the extension is in the
        allowed extensions returns boolean.

        Returns:
            True if file_name is valid.
            None if file_name is invalid.
    """

    return '.' in file_name and (file_name.split('.')[1] in ALLOWED_EXTENSIONS)


def commit_changes(item, crud_function='add'):
    """Commit CRUD changes with proper error catching."""

    try:
        if crud_function == 'add':
            session.add(item)
        else:
            session.delete(item)
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        flash("An error occurred while trying to %s" % crud_function)
        return None


def alert_script(str_message):
    """Javascript alert message if user tries to access restricted page."""

    return ("<script>function myFunction() {"
            "alert('You are not authorized to %s. "
            "Please login to continue!');}"
            "</script><body onload='myFunction()''>"
            % (str_message))


def get_user_info(user_id):
    """Returns User object given user_id."""

    user_object = session.query(User).filter_by(id=user_id).first()
    return user_object
