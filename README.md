# Wanderlust
###A full-stack web app built in 4 weeks as Hackbright Fellowship final project
<img src="/static/css/Wanderlust-homepage.jpg" alt="Wanderlust Homepage screenshot">
####Project Overview
Wanderlust is an interactive application for everyone from world explorers to family vacationers to businesspeople. It organizes your travel plans in one convenient location for you to easily access at anytime.  Simply forward your confirmation emails and Wanderlust will take the parsed email details to aggregate all flight, hotel, car rental, public transportation, event and meeting confirmations into a complete and detailed itinerary.

####Application Tech Stack 
Python, Flask, Jinja, SQLAlchemy, Ngrok, PostgreSQL
####APIs Used
WorldMate, FLICKR
####Front-End Tech Stack
HTML/CSS, Bootstrap, JQuery, JavaScript, AJAX
####GitHub Project URL
https://github.com/apastewk/Wanderlust
####Features
#####Create an account
* Sign up with your first and last name, email address and password

#####Create a trip
* Create a trip by inputting the trips destination, trip name, start and end date and any additional information
* Trips are separated by past and future trips 

#####Add trip details through the use of a form
* Choose the type of information that you would like to add to a trip
* The appropriate form appears through the use of jQuery's hide and show functions
* A flask route gets the forms inputs and stores the information in the PostreSQL database

#####Add trip details by forwarding a confirmation email
* Forward your email to WorldMates inbox (email address can be found by clicking on the 'About' button in the top right hand corner of Wanderlust)
* Worldmates API than parses the email and returns the data as XML to a temporary URL that was created using Ngrok
* The XML is navigated and the important details are taken and stored in the PostgreSQL database
* A confirmation email is matched to the appropriate user by matching the email address on the email to an email address in the database
* Next the start date on the confirmation email is compared to the trips belonging to that user using a SQLALchemy query
* For the confirmation to match a trip, the start date has to fall between both the start date and end date of a trip
* If any of theses conditions are not met, a future implementation would be to send the user an email advising them of the particular error that occured and how to fix it

#####View the itinerary for a trip
* The magnifying glass on the trips page will take you to the page that displays the trips itinerary
* Through the use of a generator, the daterange of a trip was established
* The daterange was then used to present the details in chronological order by date and time
* jQuery's toggle function allows a user to click on the 'Show More Details' button and more details about that particular part of the trip is displayed

#####Flickr API
* Everytime a user goes to a trips itinerary page, an ajax call is made to Flickrs API
* Flickr gathers images for a particular destination and return the image to Wanderlust in JSON
* The URL is then reconstructed using pieces of information from the JSON
* The image is immediately displayed by using jQuery



<p>Allison Pastewka<br>
<a href="https://www.linkedin.com/in/allison-pastewka">Linkedin</a>
</p>