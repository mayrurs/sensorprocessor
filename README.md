# System description 

 Event-driven backend component to store and processe (weather) sensory data.

# Development 

 For development a self-contained setup including PostgresDB and Redis is configured within `docker-compose.yaml`. For convienience the most commen commands are provided within the `Makefile`. To run make commands make needs to bin installed on the dev system.  

 **Remark**: `docker-compose.yml` is only intended for development not for production (see production setup)

Some commands (alembic) require an activated virtualenv on the client host with an installed version of the package and its dependencies.

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -e ./src/
```

 ## Debugging in development mode

 Check for DEV database availability:
 `psql -h 0.0.0.0 -p 54321 -U service`

Check for api availability
 `curl 0.0.0.0:5005/healthcheck`

Check availability of the redis instance
 `redis-cli -h redis -p 63791 PING`

 Send a test message to redis 
 `PUBLISH sensor_stream '{"sensor": "temperature", "value": 14, "timestamp": "2024-12-01 12:00:00"}'`

# Database versioning 

For database versioning Alembic is used. It creates the database schema based on the ORM.  

The environment specific configuration which allows alembic to generate the schemas and handles the database migrations are defined in `env.py` and `alembic.ini`. In particular `alembic.ini` handles the connection string to the database.  

1. Alembic needs to be installed and active in the current enviornment
```zsh
    source venv/bin/activate
    pip install -e ./src/
```

2. Initiate allembic for the projet in the root level of the project.
`alembic init migrations` 

3. Create initial database schema. The required $ENV variables as configured in env.py need to be available in the current environment.  
`alembic revision --autogenerate -m "Initial"`

4. Migrate to the latest version file. This connects to the within the `DB_HOST` environment defined database and CREATE / ALTERS the database to the latest version.
`alembic upgrade head`

# Production set-up

## Basic setup

The described setup assumed that the following `ENV` variables are set in the current environment  

```zsh
DB_HOST=postgres-prod
REDIS_HOST=redis-prod
API_HOST=0.0.0.0
DB_PASSWORD=<postgres-password>
```

All components are running within their own docker container. The containers are combined within one docker network for communication. To allow binding to the containers by their container names external networks in docker-compose are used.

`docker network create sensorhub`

## PostgresDB

The database configuration can be stored within its own repository, e.g. `~/docker/postgres-prod`. For portability the data are persisted within a docker volume  

`docker volume create postgres-data-prod`

The database configuration is given by the following docker-compose.yml

```yaml
version: '3'

services:
  postgres:
    container_name: postgres-prod
    image: postgres:16.2
    environment:
      - POSTGRES_USER=service
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    ports:
      - "5432:5432"
    networks:
      - sensorhub
    volumes:
      - postgres-data-prod:/var/lib/postgresql/data

volumes:
  postgres-data-prod:

networks:
  sensorhub:
    external: true
```

The service is startet by calling 
`docker compose run`

### Database initation / migration

**Remark**: 
- To run alembic, an active python virtualenv with the sensorprocessor package installed is required.
- If the current host is not part of the docker network the `DB_HOST` variable need temporally be set to the IP of the database server instead of the container name. If the current host and the database server are within the same local network `export DB_HOST=0.0.0.0` can be used (after migration run `source .env` again to restore the ENV variables).

Instantiate / migrate the database to the latest alembic files (for alembic setup see above)
`alembic upgrade head`

Connect to the database and check if migration was succefull.
```zsh
psql -h $BD_HOST -p 5432 -U service
\dt
\q
```

## REDIS

The REDIS configuration can be stored within its own repository, e.g. `~/docker/redis-prod`. 

```yaml
services:
  redis-prod:
    image: redis:latest
    container_name: redis-prod
    ports:
      - '6379:6379'
    networks:
      - sensorhub

networks:
  sensorhub:
    external: true
```

The service is startet by calling 
`docker compose run`

## Sensorhub 

### Build and publish image
Build and tag image

`sudo docker build -t <username>/sensorhub:v0.1.0 .`

Push image to registry

`docker push <username>/sensorhub:v0.1.0`

The setup consists of postgres and redis production instances. In the described setup both are running on a NAS server each as its own docker process.  

### Run container
`docker compose -f docker-compose.prod.yml up`

**Remark**: The two sensorhub images need to be startet after the postgres and redis databases are running.