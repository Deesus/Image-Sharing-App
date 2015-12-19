# Image Sharing App
###### A similar, but older prototype can be [found here](http://54.186.19.143)

![app demo](https://raw.githubusercontent.com/Deesus/Image-Sharing-App/master/demo_image.jpg "Image of App")

### Upload and Share Images
The **Image Sharing App** is a Flask-based web app that that allows users to upload and share images. The app allows users to create public albums; it implements 3-party OAuth2 to give ownership of albums and images to the creators/uploaders. Users can freely access and view images from any album, but only the authorized users may add/edit/delete their own images and albums.

### Installation
1. If you don't already have Vagrant VM, you can [download it here](https://www.virtualbox.org/wiki/Downloads) and install it on your machine.
2. Clone/download the [latest release of Image Sharing App](https://github.com/Ogodei/Image-Sharing-App/archive/master.zip) from GitHub.
3. From the terminal, cd to the cloned directory (you should see the included `Vagrantfile`).
4. Enter `vagrant up` to launch the virtual machine. Wait for the dependencies to be downloaded. 
5. Then type `vagrant ssh` to log in.
6. Issue `cd /vagrant`.
7. Create the database with `psql -f create_database.sql`
8. Finally, launch the app with `python start_server.py`

### Usage
Users must sign in before they can add/edit/delete albums and images. However, they can view any extant albums/images.

- add album: user may add an album, which is simply a collection of images.
- edit album: user may edit the name of album.
- delete album: user may delete an album -- this will also delete all images
    within that album.
- add image: once an album is created, a user may add images to his album.
    He may optionally add a title and description for that image.
- edit image: user may edit the image's name and description.
- delete image: user may delete an image.
- retrieve JSON info: user may request a JSON output for albums and images:
    - for api of all albums, enter `./albums/JSON` in your browser
    - for api of a specific album, enter `./album/<album_id>/images/JSON` in your browser -- where `<album_id>` is the integer of the album's id.
    - for api of a specific image, enter `./album/<album_id>/images/<image_id>/JSON` in your browser -- where `<album_id>` is the album's id and `<image_id>` is the image's id (both integers).
- retrieve XML info: user may request an XML output for albums and images:
    - for api of all albums, enter `./albums/XML` in your browser
    - for api of a specific album, enter `./album/<album_id>/images/XML` in your browser -- where `<album_id>` is the integer of the album's id.
    - for api of a specific image, enter `./album/<album_id>/images/<image_id>/XML` in your browser -- where `<album_id>` is the album's id and `<image_id>` is the image's id (both integers).

### What's included
Inside the **Image Sharing App** directory, you'll find the following files:
```
Image-Sharing-App/
    ├── create_database.sql
    ├── start_server.py
    ├── client_secrets.json
    ├── README.md
    ├── pg_config.sh
    ├── Vagrantfile
    ├── LICENSE
    └── image_sharing_app/
        ├── __init__.py
        ├── api_endpoints.py
        ├── database_setup.py
        ├── google_oauth.py
        ├── views.py
        ├── uploaded/
        ├── static/
        │   ├── style.css
        │   ├── g_plus_logo.png
        │   ├── header_line.png
        │   └── MANIFESTO.ttf
        └── templates/
            ├── 404Error.html
            ├── about.html
            ├── albums.html
            ├── deleteAlbum.html
            ├── deleteImage.html
            ├── editAlbum.html
            ├── editImage.html
            ├── images.html
            ├── login.html
            ├── newAlbum.html
            ├── newImage.html
            ├── publicAlbums.html
            ├── publicImages.html
            ├── xmlEndpoint.xml
            └── partials/
                ├── footer.html
                ├── head.html
                ├── headerLogedIn.html
                └── headerPublic.html
```

### Issues
1) There are known compatibility issues with newer versions of flask. The **Image Sharing App** circumvents these issues, and you should not encounter any problems -- but if you do, particularly something in the order of `TypeError: <oauth2client.client.OAuth2Credentials object at 0xb5d7e90c> is not JSON serializable`, then it is advised to downgrade flask:
```
sudo pip install flask==0.9
```

### License
MIT License. Copyright (c) 2015 Dee Reddy.
