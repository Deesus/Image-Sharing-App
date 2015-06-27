/******************************************
* Author: Dee Reddy
*
* Quick Start:
*	- from vagrant, move the root directory
*	- type `psql -f create_database.sql`
*	- the database will now be created
*******************************************/


-------------------------------------------
-- CREATE new DATABASE instance          --
-------------------------------------------

-- Check for and drop database if exists:
DROP DATABASE IF EXISTS imagesharing;
CREATE DATABASE imagesharing;

\q