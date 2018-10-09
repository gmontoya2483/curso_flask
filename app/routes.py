from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'gabriel'} # Faked user

    # Faked Posts
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Vienna'
        },
        {
            'author': {'username': 'Gsbriel'},
            'body': 'Beautiful day in Buenos Aires'
        },
        {
            'author': {'username': 'Sandrita'},
            'body': 'Beautiful day in China'
        }
    ]

    return render_template('index.html', user=user, title='Home', posts=posts)
