from flask import Blueprint, render_template, request, flash, redirect, current_app, abort          # imports basic flask modules
from .models import Article, Writer, Subscription, Event, Volunteer, EventComment                   # imports all database classes that'll be used to format entries
from sqlalchemy import desc                                                         # imports desc used for queries to sort in decending order
from . import db                                                                    # imports db from __init__.py
from datetime import datetime                                                       # import datetime to get the current date and time
from re import fullmatch                                                            # import fullmatch a regex function that will be used for verification
from os import path, remove                                                         # imports path to make os friendly paths, and remove to remove files like unused images for later
from PIL import Image                                                               # imports pillow's image method, used later to convert files to webp for better performance

views = Blueprint('views', __name__)                                                # sets views as the blueprint views and uses __name__ to know where it is defined all URLs associated with this blueprint will have its url_prefix prepended

EMAIL_REGEX = r'\b[\w\d.%+-]+@[A-Za-z\d]+(\.[A-Za-z]{2,}){1,2}\b'                   # creates a real string variable with a regex pattern for matching emails within, capitalized to remind other editors that it should be treated like a constant
POSTCODE_REGEX = r'\b[A-Za-z]{1,2}(\d{1,2}|\d[A-Za-z]) ?\d[A-Za-z]{2}\b'            # creates a real string variable with a regex pattern for matching postcodes within
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'ico'}                          # creates a set of file types allowed to be uploaded, sets are not organized nor can contain duplicates

def allowed_file(filename):                                                                         # creates a function with the file's name passed in
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS             # returns a True or False if the extention of the filename is within the ALLOWED_EXTENSIONS set

def subscribeForm():                                                                # creates a function called subscribeForm
    if request.method == 'POST':                                                    # checks if inforamtion passed though was though the POST method if so execute code within
        form_name = request.form['form-name']                                       # gets the form name and stores it, form-name is from the html form input preset from within the current html page
        if form_name == 'email_subscription':                                       # checks if the form name is email_subscription and if so execute code within
            email = request.form.get('email')                                       # creates the variable email and sets the value to what is in the html input with the name email
            email_exists_check = Subscription.query.filter_by(email=email).first()  # uses a query filter to get the first item with the same email
            if email_exists_check:                                                  # checks if the email is within the query if so execute the code below else dont 
                flash('Email Address Already Signed Up!', category='error')         # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                        # redirects the user to the current url, so if they reload or go back to that page they dont resubmit the same information
            else:                                                                   # else statement executed if all if and elif statements is not true
                if not fullmatch(EMAIL_REGEX, email):                               # checks if the email passed though does not comply with the preset EMAIL_REGEX with the re(gex) module, if not execute the code below
                    flash('Enter a valid email address.', category='error')         # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                    return redirect(request.url)                                    # redirects the user to the current url
                elif len(email) > 50:                                                               # checks if the length of email is shorter then 50 characters
                    flash('Enter a email address is with 50 or less characters.', category='error') # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                    return redirect(request.url)                                                    # redirects the user to the current url
                else:                                                               # else statement executed if all if and elif statements is not true
                    new_subscriber = Subscription(email=email)                      # creates the variable new_subscriber with the formatting of Subscription in models.py with email set as the previous email variable
                    db.session.add(new_subscriber)                                  # adds the new_subscriber to the sqlalchemy session
                    db.session.commit()                                             # commits all database changes
                    flash('Thanks for subscribing!', category='success')            # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it notifies the user of success
                    return redirect(request.url)                                    # redirects the user to the current url

@views.route('/errorpages/404', methods=['GET', 'POST'])            # a decorator that calls the funcation below when routed to /errorpages/404 from any html page, methods are used to denote what requests are allowed to be made, POST is need to post infomration and GET is needed to get that information, note if you are going to add pages that will be in a directory you must use just / at the start of the link in route, e.g. /<directory>/<file>.html
def error_404():
    page_settings = {                                               # creates a dictionary called page_settings
        'cover_picture': False,                                     # adds the cover_picture as a key and False as it's value to the dictionary, this means the cover photo will not appear within the html page
        'current_page': 0,                                          # adds the current_page as a key and 0 as it's value to the dictionary, this is only used to keep track of what navbar item to highlight keep it zero if it doesnt comply with certain nav item see the other views to find the schema, this variable's exact number is not needed but if not in use set to 0
        'footer' : True,                                            # adds the footer as a key and True as it's value to the dictionary, this means the footer will appear on the html page 
        'negate_sidebar' : False,                                   # adds the negate sidebar as a key and True as it's value to the dictionary
        'sidebar_segments':0                                        # adds the sidebar_segments as a key and 0 as it's value to the dictionary, this will divvy up the side navbar into 0, 1 or 2 segments above 2 segments will just segment twice
        }                                                           # closes the dictionary

    subscribeForm()                # executes the subscribeForm function

    return render_template(                                         # returns render_template, this function means it'll render a html file for the user to see when this function is called, note if you are going to add pages that will be in a directory you must use a ./ at the start of the link in render template here, e.g. ./<directory>/<file>.html
        './errorpages/404.html',                                    # passes through the relative path of the page it'll send the user to, here it is the /errorpages/404 page, note flask's current directory will be templates when routing! when referencing assets in html the then current directory will be website, but please only store assets in static
        cover_picture=page_settings['cover_picture'],               # creates a variable called cover_picture with the value within page_settings' cover_picture key, the passes it though to be used within the html file
        current_page_num=page_settings['current_page'],             # creates a variable called current_page_num with the value within page_settings' current_page key
        footer=page_settings['footer'],                             # creates a variable called footer with the value within page_settings' footer key
        sidebar_segments=page_settings['sidebar_segments']          # creates a variable called sidebar_segments with the value within page_settings' sidebar_segments key
        )                                                           # ends render_template function

@views.route('/', methods=['GET', 'POST'])                          # a decorator that calls the funcation below when routed to / from any html page, methods are used to denote what requests are allowed to be made, POST is need to post infomration and GET is needed to get that information
def home():
    page_settings = {                                               # creates a dictionary called page_settings
        'cover_picture': True,                                      # adds the cover_picture as a key and False as it's value to the dictionary, this means the cover photo will appear within the html page, make sure to add the appropriate blocks to add the title and image link within the html pages
        'current_page': 1,                                          # adds the current_page as a key and 0 as it's value to the dictionary
        'footer' : True,                                            # adds the footer as a key and True as it's value to the dictionary
        'negate_sidebar' : False,                                   # adds the negate sidebar as a key and True as it's value to the dictionary
        'sidebar_segments':1 #maximum 2                             # adds the sidebar_segments as a key and 2 as it's value to the dictionary
        }                                                           # closes the dictionary
    sidebar_links = [                                               # creates a list called sidebar_links
        '/'                                                         # adds # to the list
    ]                                                               # closes the list

    subscribeForm()                # executes the subscribeForm function

    dbarticles = Article.query.order_by(desc(Article.id)).limit(3).all()            # uses a query filter to get items from the Articles database and sorts them by decending id value, and limits the query to 3 rows

    return render_template(                                         # returns render_template, this function means it'll render a html file for the user to see when this function is called
        './home.html',                                              # passes through the relative path of the page it'll send the user to, here it is the /home page
        cover_picture=page_settings['cover_picture'],               # creates a variable called cover_picture with the value within page_settings' cover_picture key, the passes it though to be used within the html file
        current_page_num=page_settings['current_page'],             # creates a variable called current_page_num with the value within page_settings' current_page key
        footer=page_settings['footer'],                             # creates a variable called footer with the value within page_settings' footer key
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links,                                # creates a variable called sidebar_links with the list of sidebar_links
        sidebar_segments=page_settings['sidebar_segments'],         # creates a variable called sidebar_segments with the value within page_settings' sidebar_segments key
        articles=dbarticles                                         # creates a variable called articles that passes though dbarticles, the article query
        )                                                           # ends render_template function

@views.route('/articles/articles/<int:pg>', methods=['GET', 'POST'])                # a decorator that calls the funcation below when routed to /articles/articles/<insert_integer_number> from any html page, <int:pg> acts like a variable that will be used to check for the page number, any number can be inserted so long as its an integer, a number must be inserted else it will 404
def articles(pg):                                                   # creates a function called articles but also passes though the value of <int:pg> to be used later
    page_settings = {                                               # creates a dictionary called page_settings
        'cover_picture': True,                                      # adds the cover_picture as a key and False as it's value to the dictionary
        'current_page': 2,                                          # adds the current_page as a key and 0 as it's value to the dictionary
        'footer' : True,                                            # adds the footer as a key and True as it's value to the dictionary
        'negate_sidebar' : False,                                   # adds the negate sidebar as a key and True as it's value to the dictionary
        'sidebar_segments':1 #maximum 2                             # adds the sidebar_segments as a key and 2 as it's value to the dictionary
        }                                                           # closes the dictionary
    sidebar_links = [                                               # creates a list called sidebar_links
        '/articles/articles/1'                                      # adds /articles/articles/1 to the list
    ]                                                               # closes the list

    subscribeForm()                # executes the subscribeForm function

    dbarticles = Article.query.order_by(desc(Article.id)).limit(50).all()           # uses a query filter to get items from the Articles database and sorts them by decending id value, and limits the query to 50 rows, this query will be used to show article items / to pass though a query of the database to the html page
    
    dbarticledivision = (-(-len(dbarticles)//5))                    # creates a variable called dbarticledivision which gets the length of dbarticles and integer divides it by five while rounding it up

    return render_template(                                         # returns render_template, this function means it'll render a html file for the user to see when this function is called
        './articles/articles.html',                                                 # passes through the relative path of the page it'll send the user to, here it is /articles/articles page
        cover_picture=page_settings['cover_picture'],               # creates a variable called cover_picture with the value within page_settings' cover_picture key, the passes it though to be used within the html file
        current_page_num=page_settings['current_page'],             # creates a variable called current_page_num with the value within page_settings' current_page key
        footer=page_settings['footer'],                             # creates a variable called footer with the value within page_settings' footer key
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links,                                # creates a variable called sidebar_links with the list of sidebar_links
        sidebar_segments=page_settings['sidebar_segments'],         # creates a variable called sidebar_segments with the value within page_settings' sidebar_segments key
        articles=dbarticles,                                        # creates a variable called articles with the value of dbarticles, the query made before
        max_pages=dbarticledivision,                                # creates a variable called max_pages with the value of dbarticledivision
        article_page=pg                                             # creates a variable called article_page with the value of pg, the passed though value from the url
        )                                                           # ends render_template function

@views.route('/articles/article-view/<string:articletitle>', methods=['GET', 'POST'])               # a decorator that calls the funcation below when routed to /articles/articles/<insert_string> from any html page, <string:articletitle> acts like a variable that will be used to check for the article, it will 404 if an improper title is inserted
def articleView(articletitle):                                                                      # creates a function called articles but also passes though the value of <string:articletitle> to be used later
    page_settings = {                                               # creates a dictionary called page_settings
        'cover_picture': True,                                      # adds the cover_picture as a key and False as it's value to the dictionary
        'current_page': 2,                                          # adds the current_page as a key and 0 as it's value to the dictionary
        'footer' : True,                                            # adds the footer as a key and True as it's value to the dictionary
        'negate_sidebar' : False,                                   # adds the negate sidebar as a key and True as it's value to the dictionary
        'sidebar_segments':1 #maximum 2                             # adds the sidebar_segments as a key and 2 as it's value to the dictionary
        }                                                           # closes the dictionary
    sidebar_links = [                                               # creates a list called sidebar_links
        '/articles/articles/1'                                      # adds /articles/articles/1 to the list
    ]                                                               # closes the list

    subscribeForm()                # executes the subscribeForm function

    articletitle = articletitle.replace('-',' ')

    dbarticle = Article.query.filter_by(title=articletitle).first() # uses a query filter to the article from the Articles database, this query will be used to show article items / to pass though a query of the article to the html page

    if not dbarticle:                                               # this is used to check if the article doesnt exists
        abort(404)                                                  # this is used to raise a 404 if the article doesnt exist

    dbwriter = Writer.query.filter_by(id=dbarticle.writer_id).first()               # uses a query filter to get the article's writer's information
        
    max_article = Article.query.order_by(desc(Article.id)).first().id               # uses a query filter to get items from the Articles database and sorts them by decending id value, and limits the query to 50 rows, this query will be used to show article items / to pass though a query of the database to the html page

    return render_template(                                         # returns render_template, this function means it'll render a html file for the user to see when this function is called
        './articles/article-view.html',                             # passes through the relative path of the page it'll send the user to, here it is /articles/articles page
        cover_picture=page_settings['cover_picture'],               # creates a variable called cover_picture with the value within page_settings' cover_picture key, the passes it though to be used within the html file
        current_page_num=page_settings['current_page'],             # creates a variable called current_page_num with the value within page_settings' current_page key
        footer=page_settings['footer'],                             # creates a variable called footer with the value within page_settings' footer key
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links,                                # creates a variable called sidebar_links with the list of sidebar_links
        sidebar_segments=page_settings['sidebar_segments'],         # creates a variable called sidebar_segments with the value within page_settings' sidebar_segments key
        max_article=max_article,                                    # creates a variable called articles with the value of dbarticles, the query made before
        article=dbarticle,                                          # creates a variable called articles with the value of dbarticles, the query made before
        writer=dbwriter                                             # creates a variable called articles with the value of dbarticles, the query made before
        )                                                           # ends render_template function

@views.route('/events/events-gridview/<int:pg>', methods=['GET', 'POST'])           # in the link /events/events-gridview/<int:pg>, <int:pg> acts like a variable that can be manually inserted and will be used to check for the page number, any number can be inserted so long as its an integer
def eventsGridview(pg):                                                             # passes though the value of <int:pg> to be used later
    page_settings = {
        'cover_picture': True,
        'current_page': 3,
        'footer' : True,
        'negate_sidebar' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/events/events-mapview',                                   # adds /events/events-mapview to the list, a different page link that will be used within the html
        '#'
    ]

    subscribeForm()                # executes the subscribeForm function
    
    dbevents = Event.query.order_by(desc(Event.id)).limit(50).all() # uses a query filter to get items from the Event database and sorts them by decending id value, and limits the query to 50 rows
    
    dbeventdivision = (-(-len(dbevents)//5))                        # creates a variable called dbarticledivision which gets the length of dbarticles and integer divides it by five while rounding it up
    
    return render_template(                                         # returns render_template, this function means it'll render a html file for the user to see when this function is called
        './events/events-gridview.html', 
        cover_picture=page_settings['cover_picture'],               # creates a variable called cover_picture with the value within page_settings' cover_picture key, the passes it though to be used within the html file
        current_page_num=page_settings['current_page'],             # creates a variable called current_page_num with the value within page_settings' current_page key
        footer=page_settings['footer'],                             # creates a variable called footer with the value within page_settings' footer key
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links,                                # creates a variable called sidebar_links with the list of sidebar_links
        sidebar_segments=page_settings['sidebar_segments'],         # creates a variable called sidebar_segments with the value within page_settings' sidebar_segments key
        events=dbevents,                                            # creates a variable called events with the value of dbevents
        max_pages=dbeventdivision,                                  # creates a variable called max_pages with the value of dbeventdivision
        event_page=pg                                               # creates a variable called event_page with the value of pg
        )                                                           # ends render_template function

@views.route('/events/events-mapview')
def eventsMapview():
    page_settings = {
        'cover_picture': False,
        'current_page': 3,
        'footer' : False,                                           # adds the footer as a key and False as it's value to the dictionary, this means the footer will not appear on the html page 
        'negate_sidebar' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '/events/events-gridview/1'                                 # adds /events/events-gridview to the list
    ]

    return render_template(
        './events/events-mapview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/events/event-view/<string:eventtitle>', methods=['GET', 'POST'])         # in the link /events/event-view/<string:eventtitle>, <string:eventtitle> acts like a variable that can be manually inserted and will be used to check for the page number, any string can be inserted
def eventView(eventtitle):                                                              # passes though the value of <string:eventtitle> to be used later
    page_settings = {
        'cover_picture': True,
        'current_page': 3,
        'footer' : True,
        'negate_sidebar' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/events/events-mapview',                                   # adds /events/events-mapview to the list, a different page link that will be used within the html
        '/events/events-gridview/1'
    ]

    subscribeForm()                # executes the subscribeForm function

    eventtitle = eventtitle.replace('-',' ').replace('?',r'%3F')

    dbevent = Event.query.filter_by(name=eventtitle).first()        # uses a query filter to the article from the Event database, this query will be used to show event items / to pass though a query of the event to the html page

    if not dbevent:                                                 # this is used to check if the article doesnt exists
        abort(404)                                                  # this is used to raise a 404 if the article doesnt exist

    dbcomments = EventComment.query.filter_by(event_id=dbevent.id).limit(15).all()                       # uses a query filter to get items from the EventComment database and sorts them by decending id value, and limits the query to 15 rows

    max_event = Event.query.order_by(desc(Event.id)).first().id     # uses a query filter to get items from the Articles database and sorts them by decending id value, and limits the query to 50 rows, this query will be used to show article items / to pass though a query of the database to the html page

    if request.method == 'POST':                                    # checks if inforamtion passed though was though the POST method if so execute code within

        form_name = request.form['form-name']                       # gets the form name and stores it, form-name is from the html form input preset from within the current html page
        if form_name == 'add-comment':                              # checks if the form name is email_subscription and if so execute code within

            username = request.form.get('username')                 # creates a variable called firstname then stores the request of the data inputted from the form input tag with the name of firstname
            content = request.form.get('comment')                   # creates a variable called lastname then stores the request of the data inputted from the form input tag with the name of lastname

            if len(username) < 1:                                                               # if statment if the if statement was false that gets the length of the username and checks if its smaller then 0 characters if so execute code below
                flash('Enter a username is with 1 or more characters.', category='error')       # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(username) > 100:                                                           # an else if statment if the if statement was false that gets the length of the username and checks if its larger then 100 characters if so execute code below
                flash('Enter a username is with 100 or less characters.', category='error')     # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(content) < 25:                                                             # an else if statment if the if statement was false that gets the length of the content and checks if its smaller then 25 characters if so execute code below
                flash('Content must be 25 or more characters long.', category='error')          # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(content) > 512:                                                            # an else if statment if the if statement was false that gets the length of the content and checks if its smaller then 25 characters if so execute code below
                flash('Content must be 512 or less characters long.', category='error')         # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            else:
                new_comment = EventComment(username=username, content=content, event_id=dbevent.id)
                db.session.add(new_comment)
                db.session.commit()
                flash('Comment added.', category='success')
                return redirect(request.url)

    return render_template(                                         # returns render_template, this function means it'll render a html file for the user to see when this function is called
        './events/event-view.html',                                 # passes through the relative path of the page it'll send the user to, here it is /articles/articles page
        cover_picture=page_settings['cover_picture'],               # creates a variable called cover_picture with the value within page_settings' cover_picture key, the passes it though to be used within the html file
        current_page_num=page_settings['current_page'],             # creates a variable called current_page_num with the value within page_settings' current_page key
        footer=page_settings['footer'],                             # creates a variable called footer with the value within page_settings' footer key
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links,                                # creates a variable called sidebar_links with the list of sidebar_links
        sidebar_segments=page_settings['sidebar_segments'],         # creates a variable called sidebar_segments with the value within page_settings' sidebar_segments key
        max_event=max_event,                                        # creates a variable called articles with the value of dbarticles, the query made before
        event=dbevent,                                              # creates a variable called articles with the value of dbarticles, the query made before
        comments=dbcomments                                         # creates a variable called comments with the value of dbcomments, the query made before
        )                                                           # ends render_template function


@views.route('/volunteer/volunteer-gridview/<int:pg>', methods=['GET', 'POST'])     # in the link /volunteer/volunteer-gridview/<int:pg>, <int:pg> acts like a variable that can be manually inserted and will be used to check for the page number, any number can be inserted so long as its an integer
def volunteerGridview(pg):                                                          # passes though the value of <int:pg> to be used later
    page_settings = {
        'cover_picture': True,
        'current_page': 4,
        'footer' : True,
        'negate_sidebar' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/volunteer/volunteer-mapview',                             # adds /volunteer/volunteer-mapview to the list
        '/volunteer/volunteer-gridview/1'
    ]

    subscribeForm()                # executes the subscribeForm function

    dbvolunteers = Volunteer.query.order_by(desc(Volunteer.id)).limit(50).all()     # uses a query filter to get items from the Volunteer database and sorts them by decending id value, and limits the query to 50 rows
    
    dbvolunteersdivision = (-(-len(dbvolunteers)//5))                               # creates a variable called dbvolunteersdivision which gets the length of dbvolunteers and integer divides it by five while rounding it up

    return render_template(
        './volunteer/volunteer-gridview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        volunteers=dbvolunteers,                                    # creates a variable called events with the value of dbevents
        max_pages=dbvolunteersdivision,                             # creates a variable called max_pages with the value of dbeventdivision
        volunteer_page=pg                                           # creates a variable called event_page with the value of pg
    )
    
@views.route('/volunteer/volunteer-mapview', methods=['GET', 'POST'])
def volunteerMapview():
    page_settings = {
        'cover_picture': False,
        'current_page': 4,
        'footer' : False,
        'negate_sidebar' : True,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '#',
        '/volunteer/volunteer-gridview/1'
    ]

    subscribeForm()                # executes the subscribeForm function

    return render_template(
        './volunteer/volunteer-mapview.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
    )

@views.route('/support/support-home', methods=['GET', 'POST'])
def support():
    page_settings = {
        'cover_picture': True,
        'current_page': 5,
        'footer' : True 
        }

    subscribeForm()                # executes the subscribeForm function

    return render_template(
        './support/support-home.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        )

@views.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    page_settings = {
        'cover_picture': True,
        'current_page': 6,
        'footer' : True,
        'negate_sidebar' : False,
        'sidebar_segments':1 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]

    subscribeForm()                # executes the subscribeForm function

    return render_template(
        './aboutus.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/hidden/db-manager', methods=['GET', 'POST'])         # should NOT be be linked whatsoever to the post production website AND THIS LINE SHOULD BE REMOVED, use this code as an example of how python flask works with forms
def articleManager():
    page_settings = {
        'cover_picture': False,
        'current_page': 0,
        'footer' : True,
        'negate_sidebar' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/',
        '/hidden/db-viewer'
    ]

    subscribeForm()                # executes the subscribeForm function
    
    if request.method == 'POST':                                    # checks if inforamtion passed though was though the POST method if so execute code within

        form_name = request.form['form-name']                       # gets the form name and stores it, form-name is from the html form input preset from within the current html page
        if form_name == 'add-writer':                               # checks if the form name is email_subscription and if so execute code within

            firstname = request.form.get('firstname')               # creates a variable called firstname then stores the request of the data inputted from the form input tag with the name of firstname
            lastname = request.form.get('lastname')                 # creates a variable called lastname then stores the request of the data inputted from the form input tag with the name of lastname
            twitterid = request.form.get('twitter')                 # creates a variable called twitterid then stores the request of the data inputted from the form input tag with the name of twitter
            instagramid = request.form.get('instagram')             # creates a variable called instagramid then stores the request of the data inputted from the form input tag with the name of instagram
            facebookid = request.form.get('facebook')               # creates a variable called facebookid then stores the request of the data inputted from the form input tag with the name of facebook

            if len(firstname) <= 0:                                                             # gets the length of the firstname and checks if its equal to or smaller then 0 if so execute code below
                flash('Enter a firstname is with 1 or more characters.', category='error')      # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(firstname) > 50:                                                           # an else if statment if the if statement was false that gets the length of the firstname and checks if its larger then 50 if so execute code below
                flash('Enter a firstname is with 50 or less characters.', category='error')     # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(lastname) <= 0:                                                            # an else if statment if the if statement was false that gets the length of the lastname and checks if its equal to or smaller then 0 if so execute code below
                flash('Enter a lastname is with 1 or more characters', category='error')        # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(lastname) > 50:                                                            # an else if statment if the if statement was false that gets the length of the lastname and checks if its larger then 50 if so execute code below
                flash('Enter a lastname is with 50 or less characters.', category='error')      # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(twitterid) > 50:                                                           # an else if statment if the if statement was false that gets the length of the lastname and checks if its larger then 50 if so execute code below
                flash('Enter a twitterid is with 50 or less characters.', category='error')     # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(instagramid) > 50:                                                         # an else if statment if the if statement was false that gets the length of the lastname and checks if its larger then 50 if so execute code below
                flash('Enter a instagramid is with 50 or less characters.', category='error')   # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(facebookid) > 50:                                                          # an else if statment if the if statement was false that gets the length of the lastname and checks if its larger then 50 if so execute code below
                flash('Enter a facebookid is with 50 or less characters.', category='error')    # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            else:                                                                                                                                               # if all if and elif statments were false executes the code below
                new_writer = Writer(firstname=firstname, lastname=lastname, twitterid=twitterid, instagramid=instagramid, facebookid=facebookid)                # creates variable called new_writer with the formatting of Writer in models.py with firstname arg set as the firstname variable, and lastname arg set as the lastname variable
                db.session.add(new_writer)                                                                                                                      # adds the new_writer to the sqlalchemy session
                db.session.commit()                                                             # commits all database changes
                
                flash('Writer added.', category='success')          # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it notifies the user of success
                return redirect(request.url)                        # redirects the user to the current url

        elif form_name == 'add-article':                            # checks if the form name is add-article and if so execute code within

            if 'fileupload' not in request.files:                   # checks if there is a file upload option within the form with the name of fileupload, request.files gets all files uploaded and the names form inputs their from and puts it into a dictionary
                flash('No file part', category='error')             # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user, although this is more of a site problem
                return redirect(request.url)                        # redirects the user to the current url

            file = request.files['fileupload']                      # creates a variable called file and stores all of the data of fileupload within

            if file.filename == '':                                 # checks if the original file.filename NOT filename has anything within, and if not if so execute code below
                flash('No selected file', category='error')         # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user, although this is more of a site problem
                return redirect(request.url)                        # redirects the user to the current url

            if file and allowed_file(file.filename):                # an if statement that firstly checks if file input from html exists, and then runs the file's name through the allowed_file function from earlier which checks if that file's extention is allowed to avoid some xss vulnerabilities
                try:                                                                            # trys the code below but if an exception is made by python it stops and executes the except code below
                    filename = str(Article.query.order_by(desc(Article.id)).first().id + 1)     # creates a variable called filename, and uses a query filter to get the first item from the Article database sorted them by decending id value and adds one, stringifies it, then stores it
                except:                                                                         # if the code within try exceptions the code below will run 
                    filename = str(1)                               # creates a variable called filename, not to be confused with file.filename, and stores 1 as a string
            else:                                                   # if the if statement fails the it will execute the code below
                flash('Invalid file', category='error')             # creates a flash, a message passed though flask that can be added into the html page  after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                        # redirects the user to the current url

            writerid = request.form.get('writerid')                 # creates a variable called writerid then stores the request of the data inputted from the form input tag with the name of writerid
            datetime_created = request.form.get('date')             # creates a variable called datetime_created then stores the request of the data inputted from the form input tag with the name of date
            title = request.form.get('title')                       # creates a variable called title then stores the request of the data inputted from the form input tag with the name of title
            description = request.form.get('description')           # creates a variable called description then stores the request of the data inputted from the form input tag with the name of description
            content = request.form.get('content')                   # creates a variable called content then stores the request of the data inputted from the form input tag with the name of content
            ytembed = request.form.get('ytembed')                   # creates a variable called ytembed then stores the request of the data inputted from the form input tag with the name of ytembed

            if '<embedyt>' in content and ytembed == '':
                flash('Enter a youtube video id for the embedyt tag.', category='error')        # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            
            elif '<embedyt>' not in content and ytembed != '':
                flash('Enter a embedyt tag for the youtube video embed.', category='error')     # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url

            if datetime_created != '':                              # if datetime_created has something within it then execute the code below
                dsplit = datetime_created.split('-')                                            # creates a variable called dsplit and gets datetime_created then splits it into a list of strings for each - within datetime_created 
                dtransformed = datetime(int(dsplit[0]),int(dsplit[1]),int(dsplit[2]))           # creates variable called dtransformed with the formatting of the datetime model from the datetime module with dsplit[0] set as the year, dsplit[1] set as the month, and dsplit[2] set as the day, integer-izing all of the variables in the process
            writer_check = Writer.query.filter_by(id=writerid).first()                          # creates variable called writer_check with the query result of the first matching writer with the inputted id from writerid

            if not writer_check:                                                                # if writer_check finds no writer then execute code below 
                flash('Writer does not exist.', category='error')                               # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                                                    # redirects the user to the current url
            elif len(title) < 7:                                                                # checks if the title length is 7 or more characters long
                flash('Enter a title with 7 or more characters.', category='error') 
                return redirect(request.url)
            elif len(title) > 100:                                                              # checks if the title length is 100 or less characters long
                flash('Enter a title with 100 or less characters.', category='error') 
                return redirect(request.url)
            elif len(description) > 512:                                                        # checks if the title description is 246 or less characters long
                flash('Description must be 512 or less characters long.', category='error') 
                return redirect(request.url)
            elif len(content) < 50:                                                             # checks if the content length is 50 or more characters long
                flash('Content must be 50 or more characters long.', category='error')
                return redirect(request.url)
            elif len(content) > 5000:                                                           # checks if the content length is 5000 or less characters long
                flash('Content must be 5000 or less characters long.', category='error')
                return redirect(request.url)
            elif len(ytembed) > 50:                                                             # checks if the content length is 5000 or less characters long
                flash('Content must be 50 or less characters long.', category='error')
                return redirect(request.url)
            else:
                if datetime_created == '':                                                                                                                      # if a date_created wasnt present execute code below
                    new_article = Article(writer_id=writerid, title=title, description=description, content=content, youtube_embed_link=ytembed)                # creates variable called new_article with the formatting of Article in models.py with writer_id arg set as the writerid variable, title arg set as the title variable, description arg set as the description variable and so on
                else:
                    if dtransformed > datetime.now():                                           # checks if dtransformed is larger then the current date and time
                        flash('Date cannot be in the future.', category='error')
                        return redirect(request.url)
                    else:
                        new_article = Article(writer_id=writerid, datetime_posted=dtransformed, title=title, description=description, content=content, youtube_embed_link=ytembed)              # creates variable called new_article with the formatting of Article, here it also includes the datetime_published arg set as the dtransformed variable

                db.session.add(new_article)                                                                                                     # adds the new_article to the sqlalchemy session
                db.session.commit()                                                             # commits all database changes
                file = Image.open(file)
                file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', filename + '.webp'), format="webp")
                flash('Article added.', category='success')
                return redirect(request.url)

        elif form_name == 'add-event':                              # checks if the form name is add-event and if so execute code within

            if 'fileupload' not in request.files:                   # checks if there is a file upload option within the form with the name of fileupload, request.files gets all files uploaded and the names form inputs their from and puts it into a dictionary
                flash('No file part', category='error')             # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user, although this is more of a site problem
                return redirect(request.url)                        # redirects the user to the current url

            file = request.files['fileupload']                      # creates a variable called file and stores all of the data of fileupload within

            if file.filename == '':                                 # checks if the original file.filename NOT filename has anything within, and if not if so execute code below
                flash('No selected file', category='error')         # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user, although this is more of a site problem
                return redirect(request.url)                        # redirects the user to the current url

            if file and allowed_file(file.filename):                # an if statement that firstly checks if file input from html exists, and then runs the file's name through the allowed_file function from earlier which checks if that file's extention is allowed to avoid some xss vulnerabilities
                try:                                                                            # trys the code below but if an exception is made by python it stops and executes the except code below
                    filename = str(Event.query.order_by(desc(Event.id)).first().id + 1)         # creates a variable called filename, and uses a query filter to get the first item from the Article database sorted them by decending id value and adds one, stringifies it, then stores it
                except:                                                                         # if the code within try exceptions the code below will run 
                    filename = str(1)                               # creates a variable called filename, not to be confused with file.filename, and stores 1 as a string
            else:                                                   # if the if statement fails the it will execute the code below
                flash('Invalid file', category='error')             # creates a flash, a message passed though flask that can be added into the html page  after the it executes the return function to notify the user, here it warns the user
                return redirect(request.url)                        # redirects the user to the current url

            name = request.form.get('name')
            description = request.form.get('description')
            addr1 = request.form.get('addr1')
            addr2 = request.form.get('addr2')
            city = request.form.get('city')
            county = request.form.get('county')
            country = request.form.get('country')
            postcode = request.form.get('postcode').upper()         # creates a variable called postcode then gets the request of the data inputted from the form input tag with the name of postcode, capitalizes it, then stores it
            datestart = request.form.get('datestart')
            timestart = request.form.get('timestart')
            dateend = request.form.get('dateend')
            timeend = request.form.get('timeend')

            if datestart and timestart != '':                       # checks if both datestart and timestart holds something
                dsplit_start = datestart.split('-')                 # creates a variable called dsplit_start and gets datestart then splits it into a list of strings for each - within datestart
                tsplit_start = timestart.split(':')                                                                                                             # creates a variable called tsplit_start and gets timestart then splits it into a list of strings for each - within timestart
                dstransformed = datetime(int(dsplit_start[0]),int(dsplit_start[1]),int(dsplit_start[2]),int(tsplit_start[0]),int(tsplit_start[1]))              # creates variable called dstransformed with the formatting of the datetime model from the datetime module with dsplit_start[0] set as the year, dsplit_start[1] set as the month, dsplit_start[2] set as the day, tsplit_start[0] set as the hour, and tsplit_start[1] set as the minute, integer-izing all of the variables in the process
            else:
                flash('Enter a start date and time.', category='error')
                return redirect(request.url)

            if dateend and timeend != '':                           # checks if both datestart and timestart holds something
                dsplit_end = dateend.split('-')                     # creates a variable called dsplit_end and gets dateend then splits it into a list of strings for each - within dateend
                tsplit_end = timeend.split(':')                                                                                                                 # creates a variable called tsplit_end and gets timeend then splits it into a list of strings for each - within timeend
                detransformed = datetime(int(dsplit_end[0]),int(dsplit_end[1]),int(dsplit_end[2]),int(tsplit_end[0]),int(tsplit_end[1]))                        # creates variable called dstransformed with the formatting of the datetime model from the datetime module with dsplit_end[0] set as the year, dsplit_end[1] set as the month, dsplit_end[2] set as the day, tsplit_end[0] set as the hour, and tsplit_end[1] set as the minute, integer-izing all of the variables in the process
            else:
                flash('Enter a end date and time.', category='error')
                return redirect(request.url)
            
            if dstransformed > detransformed:                                                   # checks if dstransformed, aka the start date, is further in time then detransformed, the end date
                flash('Start date cannot be greater then end date.', category='error')
                return redirect(request.url)
            
            if len(name) < 5:                                                                   # checks if the length of name is less then 5 characters long
                flash('Enter a name with 5 or more characters.', category='error')
                return redirect(request.url)
            elif len(name) > 100:                                                               # checks if the length of name is more then 100 characters long
                flash('Enter a name with 100 or less characters.', category='error')
                return redirect(request.url)
            elif len(description) < 50:                                                         # checks if the length of description is less then 50 characters long
                flash('Description must be 50 or more characters long.', category='error')
                return redirect(request.url)
            elif len(description) > 1024:                                                       # checks if the length of description is more then 256 characters long
                flash('Description must be 1024 or less characters long.', category='error')
                return redirect(request.url)
            elif len(addr1) < 5:                                                                # checks if the length of addr1 is less then 5 characters long
                flash('Address 1 must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif len(addr1) > 256:                                                              # checks if the length of addr1 is more then 256 characters long
                flash('Address 1 must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif len(addr2) > 256:                                                              # checks if the length of addr2 is more then 256 characters long
                flash('Address 2 must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif len(city) < 3:                                                                 # checks if the length of city is 3 or less characters long
                flash('City must be 3 or more characters long.', category='error')
                return redirect(request.url)
            elif len(city) > 256:                                                               # checks if the length of city is more then 256 characters long
                flash('City must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif len(country) < 5:                                                              # checks if the length of country is 5 or less characters long
                flash('Country must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif len(country) > 256:                                                            # checks if the length of country is more then 256 characters long
                flash('Country must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif not fullmatch(POSTCODE_REGEX, postcode):                                       # checks if the postcode passed though does not comply with the preset POSTCODE_REGEX with the re(gex) module, here i dont check for postcode's possible databse entry overflow as the regex should also cover that
                flash('Enter a valid postcode address.', category='error')
                return redirect(request.url)
            elif detransformed < datetime.now():                                                # checks if detransformed, aka the end date, is before the present date.
                flash('End date cannot be in the past.', category='error')
                return redirect(request.url)
            else:
                new_event = Event(name=name, description=description, address1=addr1, address2=addr2, city=city, county=county, country=country, postcode=postcode, datetime_end=detransformed, datetime_start=dstransformed)
                db.session.add(new_event)
                db.session.commit()
                file = Image.open(file)                                                                                         # overwrites the file variable and uses pillow to open the image and saves it
                file.save(path.join(current_app.config['UPLOAD_FOLDER'], 'event_covers', filename + '.webp'), format="webp")    # saves the file to event_covers with the value of filename and .webp then pillow converts the file format to webp
                flash('Event added.', category='success')
                return redirect(request.url)

        elif form_name == 'add-volunteer':

            if 'fileupload' not in request.files:                   # checks if there is a file upload option within the form with the name of fileupload, request.files gets all files uploaded and the names form inputs their from and puts it into a dictionary
                flash('No file part', category='error')             # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user, although this is more of a site problem
                return redirect(request.url)                        # redirects the user to the current url

            file = request.files['fileupload']                      # creates a variable called file and stores all of the data of fileupload within

            if file.filename == '':                                 # checks if the original file.filename NOT filename has anything within, and if not if so execute code below
                flash('No selected file', category='error')         # creates a flash, a message passed though flask that can be added into the html page after the it executes the return function to notify the user, here it warns the user, although this is more of a site problem
                return redirect(request.url)                        # redirects the user to the current url

            if file and allowed_file(file.filename):                # an if statement that firstly checks if file input from html exists, and then runs the file's name through the allowed_file function from earlier which checks if that file's extention is allowed to avoid some xss vulnerabilities
                try:                                                                            # trys the code below but if an exception is made by python it stops and executes the except code below
                    filename = str(Volunteer.query.order_by(desc(Volunteer.id)).first().id + 1) # creates a variable called filename, and uses a query filter to get the first item from the Volunteer database sorted them by decending id value and adds one, stringifies it, then stores it
                except:
                    filename = str(1)                               # creates a variable called filename, not to be confused with file.filename, and stores 1 as a string
            else:                                                   # if the if statement fails the it will execute the code below
                flash('Invalid file')
                return redirect(request.url)

            name = request.form.get('name')
            description = request.form.get('description')
            addr1 = request.form.get('addr1')
            addr2 = request.form.get('addr2')
            city = request.form.get('city')
            county = request.form.get('county')
            country = request.form.get('country')
            postcode = request.form.get('postcode').upper()         # creates a variable called postcode then gets the request of the data inputted from the form input tag with the name of postcode, capitalizes it, then stores it
            datestart = request.form.get('datestart')
            timestart = request.form.get('timestart')
            dateend = request.form.get('dateend')
            timeend = request.form.get('timeend')
            
            if datestart and timestart != '':                       # checks if both datestart and timestart holds something
                dsplit_start = datestart.split('-')                 #creates a variable called dsplit_start and gets datestart then splits it into a list of strings for each - within datestart
                tsplit_start = timestart.split(':')                                                                                                             # creates a variable called tsplit_start and gets timestart then splits it into a list of strings for each - within timestart
                dstransformed = datetime(int(dsplit_start[0]),int(dsplit_start[1]),int(dsplit_start[2]),int(tsplit_start[0]),int(tsplit_start[1]))              # creates variable called dstransformed with the formatting of the datetime model from the datetime module with dsplit_start[0] set as the year, dsplit_start[1] set as the month, dsplit_start[2] set as the day, tsplit_start[0] set as the hour, and tsplit_start[1] set as the minute, integer-izing all of the variables in the process
            else:
                flash('Enter a start date and time.', category='error')
                return redirect(request.url)

            if dateend and timeend != '':                           # checks if both datestart and timestart holds something
                dsplit_end = dateend.split('-')                     # creates a variable called dsplit_end and gets dateend then splits it into a list of strings for each - within dateend
                tsplit_end = timeend.split(':')                                                                                                                 # creates a variable called tsplit_end and gets timeend then splits it into a list of strings for each - within timeend
                detransformed = datetime(int(dsplit_end[0]),int(dsplit_end[1]),int(dsplit_end[2]),int(tsplit_end[0]),int(tsplit_end[1]))                        # creates variable called dstransformed with the formatting of the datetime model from the datetime module with dsplit_end[0] set as the year, dsplit_end[1] set as the month, dsplit_end[2] set as the day, tsplit_end[0] set as the hour, and tsplit_end[1] set as the minute, integer-izing all of the variables in the process
            else:
                flash('Enter a end date and time.', category='error')
                return redirect(request.url)

            if dstransformed > detransformed:                                                   # checks if dstransformed, aka the start date, is further in time then detransformed, the end date
                flash('Start date cannot be greater then end date.', category='error')
                return redirect(request.url)

            if len(name) < 5:                                                                   # checks if the length of name is less then 5 characters long
                flash('Enter a name with 5 or more characters.', category='error')
                return redirect(request.url)
            elif len(name) > 100:                                                               # checks if the length of name is more then 100 characters long
                flash('Enter a name with 100 or less characters.', category='error')
                return redirect(request.url)
            elif len(description) < 50:                                                         # checks if the length of description is less then 50 characters long
                flash('Description must be 50 or more characters long.', category='error')
                return redirect(request.url)
            elif len(description) > 512:                                                        # checks if the length of description is more then 256 characters long
                flash('Description must be 512 or less characters long.', category='error')
                return redirect(request.url)
            elif len(addr1) < 5:                                                                # checks if the length of addr1 is less then 5 characters long
                flash('Address 1 must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif len(addr1) > 256:                                                              # checks if the length of addr1 is more then 256 characters long
                flash('Address 1 must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif len(addr2) > 256:                                                              # checks if the length of addr2 is more then 256 characters long
                flash('Address 2 must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif len(city) < 3:                                                                 # checks if the length of city is 3 or less characters long
                flash('City must be 3 or more characters long.', category='error')
                return redirect(request.url)
            elif len(city) > 256:                                                               # checks if the length of city is more then 256 characters long
                flash('City must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif len(country) < 5:                                                              # checks if the length of country is 5 or less characters long
                flash('Country must be 5 or more characters long.', category='error')
                return redirect(request.url)
            elif len(country) > 256:                                                            # checks if the length of country is more then 256 characters long
                flash('Country must be 256 or less characters long.', category='error')
                return redirect(request.url)
            elif not fullmatch(POSTCODE_REGEX, postcode):                                       # checks if the postcode passed though does not comply with the preset POSTCODE_REGEX with the re(gex) module, here i dont check for postcode's possible databse entry overflow as the regex should also cover that
                flash('Enter a valid postcode address.', category='error')
                return redirect(request.url)
            elif detransformed < datetime.now():                                                # checks if detransformed, aka the end date, is before the present date.
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
            subscriberemail = request.form.get('subscriberemail')                               # creates a variable called subscriberemail then stores the request of the data inputted from the form input tag with the name of subscriberemail
            subscriber_check = Subscription.query.filter_by(email=subscriberemail).first()      # creates a variable called subscriber_check then uses and stores a query filter to get the first item with the same email
            if not subscriber_check:                                                            # checks if the email is not within the query if so execute the code below 
                flash('Subscriber does not exist.', category='error')
                return redirect(request.url)
            else:
                db.session.delete(subscriber_check)                 # removes the subscriber_check from the database within the sqlalchemy session
                db.session.commit()                                 # commits all database changes
                flash('Subscriber has been deleted.')
                return redirect(request.url)

        elif form_name == 'remove-writer':
            writerid = request.form.get('writerid')                                             # creates a variable called writerid then stores the request of the data inputted from the form input tag with the name of writerid
            writer_check = Writer.query.filter_by(id=writerid).first()                          # creates a variable called writer_check then uses and stores a query filter to get the first item with the same email
            if not writer_check:
                flash('Writer does not exist.', category='error')
                return redirect(request.url)
            else:
                article_check = Article.query.filter_by(writer_id=writerid)                     # creates a variable called article_check then uses and stores a query filter to get all items with the same writer_id as writerid
                for article in article_check:                                                   # uses a for loop to execute code for each item within the article_check, if there is none it will skip over it
                    db.session.delete(article)
                    if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article.id) + '.webp')):                # checks if the image for the article cover exists 
                        remove(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article.id) + '.webp'))                     # if the image for the article cover then it will delete that image
                db.session.delete(writer_check)                                                                                                 # removes the writer_check from the database within the sqlalchemy session
                db.session.commit()                                                                                                             # commits all database changes
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
                if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article_check.id) + '.webp')):              # checks if the image for the article cover exists
                    remove(path.join(current_app.config['UPLOAD_FOLDER'], 'article_covers', str(article_check.id) + '.webp'))                   # if the image for the article cover then it will delete that image
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
            if not volunteer_check:
                flash('Volunteer does not exist.', category='error')
                return redirect(request.url)
            else:
                db.session.delete(volunteer_check)
                db.session.commit()
                if path.exists(path.join(current_app.config['UPLOAD_FOLDER'], 'volunteer_covers', str(volunteer_check.id) + '.webp')):
                    remove(path.join(current_app.config['UPLOAD_FOLDER'], 'volunteer_covers', str(volunteer_check.id) + '.webp'))
                flash('Volunteer has been deleted.')
                return redirect(request.url)

    return render_template(
        './hidden/db-manager.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments']
        )

@views.route('/hidden/db-viewer', methods=['GET', 'POST'])          # should NOT be be linked whatsoever to the post production website AND THIS LINE SHOULD BE REMOVED
def articleDatabaseViewer():
    page_settings = {
        'cover_picture': False,
        'current_page': 0,
        'footer' : True,
        'negate_sidebar' : False,
        'sidebar_segments':2 #maximum 2
        }
    sidebar_links = [
        '/',
        '#'
    ]

    subscribeForm()                # executes the subscribeForm function

    dbsubscribers = Subscription.query.all()                                    # uses a query filter to get all items from the Subscription database and sorts them by decending id value
    dbwriters = Writer.query.all()                                              # uses a query filter to get all items from the Writer database and sorts them by decending id value 
    dbarticles = Article.query.all()                                            # uses a query filter to get all items from the Article database and sorts them by decending id value
    dbevents = Event.query.all()                                                # uses a query filter to get all items from the Event database and sorts them by decending id value
    dbvolunteers = Volunteer.query.all()                                        # uses a query filter to get all items from the Volunteer database and sorts them by decending id value
    dbecomments = EventComment.query.all()                                      # uses a query filter to get all items from the EventComments database and sorts them by decending id value

    return render_template(
        './hidden/db-viewer.html', 
        cover_picture=page_settings['cover_picture'], 
        current_page_num=page_settings['current_page'], 
        footer=page_settings['footer'],
        negate_sidebar=page_settings['negate_sidebar'],             # creates a variable called negate_sidebar with the value within page_settings' negate_sidebar key
        sidebar_links=sidebar_links, 
        sidebar_segments=page_settings['sidebar_segments'],
        subscribers=dbsubscribers,                                              # creates a variable called subscribers with the value of dbsubscribers
        writers=dbwriters,                                                      # creates a variable called writers with the value of dbwriters
        articles=dbarticles,                                                    # creates a variable called articles with the value of dbarticles
        events=dbevents,                                                        # creates a variable called events with the value of dbevents
        volunteers=dbvolunteers,                                                # creates a variable called volunteers with the value of dbvolunteers
        comments=dbecomments                                                    # creates a variable called volunteers with the value of dbvolunteers
        )