# fampay-yt
CRUD APIs to search the database for title and description and get the videos.

This repo contains APIs for following flows:
1. GET /videos?page=1&limit=5 #gets a list of videos
2. GET  /search-videos?title= delhi&description=india 

Prerequisites - 
1. Postgres
2. Python version 3.6.8
3. virtualenv
4. redis


# Installation Steps
1. Clone the repo
2. Move to the repo
   1. `cd fampay-yt`
3. Create .env  - values shared over email
   1. create 1 database (`fampay-db`) and save the connection string in these files
   `DATABASE_URL`
   `REDIS_URL`
   ```
   [Sample]
   DATABASE_URL=postgresql://paras:postgres@localhost:5432/fampay-db
   REDIS_URL=redis://localhost:6379/1
   ```
4. Create, activate virtualenv, install requirements
   1. `virtualenv -p /path/to/python_bin venv`
   2. `source venv/bin/activate`
   3. `pip install requirements.txt`
5. Migrate db_schema, pre-seed cities
   1. `python -m app.db_migration`
   2. `psql -d car-db < app/database/city.sql`
6. Start the API, CELERY Worker and Beat
   1. `honcho start web worker cron`


#NOTES
1. For API specifications refer `Fampay-youtube.postman_collection.json`

