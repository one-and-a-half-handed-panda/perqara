# CRUD API

## Setup Guide

### Pre-requisites
1. [PostgresSQL 14 has been installed](https://www.postgresqltutorial.com/postgresql-getting-started/)
2. [uuid-ossp has been installed in your database](https://www.postgresql.org/docs/14/uuid-ossp.html)
3. [Python 3.11.4 has been installed](https://www.python.org/downloads/release/python-3114/)
4. [Virtual Environment tool has been installed](https://medium.com/analytics-vidhya/virtual-environment-6ad5d9b6af59), if you happens to use Linux or macOS I reccomend using [pyenv](https://realpython.com/intro-to-pyenv/#installing-pyenv)
5. 

### Database Setup
1. Log in to the PostgreSQL shell using the test user and access the shell using the following commands.
```
sudo su - postgres
psql
```
2. Create the Database.
```
CREATE DATABASE perqara_db;

CREATE USER <your_username> WITH ENCRYPTED PASSWORD '<your_password>';

GRANT ALL PRIVILEGES ON DATABASE testdb TO <your_username>;
```
3. Connect to the Database, when propmted for a password type in `<your_password>` that you entered earlier. 
```
psql -d perqara_db -U <your_username>
```
4. Create the `users` Table by executing the SQL commands in the `20240223_create_users_table.sql` file.
5. If you get the `ERROR: function uuid_generate_v4() does not exist`, you can try this [solution](https://stackoverflow.com/a/22446521).

### Application Setup
1. Create a `.env` file.
2. Copy the environment variables and fill out the remaining empty ones.
```
DB_USERNAME=<your_username>
DB_PASSWORD=<your_password>
DB_PORT=<PostgresSQL running port, the default is 5432>
```
3. Open the project root folder.
4. Create a virtual environment.
5. Activate the virtual environment.
```
pip install -r requirements.txt
```
6. Install the dependencies.
7. Run the application
```
python app/main.py
```

## Usage

### Opening API Docs & Executing APIs
1. Run the application.
2. Open http://localhost:8000/docs.
3. To test any API, expand the section by clicking it and then click the **Try it out** button.
4. Fill in the parameters as needed.
5. Click **Execute** button.

### Running Unit Test
1. Open the project root folder.
2. Execute the unit tests by running this command:
```
pytest -vv
```