from flask import Blueprint, flash, redirect, request       # imports the propper functions from flask
from werkzeug import exceptions                             # imports exceptions werkzeug

errorhandlermold = Blueprint('errorhandler', __name__)      # sets errorhandlermold as the blueprint errorhandler and uses __name__ to know where it is defined all URLs associated with this blueprint will have its url_prefix prepended

@errorhandlermold.app_errorhandler(exceptions.RequestEntityTooLarge)        # a decorator that calls the function below when the error corrosponding to RequestEntityTooLarge, happens when a file larger then the preset max file upload is made, is made to the flask server
def request_entity_too_large(e):                                            # sets the function to be called on by flask while passing the decorator's error code
    flash('File too large.', category='error')                              # sends a message to the flash js to message the user warning them
    return redirect(request.url)                                            # redirects the user to their current url

@errorhandlermold.app_errorhandler(exceptions.NotFound)     # a decorator that calls the function below when the error corrosponding to NotFound, happens when the user requests for a page that doesn't exist, is made to the flask server
def not_found(e):                                           # sets the function to be called on by flask while passing the decorator's error code
    return redirect('/errorpages/404')                      # redirects the user to the 404 page
