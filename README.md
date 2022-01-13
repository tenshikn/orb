# ORB
#### Video Demo:  https://youtu.be/wBvbt49rL5A
#### Description: A web application to log and store new knowledge.

### Background
We often come across new knowledge and concepts when going about our daily activities but fail to recall it and its source when the need arises because we did not deliberately put them down or decided it was not
important. ORB is essentially a web application that allows users to add knowledge summaries (entries) to a wide array of topics (the vault). Through nicely organized images and widget entries,
learners can quickly add to and view already existing entries for their own future reference.

Upon logging in, which requires a username and a password, users can see at a glance all existing entries and the cpntents of their vault. Users can add to their vault collection via a search
and immediately add an entry or decide to do so at a later time. Users can also add to existing entries and view all entries on a particular topic by just clicking on the image representation.

Users should be able to perform the necessary tasks on whatever device they are currently on and as such the software was built to be responsive and usable on all screen sizes.

### Running
Start flask's built-in web server inside /project and visit the output URL to see the application in action.

### Understanding
## application.py
This file firstly imports necessary libraries and helper functions. After the application configuration
which includes app sessions and the likes, the file connects to orb.db: a disk-based database using python's sqlite3 module. Implementations of a bunch of routes for the app follows which includes an index and login route
for logging in, a /signing route strictly for an AJAX call, a /register and /signup for the signup process for
new users, a /new-topic route for knowledge base user query thanks to the
[wikimedia api](https://www.mediawiki.org/wiki/API:Main_page) and a /home route for the user's main page among others.

## helpers.py
helpers.py contains useful helper functions required by application.py. These include apology; responsible for displaying
certain error messages to the user as feedback, login_required function to ensure that a user needs to be logged in before
some routes are accessible and finally wiki_search; the function responsible for retrieving and parsing responses from
wikimedia's database

## orb.db
Orb.db is a lightweight disk based database for the web application. It contains tables users; all users of the app,
table vault; the table responsible for storing individual's respective titles and finally entries, which holds all user
entries for a particular title. SQL queries are performed on these tables to retrieve required data when the need arises.

## static/
Inside static/ folder exists the necessary files that adds style to the application.
This includes styles.css for CSS, and focus.js and validate.js

## templates/
Inside the templates/ folder exists the necessary HTML. These include layout.html;
the blueprint that allows other HTML files to inherit and build upon,
apology.html; the template used with the apology function found in helpers.py, index.html and signup html which are
responsible for user log in and sign up respecively, new-topic.html for the adding of new topics and/or entries
to a user's collection, and finally home.html and logs.html for displaying user's existing data.
These templates are returned and displayed to the user based on certain conditions by application.py.

### Implementation Details
- application.py is the controller of the application and contains all the necessary configurations and functions.
    -  index function is implemented in such a way that it displays an HTML form for user log in
        - index.html template is rendered when the /index or /login route is visited via a GET method
        - With a POST request, the user is successfully logged in and redirected to the /home route if the username and password is valid (checked via a database query) else they are notified.
        - There is a user id and username stored via flask's session object before a redirect to /home
    - signing function is implemented in such a way that it displays an HTML form for user signup
        - This function's sole purpose in life is to return a “jsonified” signup.html page to /index when one clicks on the signup button displayed on index.html. More on that in a bit.
    - signup function is implemented in such a way that it allows users to signup or register for an account in order to use the application.
        - With a GET request to the /register or /signup route, the user is immediately taken to the login in page i.e /index. The user would have to select the signup button displayed in index.html which will in
          turn display the signup form for registration (why? Just because.)
        - With a POST request, all necessary field details required for an account registration is retrieved and stored in the database.
        - The user is notified via the return of the apology function in helpers.py if the necessary requirements are not met.
        - On the other hand, the user is notified via a flashed message if the signup was successful and allowed to log in.
    - new_topic function is implemented in such a way that it allows users to add to their vault any topic or title or concept of their choice and an optional entry or log for the designated topic
        - With a GET request to the /new-topic route, new-topic.html is displayed to the user.
        - With a POST request to the route, the necessary data is obtained from the user. The data included are:
          - The image URL, a URL for a visual representation of the title or topic in question; a book cover for a book or a movie poster for a movie for example.
          - The title of the topic or concept.
          - An entry heading for the entry or log for the designated topic
          - And the entry itself
        - Via the image URL, the byte string representation of the image is downloaded if possible and added to the vault table together with the other data for the user.
        - If an entry is also sent to the server but does not come along with a heading, the user is notified via the apology function and requested to do so before added to the database.
    - title_search is implemented in such a way that users are quickly able to search and add the topic in question to their vault.
        - On a POST request, this function accepts the title and returns a “jsonified” data returned by the wiki_search function in helpers.py. More on that in a bit.
    - home function is implemented in such a way that the user is able to quickly view all their vault collection and related entries at just a glance
        - With a GET request this function renders home.html, displaying to the user their current collection.
        - A database query is made to the vault table of the user which includes the title as well its visual representation (recall that this is a byte string.)
        - The title together with a base64 encode of the image is sent as response and organized on home.html accordingly.
        - All entries by the user are also sent to home.html (sorted in decreasing order of their respective dates)
    - logout function is implemented in such a way that users can log out of the server.
        - This function clears the session when the user decides to log out.
    - error_handler function is implemented in such a way that the user is notified if any error occurs during their use.
        - This function returns the apology function together with the error code and the name when one occurs.

- helpers.py contains useful helper functions required by application.py.
    - apology function
        - This function renders apology.html and displays to the user an error code and message when the need arises.
    - login_required function
        - This function ensures that users are already logged in before they are allowed to visit certain routes of the web app.
    - wiki_search function
        - This function is implemented in such a way that it accepts a title as input and via a call to the [wikimedia api](https://www.mediawiki.org/wiki/API:Main_page), returns a list of the top 3 JSON response corresponding to the query
        - This data includes but is not limited to
            - The index of the information searched on the wikimedia database
            - The description of the title searched
            - and the URL of the image representing the data

- Inside templates/ exists mobile-friendly HTML files which acts as the user interface of the software.
    - layout.html
        - This HTML file is essentially a blueprint that allows all other templates to import necessary contents. This file notably imports
        - [Bootstrap](http://getbootstrap.com/docs/4.5/); a CSS and JavaScript library for a responsive and mobile-friendly application
        - Fontawesome for necessary fonts
        - Favicon for the application's favicon
        - And LazyLoad to slow down image loading when not in the view-port
    - index.html
        - This HTML file is rendered by the index function in application.py and displays a form for user login and user signup
        - A user need only supply a username and a password and click on the login button.
        - The user is also prompted via static/validate.js if at least one of the required fields is left blank
        - Via a JavaScript event listener, clicking on the signup button displayed on index.html results
          in the dynamic change of the form presented to that of signup.html via a callback function which
          asynchronously accepts the html data from /signing and dynamically runs code such as automatic
          username creation and form validation much like that presented in static/validata.js
    - signup.html
        - This HTML contains the singup form for user account creation
        - This form's purpose in life is to replace the form in index.html on user request to sign up and accept the required details for a sucessful account creation.
    - home.html
        - This HTML file displays all added topics and concepts (the vault) and all corresponding logs (entries) in an easily readble format.
        - The 'vault' contents are base64 image encoded button displayed on the left pane (or center depending on the viewport) which leads to a display of all corresponding entries on logs.html when clicked.
        - All entries and their corresponding date and heading on the other hand are displayed
          on the center page containing all entries
    - logs.html
        - This HTML displays all entries on a particular topic or concepts in widget like format when
        requested by the user via a click on the designated image
    - new-topic.html
        - This HTML file is responsible for allowing the user of the web application to add to their collection.
        - Users can search for anything they would like to file into their personal collection and get a visual representation of the topic in question.
        - The title or topic that was searched for can also be edited if they are not satisfied with the data response
          and would personally like to use a different name.
        - By using the power of JavaScript's session storage, this HTML file also allows the user to add entries
          to a particular topic without need to query orb.db
    - apology.html
        - This HTML file is displayed by the apology function in helpers.py
- Inside static/ exists the necessary static files needed to style the template files
    - focus.js
      - This JavaScript function's sole purpose in life is to focus on an image that is hovered
    - validate.js
      - This JavaScript function's purpose in life is to prevent form submissions if the necessary fields are empty

#### The Future
Below is a possible list of features that will be added to ORB down the line
- Visually stunning links between two or more vault members if knowledge summaries are similar
- Dark Mode
- PWA