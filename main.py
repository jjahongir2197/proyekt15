from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import threading
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emailq.db'
db = SQLAlchemy(app)

email_queue = []

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    status = db.Column(db.String(50))

def process_emails():
    while email_queue:
        email = email_queue.pop(0)

        print(f"Sending email to {email}")

        time.sleep(2)

        log = EmailLog(
            email=email,
            status="sent"
        )

        db.session.add(log)
        db.session.commit()

def add_email(email):
    email_queue.append(email)

with app.app_context():
    db.create_all()

    add_email("ali@gmail.com")
    add_email("vali@gmail.com")

    t = threading.Thread(target=process_emails)
    t.start()
