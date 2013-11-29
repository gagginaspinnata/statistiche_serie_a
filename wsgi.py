#! /usr/bin/env python
#-*- coding: utf-8 -*-


from flask import Flask, Request, Response, json, render_template
from scraper import Scraper

application = app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/api/pareggi/serie_a')
def serie_a():
	scraper = Scraper()
	data = scraper.squadre_senza_pareggi()
	return json.dumps(data)


@app.route('/api/pareggi/premier')
def premier():
	scraper = Scraper('premier')
	data = scraper.squadre_senza_pareggi()
	return json.dumps(data)

@app.route('/api/pareggi/liga')
def liga():
    scraper = Scraper('liga')
    data = scraper.squadre_senza_pareggi()
    return json.dumps(data)

@app.route('/api/pareggi/bundes')
def bundes():
    scraper = Scraper('bundes')
    data = scraper.squadre_senza_pareggi()
    return json.dumps(data)

@app.route('/api/pareggi/legue1')
def legue1():
    scraper = Scraper('legue1')
    data = scraper.squadre_senza_pareggi()
    return json.dumps(data)

# @app.route('/template')
# def template():
# 	# scraper = Scraper()
# 	# data = scraper.squadre_senza_pareggi()
# 	return render_template('ciao.html')

if __name__ == '__main__':

	app.run(debug=True)
