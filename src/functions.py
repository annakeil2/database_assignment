from flask import Flask, render_template, request, redirect, url_for
import random, json, time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import models

def save_to_file(messages):
    with open("data/messagebank.json", "w") as f:
        f.write(json.dumps(messages))
        

def load_from_file():
    with open("data/messagebank.json", "r") as f:
        json_string = f.read()
        return json.loads(json_string)

    
    

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


def get_message_for_current_time(db: SQLAlchemy):
    slot = get_slot_for_current_time()
    
    messages = db.session.execute(db.select(models.Message).filter_by(slot=slot)).all()
    
    for i in range(len(messages) -1, -1, -1):
        message = messages[i]
        if message['slot'] == slot:
            return message
    # if we do not have a message for a slot, return the last message:    
    return messages[len(messages) -1]    
    

