
# get docker image
docker pull postgres
docker run --name DbSampleAppPG -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
docker stop DbSampleAppPG
docker start DbSampleAppPG

# get sqlalchemy
poetry add sqlalchemy psycopg2
poetry add sqlalchemy-utils
