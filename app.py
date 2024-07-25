import os
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mail import Mail, Message
from dotenv import load_dotenv, dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Item

app = Flask(__name__)

load_dotenv()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
# Use your actual Gmail address
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
# Use your generated App Password
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
secret_key = os.environ.get("SECRET_KEY")
app.config['SECRET_KEY'] = secret_key
# Get environment variables
TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

# construct special SQLAlchemy URL
#dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

#engine = create_engine(dbUrl, connect_args={'check_same_thread': False}, echo=True)

mail = Mail(app)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/home/')
def home():
    return main()


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        if not email:
            flash('An email is required!', 'error')
        elif not subject:
            flash('A Subject is required!','error')
        elif not message:
            flash('A message is required!', 'error')
        else:
            flash('Your message has been sent!', 'success')
            return render_template('contact.html', data='disabled', visibility="hidden" )

    return render_template('contact.html', data='enabled', visibility="hidden" )

@app.route('/resume/')
def resume():
    return render_template('resume.html', visibility="hidden")   

@app.route("/getdbitems/", methods=(["GET"]))
def get_db_items():
    session = Session(engine)

    try:    
        # get & print items
        stmt = select(Item)

        for item in session.scalars(stmt):
            print(item)
    except Exception as e:
        print(e)
        return "An error  with the request occurred", 404
   
if __name__ == '__main__':
    app.run(debug=True)



