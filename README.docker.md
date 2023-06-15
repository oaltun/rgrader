# EXAMADDIN PROJECT BACKEND 


# remove network
docker stack rm exs
docker swarm leave --force

# restart network prod
docker login -u oguz211 # enter your password
git pull

## for dev docker  
docker swarm init
python3 secret_values_prod.py
bash start_swarm_dev.sh

## for prod docker
prod: 
  docker swarm init --advertise-addr 137.184.110.86
local//backend:
  ssh deployer@stylecv.com python3 < secret_values.py
local//exs_swarm: 
  python3 render_templates.py 
  git add --all
  git commit -m "message"
  git push --all
prod//exs_swarm: 
  docker stack rm exs
  git pull
  bash start_swarm_prod.sh
  docker service ls
  docker service logs -f --raw exs_backend_api
  docker exec $(docker ps -q -f name=exs_backend_api) alembic upgrade head
  docker exec $(docker ps -q -f name=exs_backend_api) python ./app/initial_data.py

# see service logs
docker service ls
docker service logs -f --raw exs_backend

# secret change:
// remove network, run secrets/set_secrets.py, then restart network

# docker cleanup.
// remove network.
// prune all containers
docker container prune

// prune all images
docker image prune

// prune unused everything
docker system prune -a

// remove all containers
docker rm -f $(docker ps -a -q)

# remove selected volumes: may erase data!
// find all volumes:
docker volume ls
// delete unvanted volumes:
docker volume rm <volume_name>


# remove all docker data. Notice: will erase database data!
docker volume rm $(docker volume ls -q)


# send new version to github/digital ocean:
git push

# run test
docker exec $(docker ps -q -f name=exs_backend_api) pytest -x

# upgrade db tables
docker exec $(docker ps -q -f name=exs_backend_api) alembic revision --autogenerate -m "message"

docker exec $(docker ps -q -f name=exs_backend_api) alembic upgrade head


# get interactive shell example
docker exec -ti $(docker ps -q -f name=exs_backend) bash

# query example
docker service ps exs_backend
docker ps -q -f name=exs_backend
docker image ls
docker service ls

# log view example
docker service logs -f exs_backend --raw
docker service ps exs_backend
docker inspect $(docker ps -q -f name=exs_backend)

# system architecture
docker info|grep Architecture