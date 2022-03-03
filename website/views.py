from flask import Blueprint, render_template, request, flash, redirect, current_app
from .models import Article, Writer, Subscription, Event, Volunteer
from sqlalchemy import desc
from . import db
from datetime import datetime
from re import fullmatch
from os import path, remove
from PIL import Image

views = Blueprint('views', __name__)

EMAIL_REGEX = r'\b[\w\d.%+-]+@[A-Za-z\d]+(\.[A-Za-z]{2,}){1,2}\b'
POSTCODE_REGEX = r'\b[A-Za-z]{1,2}(\d{1,2}|\d[A-Za-z]) ?\d[A-Za-z]{2}\b'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def newsletterForm():
    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'email_subscription':
            email = request.form.get('email')
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
    
    dbarticles = Article.query.order_by(desc(Article.id)).limit(3).all()

    return render_template(
        './home.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        articles=dbarticles
        )

@views.route('/articles/<int:pg>', methods=['GET', 'POST'])
def articles(pg):
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

    dbarticles = Article.query.order_by(desc(Article.id)).limit(50).all()
    
    dbarticledivision = (-(-len(dbarticles)//5))

    return render_template(
        './articles.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        articles=dbarticles,
        max_pages=dbarticledivision,
        article_page=pg
        )

@views.route('/events/events-gridview/<int:pg>', methods=['GET', 'POST'])
def eventsGridview(pg):
    page_settings = {
        'cover_picture': True,
        'current_page': 3,
        'footer' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/events/events-mapview',
        '#'
    ]

    newsletterForm()
    
    dbevents = Event.query.order_by(desc(Event.id)).limit(50).all()
    
    dbeventdivision = (-(-len(dbevents)//5))
    
    return render_template(
        './events/events-gridview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        events=dbevents,
        max_pages=dbeventdivision,
        event_page=pg
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
        '#',
        '/events/events-gridview'
    ]

    return render_template(
        './events/events-mapview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/volunteer/volunteer-gridview/<int:pg>', methods=['GET', 'POST'])
def volunteerGridview(pg):
    page_settings = {
        'cover_picture': True,
        'current_page': 4,
        'footer' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/volunteer/volunteer-mapview',
        '#'
    ]

    newsletterForm()

    dbvolunteers = Volunteer.query.order_by(desc(Volunteer.id)).limit(50).all()
    
    dbvolunteersdivision = (-(-len(dbvolunteers)//5))

    return render_template(
        './volunteer/volunteer-gridview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        volunteers=dbvolunteers,
        max_pages=dbvolunteersdivision,
        volunteer_page=pg
    )
    
@views.route('/volunteer/volunteer-mapview', methods=['GET', 'POST'])
def volunteerMapview():
    page_settings = {
        'cover_picture': False,
        'current_page': 4,
        'footer' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '/volunteer/volunteer-gridview'
    ]

    newsletterForm()

    return render_template(
        './volunteer/volunteer-mapview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
    )

@views.route('/support/support-home', methods=['GET', 'POST'])
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
        './support/support-home.html', 
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

@views.route('hidden/db-manager', methods=['GET', 'POST']) #should be hidden
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
                    file = Image.open(file)
                    file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'writer_pfps', filename + '.webp'), format="webp")
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
                try:
                    filename = str(Article.query.order_by(desc(Article.id)).first().id + 1)
                except:
                    filename = str(1)
            else:
                flash('Invalid file')
                return redirect(request.url)

            writerid = request.form.get('writerid')
            datetime_created = request.form.get('date')
            title = request.form.get('title')
            description = request.form.get('description')
            content = request.form.get('content')
            ytembed = request.form.get('ytembed')

            dsplit = datetime_created.split('-')
            if datetime_created != '':
                dtransformed = datetime(int(dsplit[0]),int(dsplit[1]),int(dsplit[2]))
            writer_check = Writer.query.filter_by(id=writerid).first()
            if not writer_check:
                flash('Writer does not exist.', category='error')
                return redirect(request.url)
            elif len(title) < 7:
                flash('Enter a title with 7 or more characters.', category='error')
                return redirect(request.url)
            elif len(content) <= 50:
                flash('Content must be more then 50 characters long.', category='error')
                return redirect(request.url)
            else:
                if datetime_created == '':
                    new_article = Article(writer_id=writerid, title=title, description=description, content=content, youtube_embed_link=ytembed)
                    db.session.add(new_article)
                    db.session.commit()
                    file = Image.open(file)
                    file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', filename + '.webp'), format="webp")
                    flash('Article added.', category='success')
                    return redirect(request.url)
                elif dtransformed > datetime.now():
                    flash('Date cannot be in the future.', category='error')
                    return redirect(request.url)
                else:
                    new_article = Article(writer_id=writerid, date=dtransformed, title=title, description=description, content=content, youtube_embed_link=ytembed)
                    db.session.add(new_article)
                    db.session.commit()
                    file = Image.open(file)
                    file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', filename + '.webp'), format="webp")
                    flash('Article added.', category='success')
                    return redirect(request.url)
                
        elif form_name == 'add-event':
            if 'fileupload' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['fileupload']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    filename = str(Event.query.order_by(desc(Event.id)).first().id + 1)
                except:
                    filename = str(1)
            else:
                flash('Invalid file')
                return redirect(request.url)

            name = request.form.get('name')
            description = request.form.get('description')
            addr1 = request.form.get('addr1')
            addr2 = request.form.get('addr2')
            city = request.form.get('city')
            county = request.form.get('county')
            country = request.form.get('country')
            postcode = request.form.get('postcode').upper()
            datestart = request.form.get('datestart')
            timestart = request.form.get('timestart')
            dateend = request.form.get('dateend')
            timeend = request.form.get('timeend')
            
            if datestart and timestart != '':
                dsplit_start = datestart.split('-')
                tsplit_start = timestart.split(':')
                dstransformed = datetime(int(dsplit_start[0]),int(dsplit_start[1]),int(dsplit_start[2]),int(tsplit_start[0]),int(tsplit_start[1]))
            else:
                flash('Enter a start date and time.', category='error')
                return redirect(request.url)
            if dateend and timeend != '':
                dsplit_end = dateend.split('-')
                tsplit_end = timeend.split(':')
                detransformed = datetime(int(dsplit_end[0]),int(dsplit_end[1]),int(dsplit_end[2]),int(tsplit_end[0]),int(tsplit_end[1]))
            else:
                flash('Enter a end date and time.', category='error')
                return redirect(request.url)
            
            if dstransformed > detransformed:
                flash('Start date cannot be greater then end date.', category='error')
                return redirect(request.url)
            
            if len(name) <= 5:
                flash('Enter a name with more then 5 characters.', category='error')
                return redirect(request.url)
            elif len(description) <= 50:
                flash('Content must be more then 50 characters long.', category='error')
                return redirect(request.url)
            elif len(addr1) < 5:
                flash('Address 1 must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif len(city) < 3:
                flash('City must be 3 or more characters long.', category='error')
                return redirect(request.url)
            elif len(country) < 5:
                flash('Country must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif not fullmatch(POSTCODE_REGEX, postcode):
                flash('Enter a valid postcode address.', category='error')
                return redirect(request.url)
            elif detransformed < datetime.now():
                flash('End date cannot be in the past.', category='error')
                return redirect(request.url)
            else:
                new_event = Event(name=name, description=description, address1=addr1, address2=addr2, city=city, county=county, country=country, postcode=postcode, datetime_end=detransformed, datetime_start=dstransformed)
                db.session.add(new_event)
                db.session.commit()
                file = Image.open(file)
                file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'event_covers', filename + '.webp'), format="webp")
                flash('Event added.', category='success')
                return redirect(request.url)

        elif form_name == 'add-volunteer':
            if 'fileupload' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['fileupload']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    filename = str(Volunteer.query.order_by(desc(Volunteer.id)).first().id + 1)
                except:
                    filename = str(1)
            else:
                flash('Invalid file')
                return redirect(request.url)

            name = request.form.get('name')
            description = request.form.get('description')
            addr1 = request.form.get('addr1')
            addr2 = request.form.get('addr2')
            city = request.form.get('city')
            county = request.form.get('county')
            country = request.form.get('country')
            postcode = request.form.get('postcode').upper()
            datestart = request.form.get('datestart')
            timestart = request.form.get('timestart')
            dateend = request.form.get('dateend')
            timeend = request.form.get('timeend')
            
            if datestart and timestart != '':
                dsplit_start = datestart.split('-')
                tsplit_start = timestart.split(':')
                dstransformed = datetime(int(dsplit_start[0]),int(dsplit_start[1]),int(dsplit_start[2]),int(tsplit_start[0]),int(tsplit_start[1]))
            else:
                flash('Enter a start date and time.', category='error')
                return redirect(request.url)
            if dateend and timeend != '':
                dsplit_end = dateend.split('-')
                tsplit_end = timeend.split(':')
                detransformed = datetime(int(dsplit_end[0]),int(dsplit_end[1]),int(dsplit_end[2]),int(tsplit_end[0]),int(tsplit_end[1]))
            else:
                flash('Enter a end date and time.', category='error')
                return redirect(request.url)
            
            if dstransformed > detransformed:
                flash('Start date cannot be greater then end date.', category='error')
                return redirect(request.url)
            
            if len(name) <= 5:
                flash('Enter a name with more then 5 characters.', category='error')
                return redirect(request.url)
            elif len(description) <= 50:
                flash('Content must be more then 50 characters long.', category='error')
                return redirect(request.url)
            elif len(addr1) < 5:
                flash('Address 1 must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif len(city) < 3:
                flash('City must be 3 or more characters long.', category='error')
                return redirect(request.url)
            elif len(country) < 5:
                flash('Country must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif not fullmatch(POSTCODE_REGEX, postcode):
                flash('Enter a valid postcode address.', category='error')
                return redirect(request.url)
            elif detransformed < datetime.now():
                flash('End date cannot be in the past.', category='error')
                return redirect(request.url)
            else:
                new_volunteer = Volunteer(name=name, description=description, address1=addr1, address2=addr2, city=city, county=county, country=country, postcode=postcode, datetime_end=detransformed, datetime_start=dstransformed)
                db.session.add(new_volunteer)
                db.session.commit()
                file = Image.open(file)
                file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'volunteer_covers', filename + '.webp'), format="webp")
                flash('Volunteer added.', category='success')
                return redirect(request.url)

        elif form_name == 'remove-subscriber':
            subscriberid = request.form.get('subscriberid')
            subscriber_check = Subscription.query.filter_by(id=subscriberid).first()
            if not subscriber_check:
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
                    if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article.id) + '.webp')):
                        remove(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article.id) + '.webp'))
                db.session.delete(writer_check)
                db.session.commit()
                if writer_check.picture_link and path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'writer_pfps', str(writer_check.id) + '.webp')):
                    remove(path.join(current_app.config['UPLOAD_FOLDER'], 'writer_pfps', str(writer_check.id) + '.webp'))
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
                if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article_check.id) + '.webp')):
                    remove(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article_check.id) + '.webp'))
                flash('Article has been deleted.')
                return redirect(request.url)
            
        elif form_name == 'remove-event':
            eventid = request.form.get('eventid')
            event_check = Event.query.filter_by(id=eventid).first()
            if not event_check:
                flash('Event does not exist.', category='error')
                return redirect(request.url)
            else:
                db.session.delete(event_check)
                db.session.commit()
                if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'event_covers', str(event_check.id) + '.webp')):
                    remove(path.join(current_app.config['UPLOAD_FOLDER'], 'event_covers', str(event_check.id) + '.webp'))
                flash('Event has been deleted.')
                return redirect(request.url)

        elif form_name == 'remove-volunteer':
            volunteerid = request.form.get('volunteerid')
            volunteer_check = Volunteer.query.filter_by(id=volunteerid).first()
            if not event_check:
                flash('Volunteer does not exist.', category='error')
                return redirect(request.url)
            else:
                db.session.delete(volunteer_check)
                db.session.commit()
                if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'volunteer_covers', str(volunteer_check.id) + '.webp')):
                    remove(path.join(current_app.config['UPLOAD_FOLDER'], 'volunteer_covers', str(volunteer_check.id) + '.webp'))
                flash('Volunteer has been deleted.')
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
        './hidden/db-manager.html', 
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
    dbevents = Event.query.all()
    dbvolunteers = Volunteer.query.all()

    return render_template(
        './hidden/db-viewer.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        subscribers=dbsubscribers,
        writers=dbwriters,
        articles=dbarticles,
        events=dbevents,
        volunteers=dbvolunteers
        )