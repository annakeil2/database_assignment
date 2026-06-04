from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import json
from datetime import datetime

MAX_MESSAGE_SLOT = 95
NUMBER_OF_HISTORY = 10

app = Flask(__name__, root_path=".", template_folder='../html', static_url_path='', static_folder='../static')

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://app:mystrongPW26A!@localhost/database_assignment"

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
        old_messages = load_from_file()
        print('old_messages', old_messages)

        for i in range(len(old_messages) - 1, -1, -1):
            old_message = old_messages[i]
            message = Message(
                message=old_message['message'],
                create_date=datetime.fromtimestamp(old_message['created_at']),
                slot=old_message['slot']
            )
            print(message)

            # Insert the message into the DB
            db.session.add(message)

        db.session.commit()

    
# Get the last ten messages regardless of slot
def get_last_messages(n = 10):
    return db.session.execute(
        db.select(Message)
        .limit(n)
        .order_by(Message.id.desc())
    ).scalars()


# Get the last messages regardless of slot
def get_last_message():
    return db.session.execute(
        db.select(Message)
        .limit(1)
        .order_by(Message.id.desc())
    ).scalar_one()


# Get the next slot for a message
# This is 1 greater than the last slot used between 0 and MAX_MESSAGE_SLOT
def get_next_slot():
    last_message = get_last_message()
    if last_message is not None:
        print('last message found', last_message)
        slot = last_message.slot
        if slot == MAX_MESSAGE_SLOT:
            return 0
        
        return slot + 1
    else:
        print('no last message found')
        return 0


# return a slot between 0 and 95 based on the 15 minute intervals of the day
def get_slot_for_current_time():
    hour = int(datetime.now().strftime('%H'))
    minute = int(datetime.now().strftime('%M'))
    slot = (hour * 4)
    if minute < 15:
        slot = slot
    elif minute < 30:
        slot = slot +1
    elif minute < 45:
        slot = slot + 2
    else:
        slot = slot + 3
    return slot


# Get the message for the current time
def get_message_for_current_time():
    slot = get_slot_for_current_time()

    # Get the latest message for the slot
    return db.session.execute(
        db.select(Message)
            .where(Message.slot == slot)
            .order_by(Message.id.desc())
            .limit(1)
    ).scalar()

@app.route('/')
def index():
    content = ''
    message = get_message_for_current_time()
    if message is None:
        # If we don't have a message for a time slot just display the last message
        message = get_last_message()
        if message is None:
            content = "You haven't been sent any bottled messages yet. But you can be the first to send one!"
            message = ''

    return render_template('index.html', content=content, message=message)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    return render_template('submit.html')


@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('message')

    if content:
        slot = get_next_slot()
        print("slot", slot)

        # Create a new message with the last slot + 1
        message = Message(message=content, create_date=datetime.now(), slot=slot)
        print(message)

        # Insert the message into the DB
        db.session.add(message)

        db.session.commit()

    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    name = request.form['name']
    return render_template('contact_result.html', name = name)

@app.route('/history')
def history():
    messages_to_display = get_last_messages(10)
    return render_template('history.html', messages=messages_to_display)


# Start the app
if __name__ == '__main__':
    app.run(debug=True)

# populate_messages()