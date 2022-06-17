#! /usr/bin/zsh

echo "Starting project setup..." 
sleep 3

echo $(pip install pip --upgrade)

echo "Code already cloned/forked? (y/n)"
read answer
sleep 1

if [[ $answer == "n" ]]; then
    echo $(git clone https://github.com/LaColorada/prode_rest.git )
    sleep 1
fi

echo "Installing required packages."
sleep 1

echo "Do you have Docker and Docker Compose installed? (y/n)"
read answer

if [[ $answer == "n" ]]; then
    echo $(pip install docker)
    echo $(pip install docker-compose-plugin)
    sleep 1
fi

echo "Running Docker."
sleep 1

echo "Database and endpoint build."
sleep 1

echo $(docker stop $(docker ps -aq))

echo $(docker compose pull pgdb)
echo $(sudo docker compose build drf-api)

echo "Database and endpoint up."
sleep 1

echo $(sudo docker compose up -d pgdb --remove-orphans)
echo $(sudo docker compose up -d drf-api --remove-orphans)
echo $(sudo docker compose exec drf-api python3 manage.py migrate)

echo "Do you want to create superuser? (y/n)"
read answer
sleep 1

if [[ "$answer" = "y" ]]; then
    echo "Creating project superuser."
    sleep 1
    echo $(docker compose exec drf-api python3 manage.py createsuperuser)
fi



