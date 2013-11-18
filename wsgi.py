#! /usr/bin/env python
#-*- coding: utf-8 -*-


from flask import Flask, Request, Response, json, render_template
from scraper import Scraper

application = app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/api/pareggi')
def scraper():
	scraper = Scraper()
	data = scraper.squadre_senza_pareggi()
	return json.dumps(data)

# @app.route('/template')
# def template():
# 	# scraper = Scraper()
# 	# data = scraper.squadre_senza_pareggi()
# 	return render_template('ciao.html')

if __name__ == '__main__':

	app.run(debug=True)