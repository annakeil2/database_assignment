from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import random, json, time
from datetime import datetime
import functions

@app.route('/')
def index():
    message = ''
    content = ''
    if messages:
        message = functions.get_message_for_current_time()['message']
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
            'slot': functions.get_next_slot(messages)
        })
        functions.save_to_file(messages)

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
    messages_to_display = functions.get_last_ten()
    print(messages_to_display)
    return render_template('history.html', messages=messages_to_display)

