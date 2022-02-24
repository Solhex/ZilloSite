from flask import Blueprint, render_template, request, flash, jsonify
from .models import Article, Writer
from . import db
from json import loads
from datetime import datetime

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

@views.route('/article-manager', methods=['GET', 'POST']) #should be hidden
def articleManager():
    page_settings = {
        'cover_picture': False,
        'current_page': 7,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/',
        '/article-d-viewer'
    ]
    
    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'writer':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            picureurl = request.form.get('pictureurl')
            if len(firstname) <= 0:
                flash('firstname is too short.', category='error')
            elif len(lastname) <= 0:
                flash('lastname is too short.', category='error')
            else:
                new_writer = Writer(firstname=firstname, lastname=lastname, picture_link=picureurl)
                db.session.add(new_writer)
                db.session.commit()
                flash('Writer added.', category='success')
        elif form_name == 'article':
            writerid = request.form.get('writerid')
            date = request.form.get('date')
            title = request.form.get('title')
            description = request.form.get('description')
            content = request.form.get('content')
            ytembed = request.form.get('ytembed')
            
            dsplit = date.split('-')
            writer_check = Writer.query.filter_by(id=writerid).first()
            if not writer_check:
                flash('Writer does not exist.', category='error')
            elif datetime(dsplit[0],dsplit[1],dsplit[2]) > datetime.now():
                flash('Date cannot be in the future.', category='error')
            elif len(title) <= 7:
                flash('Enter a title with more then 7 characters.', category='error')
            elif len(content) <= 50:
                flash('Content must be more then 50 characters long.', category='error')
            else:
                new_article = Article(writer_id=writerid, date=date, title=title, description=description, content=content, youtube_embed_link=ytembed)
                db.session.add(new_article)
                db.session.commit()
                flash('Article added.', category='success')
    
    return render_template(
        'article-manager.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )
    
@views.route('/article-d-viewer', methods=['GET']) #should be hidden
def articleDatabaseViewer():
    page_settings = {
        'cover_picture': False,
        'current_page': 7,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]
    dbwriters = Writer.query.all()
    dbarticles = Writer.query.all()
    
    return render_template(
        'article-d-viewer.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        writers=dbwriters,
        articles=dbarticles)