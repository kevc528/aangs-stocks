# Aang's Stocks

![alt text](https://www.pngitem.com/pimgs/m/375-3756954_avatar-aang-png-transparent-png.png)

Web platform with DevOps features for Aang to manage his stocks

## Cloud deployment:

Assuming Kevin has the database running...

Push a change to GitHub to run the web app and cronjob! 
This also performs any database migrations for the running postgres database.

The app is reachable at `kevc528.cis188.org`


-----------------
## Manual cloud deployment:

Go to aws.cloud.upenn.edu and login

Go to https://console.aws.amazon.com/iam/home?region=us-east-1#/users/YOUR_PENNKEY_HERE?section=security_credentials (replace YOUR_PENNKEY_HERE with your pennkey [letters, not numbers]). Create an access key and add it to the aws cli by running `aws configure`

Create an access key for your user, and don't close out of the confirmation window with the key visible.

Run aws configure and enter the Access Key ID and the Secret Key from the confirmation window.

To generate the kubeconfig, run `aws eks --region us-east-1 update-kubeconfig --name cis188 --role-arn arn:aws:iam::474844133309:role/YOUR_PENNKEY_HERE --alias cis188`, again replacing YOUR_PENNKEY_HERE with your pennkey.
Next, set the default kubectl namespace with `kubectl config set-context --current --namespace=YOUR_PENNKEY_HERE`

Go to the repository's root directory.

Replace PENNKEY occurrences in manual-web-app-values.yaml with your own PENNKEY. Additionally, make sure to 
fill out email credentials and choose a JWT secret in the environment section.

Run the postgres database with 
`helm upgrade --install db ./helm-db/`

Run the web-app & cronjob with
`helm upgrade --install -f manual-web-app-values.yaml app ./helm-app/`

This also performs any database migrations for the running postgres database.

You can end the web-app/cronjob with:
`helm uninstall app`

and remove/clear the database with
`helm uninstall db`

-----------------
## Local deployment with docker-compose

If you want to run locally with docker, make sure to change the docker-compose file to have the correct 
environment variables for email and email password.

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

Run the cronjob using

`docker-compose run web-app poetry run python email_job.py`
