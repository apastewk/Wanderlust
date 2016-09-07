<h1>Wanderlust</h1>

<p><strong>Description</strong></p>

<p>Wanderlust organizes your travel plans in one convenient location for you to easily access at anytime.  Simply forward your confirmation emails and Wanderlust will take the parsed email details to aggregate all flight, hotel, car rental, public transportation, event and meeting confirmations into a complete and detailed itinerary.</p>

<p><strong>How it works</strong></p>

<p>Once an account is created, a user can create a trip. Trips are separated between past and future trips. From there, there are two ways for a user to input their confirmation details, either by filling out a form or by forwarding their confirmation email. For the form, a user can choose the type of confirmation that they would like to add and using jquery, the appropriate form will appear. If a user would like to forward their email, their email is sent to WorldMates API where the data is returned as XML and is sent to a temporary URL that was created using Ngrok. From there, the XML is naviagted and the imporant details are taken and stored in the PostgreSQL database. One of the main challenges was ensuring that the XML that was returned was matched with the appropriate user and trip. To match the user, the email address on the confirmation email was parsed and was matched to a users email in the database. Next the start date on the confirmation email is compared to the trips belonging to that user using a SQLAlchemy query. For the confirmation to match a trip, the start date has to fall between both the start date and end date of a trip. If any of these conditions are not met, a future implementation would be to send the user an email advising them of the particular error that occured and how to fix it. Once confirmations are stored in the database, all of the details are then presented in chronological order using Jinja.</p>

<p>Another API that is used is Flickrs API. Everytime a user goes to their itinerary page, an ajax call is made to Flickrs API. Flickr then gathers images for a particular destination and returns the image to the Wanderlust in JSON. The URL is then reconstructed using pieces of information from the JSON and then using jquery, the image is immediately displayed.</p>

<h3>Technology Stack</h3>

<p><strong>Application:</strong> Python, Flask, Jinja, SQLAlchemy, Ngrok, PostgreSQL<br>
<strong>APIs:</strong> WorldMates API, FLICKRs API<br>
<strong>Front-End</strong>: HTML/CSS, Bootstrap, JQuery, JavaScript, AJAX    </p>

<p>Allison Pastewka<br>
<a href="https://www.linkedin.com/in/allison-pastewka">Linkedin</a>
</p>