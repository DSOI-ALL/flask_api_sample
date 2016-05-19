#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests
from requests.auth import HTTPBasicAuth
from ConfigParser import ConfigParser
import os

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), './frontend_settings.cfg'))

app = Flask(__name__)

API_HOST = config.get('api', 'host')
API_PORT = config.get('api', 'port')
AUTH_TUPLE = (config.get('auth', 'service_username'), config.get('auth', 'service_password'))

@app.route("/")
def display_movies():
    r = requests.get('http://%s:%s/api/movies' %(API_HOST, API_PORT), auth=AUTH_TUPLE)
    movies = r.json()['movies']
    return render_template('home.html', movies=movies)


@app.route("/movies/<int:movie_id>")
def display_movie(movie_id):
    url = "http://%s:%s/api/movies/%s" %(API_HOST, API_PORT, str(movie_id))
    r = requests.get(url, auth=AUTH_TUPLE)
    movie = r.json()['movie']
    return render_template('movie.html', movie=movie)


if __name__ == "__main__":
    app.run(host=config.get('network', 'listen_host'), port=int(config.get('network', 'listen_port')), debug=config.get('runtime', 'debug'))
