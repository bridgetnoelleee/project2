from helpers import functions
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

def login():
    """Logs the user in."""
    if g.user:
        return redirect(functions.url_for('/'))
    error = None
    if request.method == 'POST':
        user = functions.query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(functions.url_for('/'))
    return render_template('login.html', error=error)

def register():
    """Registers the user."""
    return render_template('register.html')

def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(functions.url_for('/public'))


