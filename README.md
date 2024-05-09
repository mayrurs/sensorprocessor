# Sensorprocessor
 
 Event-driven backend component to collect and store different (weather) sensory data. 

 ## Debugging in enviromental mode

 Check for DEV database availability:
 `psql -h 0.0.0.0 -p 54321 -U service`

Check for api availability
 `curl 0.0.0.0:5005/healthcheck`

Check availability of DEV redis instance
 `redis-cli -h redis -p 63791 PING`

 `redis-cli -h redis -p 63791 PING`

 Send a test message to
 `PUBLISH sensor_stream '{"sensor": "temperature", "value": 14, "timestamp": "2024-12-01 12:00:00"}'`




# Alembic 

To generate database schema from the domain model. This requires that alembic has been initalised `alembic init migrations` and the necessary configurations are set in the env.py as well as the alembic.ini file. 

## Install the package in env
`source venv/bin/activate`
`pip install -e ./src/`

## Create migration skripts 
The required $ENV variables as configured in env.py need to be available in the current environment. 

`alembic revision --autogenerate -m "Initial"`

Connect to the database and migrate to the latest version file
`alembic upgrade head`