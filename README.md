# Creditoro API
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=creditoro_api&metric=alert_status)](https://sonarcloud.io/dashboard?id=creditoro_api)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=creditoro_api&metric=coverage)](https://sonarcloud.io/dashboard?id=creditoro_api)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=creditoro_api&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=creditoro_api)

REST API for [Creditoro](https://api.creditoro.nymann.dev), a semester 
project at SDU.


## Running in production
The suggested way to run the API in production is via [Docker]() and 
[Docker Compose]().

An example configuration can be seen in 
[production/docker-compose.yml](production/docker-compose.yml).
Remember to change configuration settings in [db.env](production/db.env).
#### First time setup
- Configure your `docker-compose.yml` file and your `.env` files as 
stated above.
- Run `./upgrade.sh`

#### Upgrading to a newer version
- Run `./upgrade.sh`

## Running locally
For local development, you have the option to run in the same way as 
production, or the following:

#### First time setup
Configure [dev-setup.sh](dev-setup.sh) to your liking, and setup a 
PostgreSQL database using the credentials specified that you have just 
configured. When the database is created, do the following:
- `source dev-setup.sh`
- `flask db upgrade`
- `flask run`

##### Upgrading to a newer version
- Run `flask db upgrade` (if any db changes)
- Run `flask run`
