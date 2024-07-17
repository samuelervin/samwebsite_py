import os
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mail import Mail, Message

app = Flask(__name__)

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
            return render_template('contact.html', data='disabled')

    return render_template('contact.html', data='enabled')

@app.route('/resume/')
def resume():
    return render_template('resume.html')   

if __name__ == '__main__':
    app.run(debug=True)
