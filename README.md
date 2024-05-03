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







