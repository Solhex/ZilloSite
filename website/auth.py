from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Article, Writer
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


"""
picture_link = NULL
firstname = 'Cassis'
surname = 'Texic'

title = 'Lorem ipsum dolor sit'
description = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Adipiscing enim eu turpis egestas pretium aenean pharetra.'''

text = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Adipiscing enim eu turpis egestas pretium aenean pharetra. Donec et 
odio pellentesque diam volutpat commodo sed. Aliquet sagittis id consectetur 
purus ut faucibus pulvinar. Commodo sed egestas egestas fringilla phasellus 
faucibus scelerisque eleifend donec. Metus vulputate eu scelerisque felis 
imperdiet proin fermentum leo. Eros donec ac odio tempor orci dapibus 
ultrices in. Nulla facilisi morbi tempus iaculis urna id. Semper quis 
lectus nulla at volutpat. Vestibulum lectus mauris ultrices eros in cursus 
turpis massa. Platea dictumst quisque sagittis purus sit amet volutpat 
consequat mauris. Quisque id diam vel quam. Quisque non tellus orci ac auctor 
augue mauris augue neque. Rhoncus aenean vel elit scelerisque mauris pellentesque. 
Adipiscing elit pellentesque habitant morbi tristique senectus.\n
Egestas maecenas pharetra convallis posuere morbi leo urna molestie. 
Tellus rutrum tellus pellentesque eu. Purus sit amet luctus venenatis lectus 
magna. Id eu nisl nunc mi. Velit laoreet id donec ultrices tincidunt arcu non 
sodales. Fringilla urna porttitor rhoncus dolor purus non enim praesent 
elementum. Sed vulputate mi sit amet mauris. Porta lorem mollis aliquam ut 
porttitor leo a. Porttitor rhoncus dolor purus non enim praesent elementum. 
Vitae tempus quam pellentesque nec nam aliquam. Et tortor consequat id porta. 
Augue lacus viverra vitae congue eu consequat. Faucibus pulvinar elementum 
integer enim. Consectetur adipiscing elit duis tristique sollicitudin. 
Consectetur lorem donec massa sapien faucibus et molestie. Eget lorem dolor 
sed viverra.'''

youtube_embed_link = NULL
writer_id = 1

"""