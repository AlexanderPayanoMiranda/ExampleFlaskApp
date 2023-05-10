# Simple Flask App
This is a simple application for demo purposes and teach basic Flask and SQLAlchemy sintaxis.

To execute this project the following steps are needed:
1. Install all libraries required using `pip install -r requirements.txt`
2. Create a `.env` file that is going to have our app configuration.
3. In the `.env` file, add the following:
* APP_SECRET="THIS_IS_A_SECRET"
* SQLALCHEMY_DATABASE_URI="sqlite:///users.sqlite3"
* SQLALCHEMY_TRACK_MODIFICATIONS=False"
4. Execute the application with `python main.py`