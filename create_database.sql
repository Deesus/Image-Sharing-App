/******************************************
* Author: Dee Reddy
*
* Quick Start:
*	- from vagrant, move the root directory
*	- type `$ psql -f create_database.sql`
*	- the database will now be created
*
* Troubleshooting:
*   - this file resets the password for the user 'vagrant'
*   - if you are having permission issues, consider giving this command instead:
*		`$ sudo -u vagrant psql -f create_database.sql`
*******************************************/


-------------------------------------------
-- CREATE new DATABASE instance          --
-------------------------------------------

-- Check for and drop database if exists:
DROP DATABASE IF EXISTS imagesharing;
CREATE DATABASE imagesharing;

-------------------------------------------
-- Ensure correct user settings          --
-------------------------------------------

-- (Re)sets password for user 'vagrant' to default in case it was altered:
ALTER USER vagrant PASSWORD 'pass'


-- Exit from psql
\q
