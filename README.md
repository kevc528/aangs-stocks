# aangs-stocks
Web platform with DevOps features for Aang to manage his stocks

## Web App
When you make a change to the code, update the docker image using

`docker-compose build`

Run using

`docker-compose up`

When you make a change to models, make migrations using the following commands

`docker-compose run web-app poetry run alembic revision --autogenerate`

`docker-compose run web-app poetry run alembic upgrade head`

The Postgres admin tool can be found at `localhost:5050`. You can login with username `admin@admin.com` and 
password `password`. After logging in, you can add our database server. Make sure to use the connection tab. 
Remember the database was named `postgres` in the docker compose and the username and password are also both 
`postgres`.