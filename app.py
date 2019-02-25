from flask import Flask, request, redirect, url_for, render_template, jsonify, session
import jinja2
import csv
import random
from random import shuffle
from flask.ext.session import Session

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from wtforms import Form, BooleanField, TextField, validators

from twilio.rest import Client

account_sid = 'AC02fe3d3cf0a2a6fb1a12c767ccb213b0'
auth_token = '24910555d266e50eb3b9e83c59e79646'
client = Client(account_sid, auth_token)
    
TAROT_DECK_DICT = {}

with open("static/20190223-chees-pixel-tarot.tsv") as tsv:
	for line in csv.reader(tsv, dialect="excel-tab"):
		TAROT_DECK_DICT[line[0]] = line[1:]

class ReusableForm(Form):
	name = TextField('Name:', validators=[validators.required()])

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/cut_deck")
def cut_deck():
	return render_template("cut-deck.html")

@app.route("/final_reading", methods=['GET', 'POST'])
def final_five():

	form = ReusableForm(request.form)
	
	final_cards = random.sample(xrange(78),3)
	tarot_reading = []
	for card in final_cards:
		tarot_reading.append(TAROT_DECK_DICT[str(card)])

	tarot_reading_text = ''
	for card in tarot_reading[:2]:
		tarot_reading_text += card[1] +'; '   	
	tarot_reading_text += tarot_reading[2][1]

	if request.method == 'POST':
		number=''
		number=request.form['number']

		message = client.messages.create(body=tarot_reading_text, from_='4153001499', to=number)
		return redirect('/final_reading')

	else:
		return render_template("final-reading.html", tarot_reading=tarot_reading, form=form)

# @app.route("/handle_form", methods=['GET', 'POST'])
# def my_form_post():
#     text = request.form['number']
#     processed_text = text.upper()
    
#     tarot_reading = session.get('reading', None)

#     tarot_reading_text = ''
    
#     for card in tarot_reading[:2]:
#     	tarot_reading_text += card[1] +'; '   	
# 	tarot_reading_text += tarot_reading[2][1]
    	
#     message = client.messages.create(body=tarot_reading_text, from_='4153001499', to=text)

#     return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)	