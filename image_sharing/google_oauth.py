from image_sharing import app, session
from database_setup import User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response, render_template, flash, request
from flask import session as login_session

import httplib2
import json
import requests
import random
import string

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


#############################################
#               helper functions            #
#############################################


def get_user_id(email):
    """Returns user_id given email address."""

    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except AttributeError:
        return None


def create_user(login_session):
    """Uses login_session to add user to database."""

    new_user = User(name    =login_session['username'],
                    email   =login_session['email'],
                    picture =login_session['picture'])
    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


#############################################
#            OAuth for Google+              #
#############################################


@app.route('/login')
def show_login():
    """Page that displays 3rd party login options.

    Login page for anti-forgery state token.
    """

    state = ''.join(random.choice(
                    string.ascii_uppercase +
                    string.digits +
                    string.ascii_lowercase)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Page that connects user to Google's OAuth then redirects to home.

    Checks that the token sent by the client to the server matches
    the token server sent to client.
    """

    # check if the token the client sent matches token server sent to client:
    # if tokens don't match, notify user and abort
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # obtain one-time authorization code for server:
    code = request.data

    # exchange one-time code [authorization code] for credentials object
    # -- i.e. access code for server:
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check that the access token is valid:
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)

    # submit request, parse response:
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    # create JSON GET request that contains url & access token:
    result = json.loads(str_response)

    # if there was an error in the access token info, abort:
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # verify that the access token is used for the intended user:
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # verify access token is valid for this app: if client IDs do not match,
    # the app is trying to use an id that doesn't belong to it
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if user is already logged into system:
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # if everything checks out, store access token in session for later use:
    # ____________________________________________________________________________
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # use google+ api to get info about user:
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # store data fields into login_session:
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check if user exists, else make new user:
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    # create response for successful login:
    output = '<h1>Welcome, %s!</h1>' % login_session['username']
    output += (
        '<img src="%s" style = "width: 300px; height: 300px;border-radius:'
        '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
        % login_session['picture'])
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route("/gdisconnect/")
def gdisconnect():
    """Disconnect user from Google+ OAuth.

    Revoke user's token and reset login_session.
    """

    # only disconnect a connected user:
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # reset user's session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(
            json.dumps('User has been disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # return error:
        # if don't get 200, something went wrong (e.g. given token was invalid)
        response = make_response(
            json.dumps('Failed to revoke for given user.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
