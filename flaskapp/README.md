<h1 align="center">Flask App</h1>
<p align="left">
Here flask framework is used to create the application in a modular way such that the user module can be extracted and used for other applications as part of a large module collection representing functionality.

SQLAlchemy is used as an ORM to create Models representing tables in database and presenting functionality to interact with the database, abstraction what database engine is used.
</p>

## setup

- clone rep - \
    `git clone xxxxxx.git`
- change dir into flaskapp dir \
`cd flaskapp`
- create virtual environment named venv \
`python3 -m venv venv`
- activate virtual environment \
`source venv/bin/activate
- install requirements \
`pip3 install -r requirements.txt`
- ensure all environment variables in config.py are set \
`export <VAR_NAME>=<variable value>`
- start app \
`python3 -m api.v0.app` \
or with gunicorn \
`gunicorn api.v0.app:app`

## Tech Stack :poodle:
 
- Python
- pycharm
- AWS RDS
- Heroku
- Gunicorn
- Postgres


## License :lock:

This project is licensed under the Apache License - see the [LICENSE](./LICENSE) file for details.