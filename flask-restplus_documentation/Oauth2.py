import json
from apiclient.discovery import build_from_document, build
import httplib2
import random

from oauth2client.client import OAuth2WebServerFlow

from flask import Flask, render_template, session, request, redirect, url_for, abort

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

app = Flask(__name__)


@app.route('/login')
def login():
  flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:5000/oauth2callback',
    approval_prompt='force',
    access_type='offline')

  auth_uri = flow.step1_get_authorize_url()
  return redirect(auth_uri)

@app.route('/signout')
def signout():
  del session['credentials']
  session['message'] = "You have logged out"

  return redirect(url_for('index'))

@app.route('/oauth2callback')
def oauth2callback():
  code = request.args.get('code')
  if code:
    # exchange the authorization code for user credentials
    flow = OAuth2WebServerFlow(CLIENT_ID,
      CLIENT_SECRET,
      "https://www.googleapis.com/auth/calendar")
    flow.redirect_uri = request.base_url
    try:
      credentials = flow.step2_exchange(code)
    except Exception as e:
      print "Unable to get an access token because ", e.message

    # store these credentials for the current user in the session
    # This stores them in a cookie, which is insecure. Update this
    # with something better if you deploy to production land
    session['credentials'] = credentials

  return redirect(url_for('index'))

@app.route('/')
def index():
  credentials = session['credentials']
  if credentials == None:
    return redirect(url_for('login'))

  http = httplib2.Http()
  http = credentials.authorize(http)
  service = build("calendar", "v3", http=http)
  calendar_list = service.calendarList().list().execute()

  return render_template("index.html", calendar_list=calendar_list)

if __name__ == '__main__':
  app.secret_key = 'hello world'
app.run(host='0.0.0.0')