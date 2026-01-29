from flask import Flask, session, redirect, url_for, jsonify, render_template, request
import os
import random
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from threading import Thread
from requests_oauthlib import OAuth2Session
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask('', template_folder='web', static_folder='web/static')
app.secret_key = b"fgddfgfdgdfdfgdgfdfgdfgsdfgdfgdhfgnfgcv"
# OAuth2 must make use of HTTPS in production environment.


@app.route('/')
def home():
  return "Tapidy Bot is Online"

def run():
  app.run(
		host='0.0.0.0',
		port=8080
	)

def keep_alive():
	t = Thread(target=run)
	t.start()