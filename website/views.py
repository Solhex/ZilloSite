from flask import Blueprint, render_template, request, flash, jsonify
from .models import Article, Writer
from . import db
from json import loads

views = Blueprint('views', __name__)

@views.route('/')
def home():
    page_settings = {
        'cover_picture': True,
        'current_page': 1,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    return render_template(
        'home.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/articles')
def articles():
    page_settings = {
        'cover_picture': True,
        'current_page': 2,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    return render_template(
        'articles.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/events')
def events():
    page_settings = {
        'cover_picture': True,
        'current_page': 3,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    return render_template(
        'events.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/volunteer')
def volunteer():
    page_settings = {
        'cover_picture': True,
        'current_page': 4,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    return render_template(
        'volunteer.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
    )

@views.route('/support')
def support():
    page_settings = {
        'cover_picture': True,
        'current_page': 5,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    return render_template(
        'support.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/aboutus')
def aboutus():
    page_settings = {
        'cover_picture': True,
        'current_page': 6,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]
    return render_template(
        'aboutus.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/article-maker') #should be hidden
def articleMaker():
    page_settings = {
        'cover_picture': False,
        'current_page': 7,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]
    return render_template(
        'article-maker.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )
