## To do:
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