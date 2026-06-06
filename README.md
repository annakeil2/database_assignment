# Database Assignment

## Project Description
This application allows users to get inspired by others by receiving a bottled message every 15 minutes that was sent by another random other user. 

It is built on the idea of real life bottled message practices. The goal is to get inspired or motivated by someone else's message. 

The application consists of 5 pages. One where users receive a bottled messaged sent by another user every 15 minutes (including a timer), a 'Send' page where one can type up and send a message through a form for other users to be received, a 'History' page listing the last 10 submitted messages as a record, an simple 'About' page detailing the goal and mission of the application, as well as a 'Contact' page where users are invited to send the creators any feedback.

## Database Description
A table `messages` was created to hold the bottle messages. The table has an auto-incrementing primary key, a create_date timestamp, a text message field, and an integer slot.

The slot contains an integer referencing the 15-minute time slot during the day when it should display the message. The slot is calculated before inserting the message, and messages are selected based on the slot, from the database. 

I used SQLAlechemy to access the database from Python. I used a Message class to map Python values to the PostgreSQL database. I updated all the functions that were retrieving or storing messages and had them use the PostgreSQL database.

I added a script `populate_db.py` to write initial messaged to the database to enhance user experience on first deploy.

I deployed the PostgreSQL database to render.com alongside the Python project and I passed the database credentials into my app.py script using environmental variables.

## Fixes and Enhancements
I received valuable feedback on my last assignment in the course (Python assignment) and I made sure I took all the suggestions and feedback onboard. Among some other enhancements and fixes, I made sure to make the site more inclusive with adding better contrasting colours and font sizes, and a less distracting background. These changes greatly improved useability.

Based on the previous feedback, I also made sure to add multiple media queries to make the app work on all screensizes, again adding to the improved useability of the app.

As for the timer fix that was outlined in the feedback, previously the timer just counted down 15 minutes. I now made it count down to the _next_ 15th minute of the hour. 

I also made sure to validate all the python, html, and css code on trusted validator sites, as well as linters. The html and css pass validation fully and completely. However, the python code shows one single exeption in the Pep8: line 38 where Pep8 does not like the named argument following the property declaration. 

## Features

#### Feature 1: Receive a message from another user
This feature allows users receive messages submitted earlier by other users.

#### Feature 2: Timer for next message
A timer feature has been built in on the landing page so that users know when they are to receive the next bottled message from the messages that are queued up.

#### Feature 3: Send a new bottled message 
The message that is submitted through the form on the 'Send' page end up being added to the messagebank.json file in the data folder.

#### Feature 4: Contact form 
A contact form has been implemented encouraging users to leave feedback for the betterment of the application. The email address needs to adhere to the
email address format or else it does not go through. Once it is submitted, a thank you message is displayed containing the name of the user who just
submitted feedback to make it more personal.

#### Feature 5: History page
This feature displays the last 10 messages that were submitted by users. It can be used to peak interest and encourage other users to submit their messages, or serve as inspiration for them. 

## Design choices

#### Colours
I chose these colors for the project due to the fact that at the very start I chose my own photograph as the background, so I based all my decisions re
colours so that it matches the hue of the background photo. I kept good accessibility, good balance, and of course user engagement in mind. Pastel
colours nicely seem to match the background. 

#### Fonts/Typography
I chose these this font as I did not want to overcomplicate and make the visuals overly crowded and overwhelming as I chose a background photo already. My idea was to go with a simple font to minimise visual noise. 

#### Images/Graphics
The background image is my own and I decided to base all my styling decision on the hue of the image. The only other image is the bottle image on the
landing page which I chose as it conveys playfulness.

## Development Process

#### Project planning
At the outset I was certain that I will need to pages: one for receiving and one for submitting bottled messages. The additional 3 pages were developed
at a later stage following best practices I came across in other applications and websites. Throughout the design stage I needed to find the best way to
store and queue messages that were submitted by users that will eventually be sent to other users. I ended up implementing that feature, the most 
essential feature of the app by using json. Please see messagebank.json for reference. 

#### Challenges Faced
The biggest challenge I faced was when I had to find the best way to store and queue messages that were submitted by users that will eventually be sent to other users. I ended up implementing that feature by using a json file that workes just perfectly for this purpose. At this stage I also came to realise that I would need presubmitted bottled messages queued up as well so I generated 96 of them using an AI chatbot to save hours of work.

#### Code reuse 
Throughout the implementation process I tried not to repeat myself. I tried to follow the principle of 'don't repeat yourself'. I did this by writing functions to handle persistance (i.e. storing data) such as save_to_file or loading_from_file functions. I also wrote ones for slot management of the messages to assign them to the correct 15 minute interval and retrieve the correct slot for the current time. 

#### Interactivity
I added a countdown timer that updates every second using setInterval(). The timer starts at 900 seconds (15 minutes) and automatically converts
the time into minutes and seconds for display. It updates the text on the page in real time to show users when the next bottle will be available. When
the countdown reaches zero, it resets automatically to 900 seconds (15 minutes). This allows the timer to continue running without needing to refresh the page.

#### Interactivity: Python-specific description
I used Python with the Flask framework to add functionality. Flask gave the website a structured navigation system and made it feel like a complete web application.
I also used Python to handle user-submitted messages. When a visitor writes a message and submits the form, Python collects the input, stores it in a
list, and saves it permanently in a JSON file. This means messages are not lost when the page refreshes or the server restarts. It allows the app to
keep growing with new user content over time.
Another feature I built with Python was the time-slot message system. I divided the day into 15-minute intervals and assigned each message to a slot.
Depending on the current time, Python automatically selects which bottled message should appear on the homepage. This makes the website feel dynamic.
I also added a history feature where Python retrieves the last ten messages and displays them on a separate page. This gives users access to previous
content and encourages more engagement with the app.
I also used Python to process the contact form, where the website accepts the user’s name and displays a personalised response. Overall, Python made the page smarter by handling data storage, user input, page routing, and time-based content updates.

## Deployed site

This site has been deployed to GitHub Pages at the URL below:

[https://github.com/annakeil2/database_assignment](https://github.com/annakeil2/database_assignment)

Link to render.com deployment below:

[https://database-assignment-ohok.onrender.com/](https://database-assignment-ohok.onrender.com/)