# Problems:
Kombu 4.6.4 ain't working (needed to ssh in to linux system originally)
Docker is confusing at first
Default JSON serializer can't handle byte stream (change to pickle)
Have to install gcc to install some pip packages in the container
HOW DO YOU CONNECT TO A DOCKER NETWORK PFFFFFFFFFFFFFFFFF

# Commands
virtualenv service_env
source service_env/bin/activate   

docker network create invictus_net   
docker run --network invictus_net -p 5672:5672 --hostname nameko-rabbitmq --name rabbit rabbitmq:3
docker build --tag invictus-service .   
docker run --network invictus_net --name invictus_service invictus-service 
nameko shell --config shell_config.yml       

docker start|stop rabbit
docker start|stop invictus_service

# Test
pytest test/test.py  