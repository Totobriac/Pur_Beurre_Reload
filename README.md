# 'PurBeurre'


Pur beurre is a app that will find for you healthier substitute for your daily foods.


### Local installation:

__*PostgreSQL must be installed on your system*__

- create a file
- clone the repo into it:
`git clone https://github.com/Totobriac/PurBeurre.git`
- set up a virtual environment:
`python3 -m venv venv`
- activate it:
`. venv/bin/activate`
- move to the main directory:
`cd Pur-Beurre`
- install the requirements: `pip3 install -r requirements.txt`
- migrate the database: `python3 manage.py migrate'
- populate the database: `python3 manage.py populate_db`
- run the server: `python3 manage.py runserver`
- go to http://127.0.0.1:8000/


### Live version:

- https://puramanteca.herokuapp.com/
