from flask import Blueprint, render_template, flash, redirect, request, current_app
from werkzeug import exceptions

errorhandlermold = Blueprint('errorhandler', __name__)

@errorhandlermold.app_errorhandler(exceptions.RequestEntityTooLarge)
def request_entity_too_large(e):
    flash('File too large.', category='error')
    return redirect(request.url)

@errorhandlermold.app_errorhandler(exceptions.NotFound)
def not_found(e):
    return redirect('/errorpages/404')
