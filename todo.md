## most recent TODO:
-image sharing app:
	-create home/index page:
		-have a homepage that showcases user images
	-when loging in to google, create a new window instead of redirect
	-add facebook OAuth (and perhaps twitter OAuth)

	-changes to image page:
		-create temple for 'image' page such that when we click on image/thumbnail, we should be directed to a page dedicated to the image, its details, description, etc.
		-the album page SHOULDN'T show descrtiption -- just title (maybe not even that). 
		-c.f. the structure of imgur/flickr/etc. for ideas.
		-add date image is added

	-front-end:
		-add frames (for top/header) to keep it DRY
		-move 'log-in'/'log-out' to menu bar (instead of middle of header)
		-change google sign-in button
		-add xml/json enpoints button

	-other:
		-add shell script to setup app (e.g. automate the `psql -f create_databse.sql` and other stuff)
		-get pillow/custom image resizing(Java?) to work?
		-add js for user feedback (e.g. upload progress)
		-add api link in footer (i.e. how to access json/xml endpoints)

## older todo:
0) remove `/` from the external css defininatios in the html templates. (E.g. it should be `<link rel="stylesheet" href="styles.css">` not `<link rel="stylesheet" href="styles.css"/>`)

1) Create downsampled thumbnails whem viewing albums instead of viewing fully-sized image.
    - Need to change database (database_setup.py) to link each image_id with its thumbnail counterpart.
    - Flask needs to be able to find the thumbnail when we specify the image.
    - The **Pillow** package handles image resizing, but it seems to degrade the image too much. Is there a solution?
        - If you continue to use Pillow, you need to add instructions on installing dependencies to the README.
2) Implement a system to prevent images from being overwritten if they share same name.
    - It is probably safer to create a separate folder for each image instead of implementing a system to prevent overriding file/filenames.
3) Give the app a name.
4) When loggin in should redirect to the previous page rather than returning user back to main page (e.g. if they log in whilst on viewing album, they should be redirected back to their album page).
5) Does Flask auto sanitize input (to prevent bobby tables, etc.)?
6) Add progress bar for file upload (requires JS).
7) Create a more fleshed-out site:
    - create a homepage
    - add a footer
    - instead of repeating html snippets, create frames for header, footer, etc.
    - add more styling and JS.
8) When clicking on an image in an album, the user should be taken to a 
9) Limit size of uploads, decompression bombs, DDoS, and similar attacks.
10) Add function to main Python file to connect to and create database instead of using .sql file.