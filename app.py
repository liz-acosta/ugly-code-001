from flask import Flask, request, redirect, url_for, render_template, jsonify
import jinja2
import csv
import random
from random import shuffle

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from wtforms import Form, BooleanField, TextField, validators

from twilio.rest import Client

account_sid = 'nah-uh'
auth_token = 'nope'
client = Client(account_sid, auth_token)
    

TAROT_DECK_DICT = {}

with open("static/20190223-chees-pixel-tarot.tsv") as tsv:
	for line in csv.reader(tsv, dialect="excel-tab"):
		TAROT_DECK_DICT[line[0]] = line[1:]

final_cards = random.sample(xrange(78),3)
tarot_reading = []
for card in final_cards:
	tarot_reading.append(TAROT_DECK_DICT[str(card)])

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/cut_deck")
def cut_deck():
	return render_template("cut-deck.html")

@app.route("/final_reading", methods=['GET', 'POST'])
def final_five():
	# text = request.form['number']

	# five_card_image = "static/53c0cce811d9a_thumb900.jpg"
	return render_template("final-reading.html", tarot_reading=tarot_reading)


    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #         form.username.data, form.remember_me.data))
    #     return redirect('/index')

@app.route("/handle_form", methods=['GET', 'POST'])
def my_form_post():
    text = request.form['number']
    print("*****", tarot_reading)
    processed_text = text.upper()
    tarot_reading_text = ''
    
    for card in tarot_reading:
    	tarot_reading_text += card[1] +'; '
    	
    message = client.messages.create(body=tarot_reading_text, from_='4153001499', to=text)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)	