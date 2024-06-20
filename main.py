from flask import Flask, render_template, request, redirect, url_for
import requests
from pprint import pprint
import smtplib
from dotenv import load_dotenv
import os
import time

load_dotenv()
EMAIL_KEY = os.getenv("EMAILKEY")

app = Flask(__name__)
blog_json = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

def send_email(name, sender_email, phone_number, message):
    #send email
    my_email = "calixatexample@gmail.com"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.login(user=my_email, password=EMAIL_KEY )
        connection.sendmail(
            from_addr=my_email, 
            to_addrs="hindig8888@proton.me", 
            msg=f"Subject:Blog contact!\n\nFrom: {name}, {sender_email}, {phone_number}\n\n{message}"
            )

@app.route('/')
def home():
    return render_template("index.html", posts= blog_json)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/post/<blog_id>')
def post(blog_id):
    blog_index = int(blog_id)-1
    return render_template("post.html", article= blog_json[blog_index])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        message = request.form['text']

        try: 
            send_email(name=name, sender_email=email, phone_number=phone_number, message=message)
            alert = 'Email successfully send!'
            return render_template('email_status.html', message=alert)
            
        except Exception as e:
            alert = f'Could not send Email: {e}'
            return render_template('email_status.html', message=alert)
        
    
    else:
        return render_template("contact.html")




if __name__ == "__main__":
    app.run(debug=True)
