docker-compose build
docker-osx-dev &
docker-compose up
# docker-compose run web /usr/local/bin/python manage.py collectstatic --noinput
docker-compose run --name spotica web /usr/local/bin/python manage.py migrate
