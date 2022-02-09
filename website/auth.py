from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Article, Writer
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)