from flask import Blueprint, render_template, request, flash, redirect, current_app
from .models import Article, Writer, Subscription
from sqlalchemy import desc
from . import db
from datetime import datetime
from re import fullmatch
from os import path

views = Blueprint('views', __name__)

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def newsletterForm():
    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'email_subscription':
            email = request.form.get('newsletter')
            email_exists_check = Subscription.query.filter_by(email=email).first()
            if email_exists_check:
                flash('Email Address Already Signed Up!', category='error')
                return redirect(request.url)
            else:
                if not fullmatch(EMAIL_REGEX, email):
                    flash('Enter a valid email address.', category='error')
                    return redirect(request.url)    
                else:
                    new_subscriber = Subscription(email=email)
                    db.session.add(new_subscriber)
                    db.session.commit()
                    flash('Thanks for subscribing!', category='success')
                    return redirect(request.url)
                
@views.route('/errorpages/404', methods=['GET', 'POST'])
def error_404():
    page_settings = {
        'cover_picture': False,
        'current_page': 0,
        'footer' : True,
        'sidebar_segments':0
        }
    sidebar_links = [
        '#',
        '#'
    ]
    
    newsletterForm()

    return render_template(
        './errorpages/404.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )
                
@views.route('/', methods=['GET', 'POST'])
def home():
    page_settings = {
        'cover_picture': True,
        'current_page': 1,
        'footer' : True,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    
    newsletterForm()

    return render_template(
        './home.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/articles', methods=['GET', 'POST'])
def articles():
    page_settings = {
        'cover_picture': True,
        'current_page': 2,
        'footer' : True,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    
    newsletterForm()

    return render_template(
        './articles.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/events/events-gridview', methods=['GET', 'POST'])
def eventsGridview():
    page_settings = {
        'cover_picture': True,
        'current_page': 3,
        'footer' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '/events/events-mapview'
    ]
    
    newsletterForm()

    return render_template(
        './events/events-gridview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )
    
@views.route('/events/events-mapview')
def eventsMapview():
    page_settings = {
        'cover_picture': False,
        'current_page': 3,
        'footer' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/events/events-gridview',
        '#'
    ]

    return render_template(
        './events/events-mapview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    page_settings = {
        'cover_picture': True,
        'current_page': 4,
        'footer' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]

    newsletterForm()
    
    return render_template(
        './volunteer.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
    )

@views.route('/support', methods=['GET', 'POST'])
def support():
    page_settings = {
        'cover_picture': True,
        'current_page': 5,
        'footer' : True,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '#',
        '#'
    ]
    
    newsletterForm()

    return render_template(
        './support.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    page_settings = {
        'cover_picture': True,
        'current_page': 6,
        'footer' : True,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]

    newsletterForm()

    return render_template(
        './aboutus.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('hidden/article-manager', methods=['GET', 'POST']) #should be hidden
def articleManager():
    page_settings = {
        'cover_picture': False,
        'current_page': 0,
        'footer' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/',
        '/hidden/db-viewer'
    ]

    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'add-writer':
            if 'fileupload' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['fileupload']
            if file and allowed_file(file.filename):
                file_extention = file.filename.split('.')[-1]
                try:
                    filename = str(Writer.query.order_by(desc(Writer.id)).first().id + 1)
                except:
                    filename = str(1)
            else:
                flash('Invalid file')
                return redirect(request.url)
                    
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            if len(firstname) <= 0:
                flash('firstname is too short.', category='error')
                return redirect(request.url)
            elif len(lastname) <= 0:
                flash('lastname is too short.', category='error')
                return redirect(request.url)
            else:
                if file.filename == '':
                    new_writer = Writer(firstname=firstname, lastname=lastname, picture_link=False)
                else:
                    new_writer = Writer(firstname=firstname, lastname=lastname, picture_link=True)
                db.session.add(new_writer)
                db.session.commit()
                if not file.filename == '':
                    file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'writer_pfps', filename + '.' + file_extention))
                flash('Writer added.', category='success')
                return redirect(request.url)
            
        elif form_name == 'add-article':
            if 'fileupload' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['fileupload']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file_extention = file.filename.split('.')[-1]
                try:
                    filename = str(Article.query.order_by(desc(Article.id)).first().id + 1)
                except:
                    filename = str(1)
            else:
                flash('Invalid file')
                return redirect(request.url)
                
            writerid = request.form.get('writerid')
            date = request.form.get('date')
            title = request.form.get('title')
            description = request.form.get('description')
            content = request.form.get('content')
            ytembed = request.form.get('ytembed')
            
            dsplit = date.split('-')
            if date != '':
                dtransformed = datetime(int(dsplit[0]),int(dsplit[1]),int(dsplit[2]))
            writer_check = Writer.query.filter_by(id=writerid).first()
            if not writer_check:
                flash('Writer does not exist.', category='error')
                return redirect(request.url)
            elif len(title) <= 7:
                flash('Enter a title with more then 7 characters.', category='error')
                return redirect(request.url)
            elif len(content) <= 50:
                flash('Content must be more then 50 characters long.', category='error')
                return redirect(request.url)
            else:
                if date == '':
                    new_article = Article(writer_id=writerid, title=title, description=description, content=content, youtube_embed_link=ytembed)
                    db.session.add(new_article)
                    db.session.commit()
                    file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', filename + '.' + file_extention))
                    flash('Article added.', category='success')
                    return redirect(request.url)
                elif dtransformed > datetime.now():
                    flash('Date cannot be in the future.', category='error')
                    return redirect(request.url)
                else:
                    new_article = Article(writer_id=writerid, date=dtransformed, title=title, description=description, content=content, youtube_embed_link=ytembed)
                    db.session.add(new_article)
                    db.session.commit()
                    file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', filename + '.' + file_extention))
                    flash('Article added.', category='success')
                    return redirect(request.url)
                
        elif form_name == 'remove-subscriber':
            subscriberid = request.form.get('subscriberid')
            subscriber_check = Subscription.query.filter_by(id=subscriberid).first()
            if not writer_check:
                flash('Subscriber does not exist.', category='error')
                return redirect(request.url)
            else:
                db.session.delete(subscriber_check)
                db.session.commit()
                flash('Subscriber has been deleted.')
                return redirect(request.url)
        
        elif form_name == 'remove-writer':
            writerid = request.form.get('writerid')
            writer_check = Writer.query.filter_by(id=writerid).first()
            if not writer_check:
                flash('Writer does not exist.', category='error')
                return redirect(request.url)
            else:
                article_check = Article.query.filter_by(writer_id=writerid)
                for article in article_check:
                    db.session.delete(article)
                db.session.delete(writer_check)
                db.session.commit()
                flash('Writer has been deleted.')
                return redirect(request.url)
        
        elif form_name == 'remove-article':
            articleid = request.form.get('articleid')
            article_check = Article.query.filter_by(id=articleid).first()
            if not article_check:
                flash('Article does not exist.', category='error')
                return redirect(request.url)
            else:
                db.session.delete(article_check)
                db.session.commit()
                flash('Article has been deleted.')
                return redirect(request.url)
                
                
        elif form_name == 'email_subscription':
            email = request.form.get('newsletter')
            email_exists_check = Subscription.query.filter_by(email=email).first()
            if email_exists_check:
                flash('Email Address Already Signed Up!', category='error')
                return redirect(request.url)
            else:
                if not fullmatch(EMAIL_REGEX, email):
                    flash('Enter a valid email address.', category='error')
                    return redirect(request.url)
                else:
                    new_subscriber = Subscription(email=email)
                    db.session.add(new_subscriber)
                    db.session.commit()
                    flash('Thanks for subscribing!', category='success')
                    return redirect(request.url)
    
    return render_template(
        './hidden/article-manager.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )
    
@views.route('/hidden/db-viewer', methods=['GET', 'POST']) #should be hidden
def articleDatabaseViewer():
    page_settings = {
        'cover_picture': False,
        'current_page': 0,
        'footer' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]
    
    newsletterForm()

    dbsubscribers = Subscription.query.all()
    dbwriters = Writer.query.all()
    dbarticles = Article.query.all()
    
    return render_template(
        './hidden/db-viewer.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        subscribers=dbsubscribers,
        writers=dbwriters,
        articles=dbarticles)