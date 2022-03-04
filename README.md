# How to run the website

Make sure python3 is installed

Install all of the modules within requirements.txt, to do this easily, use within cmd in the zillosite directory:

```
pip install -r requirements.txt
```

If no errors have appeared, open and execute main.py

# How to edit the columns of existing databases 

If you so want to change the database columns, add or remove some, use the command:

```
flask db init
```

If you get an error like the one below:

```
Error: Could not locate a Flask application. You did not provide 
the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" 
module was not found in the current directory.
```

Make sure your terminal is within the zillosite directory and use `$env:FLASK_APP="website/__init__.py"` and try again it then should work.

Then add / remove columns from any of the existing databases within the models.py file within the website directory then enter the command below:

```
flask db migrate
```

If no errors have appeared then use:

```
flask db upgrade
```

If no errors have appeared then its all done.