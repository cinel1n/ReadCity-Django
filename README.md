# if the virtual environment is not activated
source .venv/bin/activate 

# assemble the project
docker compose build

# adding data to the database
docker cp read_city_data.sql read-city-db-1:/tmp/
docker compose exec db psql -U postgres -d readcityapp -f /tmp/read_city_data.sql

# launch a project
docker compose up -d

# if a server error occurs - ports are unavailable: Granting port TCP 0.0.0.0:6379 -> 127.0.0.1:0: 
# Listening tcp 0.0.0.0:6379: Binding: Address already in use
sudo systemctl stop redis

# stop project
docker compose down
