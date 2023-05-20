# cb-backend
Backend of social network ChatterBox

## How to run

1. Clone the repository with `git clone https://github.com/itmo-chatterbox/cb-backend`
2. Go to the new directory with `cd cb-backend`
3. run `pip install -r ./requirements.txt`
4. Create a new `.env` file with content:
```
DB_USER=<login of DB user>
DB_PASS=<password of DB user>
DB_HOST=<host of DB>
DB_PORT=<port of DB>
DB_NAME=<name of DB>
SECRET_KEY=<b410ffcb40fe3f9cd37ab32dad0af9be2b30c2f379fa60e62e5c77b821a22a44>
```
5. Finally! Start it with `uvicorn main:app --reload`
6. ...
7. ...
8. ...
9. Do not remember to hide your gills properly, my dear newbie, — Zuсkerberg
