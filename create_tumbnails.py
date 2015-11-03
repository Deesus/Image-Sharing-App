"""
#### In order to install the "Pillow" package:
The Pillow package is a popular fork of PIL that handles image manipulation; particularly, image resizing. We need to go through the following steps to install these libraries/dependancies before we can use Pillow:

1. You will need to install a package called *python-dev* (for Ubutnu/Debian), which includes header files, a static library and other tools for building modules. Install via terminal:

```
sudo apt-get install python-dev
```

2.  install libjpeg-dev so that Pillow can process jpg/jpeg files:

```
sudo apt-get install libjpeg-dev
```

3. intall zlib1g-dev so that Pillow can process png files:

```
sudo apt-get install zlib1g-dev
```

4. Intall the image resizing module, Pillow:

```
sudo pip install -I Pillow
```
"""

# for resampling image (downsizing to tumbnails):
from PIL import Image as PIL_Image


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

            # create thumbnail -- (uncomment to add functionality):
            thumbnail = resize(file_path)
            if thumbnail: 
            	thumbnail.save(
            		os.path.join(album.file_path,"thumbnail_"+file_name))
            else: 
            	return redirect(url_for('show_images', album_id=album_id))

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



def resize(file_path):
    """Resizes (downsamples) image to create tumbnails.

    N.b. the app currently doesn't use this function or the Pillow module
    to create thumbnails as the endresults [downsampled images]
    are below average quality images.
    """

    try:
        img = PIL_Image.open(file_path)
    except IOError:
        return None

    # if image is already small, we don't need to resize thumbnail
    if max(img.size) <= 190:
        return img

    # reduce image to 190px max:
    x, y = img.size
    constant = 190 / float(max(x, y))
    tumbnail = img.resize((int(x*constant), int(y*constant)))

    return tumbnail
