import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import json
from datetime import datetime

app = Flask(
    __name__,
    root_path=".",
    template_folder='../html',
    static_url_path='',
    static_folder='../static'
    )

db = os.environ['DB_NAME']
host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + user + ":" + password + "@" + host + "/" + db


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)


class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    create_date: Mapped[datetime]
    message: Mapped[str] = mapped_column(db.String, nullable=False)
    slot: Mapped[int] = mapped_column(db.Integer)

    # Display the message when printed
    def __repr__(self):
        return f"<Message(id={self.id}, slot={self.slot}, message={self.message})>"


def save_to_file(messages):
    with open("../data/messagebank.json", "w") as f:
        f.write(json.dumps(messages))


def load_from_file():
    with open("../data/messagebank.json", "r") as f:
        json_string = f.read()
        return json.loads(json_string)


# Create messages from the messagebank.json
# Only run once
def populate_messages():
    with app.app_context():
        existing_messages = db.session.execute(
            db.select(Message)
              .limit(1)
              .order_by(Message.id.desc())
        ).scalar_one_or_none()
        
        if existing_messages is not None:
            print("Messages found. Not populating db")
            return
        
        old_messages = load_from_file()

        for i in range(len(old_messages) - 1, -1, -1):
            old_message = old_messages[i]
            message = Message(
                message=old_message['message'].replace("\n", ""),
                create_date=datetime.fromtimestamp(old_message['created_at']),
                slot=old_message['slot']
            )
            print("Adding message:", message)

            # Insert the message into the DB
            db.session.add(message)

        db.session.commit()

populate_messages()