FROM docker
WORKDIR /usr/src/app

COPY . . 

EXPOSE 4200
# EXPOSE 5000



# CMD docker-compose up 