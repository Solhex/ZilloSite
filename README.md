Make sure python3 is installed

Install all of the modules within requirements.txt, to do this easily, use within cmd in the zillosite directory:

```
pip install -r requirements.txt
```

If no errors have appeared, open and execute main.py

The file migrations within the directory website is a byproduct of flask-migrations used to update databases with new columns if you so choose to add new columns add them within models.py then use:

```
flask db migrate
```

If no errors have appeared then use:

```
flask db upgrade
```

If you get the error:

```
Error: Could not locate a Flask application. You did not provide 
the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" 
module was not found in the current directory.
```

Make sure your terminal is within the zillosite directory and use ```$env:FLASK_APP="website/__init__.py"``` and try again it then should work.