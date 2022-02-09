from flask import Blueprint, render_template, request, flash, jsonify
from .models import Article, Writer
from . import db
from json import loads

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return render_template('home.html')