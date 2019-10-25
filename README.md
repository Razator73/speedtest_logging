# Speedtest Logging

This script will run speedtest and then log the results to a postgresql database.

## Setup
### Database Installation
Get postgresql installed onto the box:
```
sudo apt install \
    postgresql \
    libpq-dev \
    postgresql-client \
    postgresql-client-common -y
```
Once it is installed create a new user for the app to use (remember password):
```
sudo su postgres

createuser pi -P --interactive
```
Create the database for it to use
```
psql

create database speedtest
```
If needed edit `/etc/postgresql/9.6/main/postgresql.conf` and 
`/etc/postgresql/9.6/main/pg_hba.conf` to suit your needs.

### Code Installation
```
git clone git@github.com:Razator73/speedtest_logging.git
```
Once the code is downloaded cd into the folder and 
using [pipenv](https://realpython.com/pipenv-guide/) install dependencies
(I also really like [pyenv](https://realpython.com/intro-to-pyenv/) to manage python
versions)
```
pipenv install
```
Once that is installed activate the virtual environment set the environment by copying
and editing the two configuration files `alembic.template.ini` (line 38) and `template.env` 
with the postgresql url from your database.
```
cp alembic.template.ini alembic.ini
nano alembic.ini

cp template.env my.env
nano my.env
```

After the config files are set run the database migrations with: 
```
alembic upgrade head 
```

### Running the program
From within the virtual environment make sure to source your `env` file:
```
source my.env
```
Then it can be run from python with:
```shell script
python speedtest_log/get_internet_speed.py
```
Or it can be set up with `crontab` by adding a line like the following to run every hour:
```
0 * * * * . $REPO_FILE_PATH/my.env; $PYTHON_PATH $REPO_FILE_PATH/speedtest_log/get_internet_speed.py
```
The `PYTHON_PATH` can be obtained using `pipenv --py`