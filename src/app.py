from flask import Flask, render_template, request, redirect, url_for
import random, json, time
from datetime import datetime

MAX_MESSAGE_SLOT = 95
NUMBER_OF_HISTORY = 10

app = Flask(__name__, template_folder='../html', static_url_path='', static_folder='../static')

connection_string = 'mystrongPW26A!'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://app:mystrongPW26A!@localhost/database_assignment"

messages = [
    # { 'message': 'test message'}
]

def save_to_file(messages):
    with open("data/messagebank.json", "w") as f:
        f.write(json.dumps(messages))
        

def load_from_file():
    with open("data/messagebank.json", "r") as f:
        json_string = f.read()
        return json.loads(json_string)

# def save_to_database(message):
    
    

def get_last_ten():
    current_slot = get_slot_for_current_time()
    end_slot = current_slot - 1
    if end_slot == -1:
        end_slot = MAX_MESSAGE_SLOT
        
    start_slot = end_slot - NUMBER_OF_HISTORY 
    if start_slot < 0:
        start_slot = MAX_MESSAGE_SLOT + start_slot
    
    pos = start_slot   
    display_messages = []
    while len(display_messages) < 10:
        display_messages.append(messages[pos])
        pos = pos + 1
        if pos == MAX_MESSAGE_SLOT:
            pos = 0
    return display_messages 
    
                   

def get_next_slot(messages):
    last_message = messages and messages[-1] or 0
    if last_message:
        slot = last_message['slot']
        if slot == MAX_MESSAGE_SLOT:
            return 0
        
        return slot + 1
    else:
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


def get_message_for_current_time():
    slot = get_slot_for_current_time()
    for i in range(len(messages) -1, -1, -1):
        message = messages[i]
        if message['slot'] == slot:
            return message
    # if we do not have a message for a slot, return the last message:    
    return messages[len(messages) -1]    
    

messages = load_from_file()
# print('messages', messages)


@app.route('/')
def index():
    message = ''
    content = ''
    if messages:
        message = get_message_for_current_time()['message']
    else:
        content = "You haven't been sent any bottled messages yet. But you can be the first to send one!"

    return render_template('index.html', content=content, message=message)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    return render_template('submit.html')


@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('message')

    if content:
        messages.append({
            "message": content,
            "created_at": int(time.time()),
            'slot': get_next_slot(messages)
        })
        save_to_file(messages)

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
    print('reached')
    messages_to_display = get_last_ten()
    print(messages_to_display)
    return render_template('history.html', messages=messages_to_display)


if __name__ == '__main__':
    app.run(debug=True)