### Docker
##### Containerization concept and why docker is used?
- Containers are isolated, performing operations inside the container does not affect host enviroment.

```bash
# First docker command
docker run hello-world

# Start a ubuntu container using interactive mode
docker run -it ubuntu

# Start a debain based container for python3 using interactive mode
docker run -it python:3.13.11-slim

# Start a debain based container for python3 with the bash CLI as the insert point
docker run -it --entrypoint=bash python:3.13.11-slim
```
> Docker containers are stateless i.e. the state of the container or any operations made inside it is lost once the container is shutdown. However, a version of this docker container is saved somwher and we can actually continue from that state of the container but it is not a good practice and is a anti pattern.

```bash
docker ps -a # returns all the persistent state of the containers

docker ps -aq # returns the ids

docker rm `docker ps -aq` # removes all the persistent docker containers

```








