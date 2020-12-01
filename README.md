
# Bug Tracker

Hello there!

![GitHub last commit](https://img.shields.io/github/last-commit/thiagohardt/bug-tracker?style=for-the-badge) ![enter image description here](https://img.shields.io/github/languages/count/thiagohardt/bug-tracker?style=for-the-badge)
 
[![FN9yS1.md.png](https://iili.io/FN9yS1.md.png)](https://freeimage.host/i/FN9yS1)

A live version can be found [here](https://bug-tracker-hardt.herokuapp.com/).

# UX

This project tries to create a clean website to track bugs or issues in a project.

The website is clean and intuitive, making navigation easy. 

## User Story

 **As a User**
 - As a User, I want to easily understand the main purpose of the site.
 - As a User, I want to be able to register a new account.
 - As a User, I want to be able to update and edit my profile.
 - As a User, I want to be able to delete my account.
 - As a User, I want to see all tickets created by me with a brief description of each.
 - As a User, I want to create new tickets.
 - As a User, I want to delete tickets created by me.
 - As a User, I want to update and edit tickets created by me.
 - As a User, I want to see tickets organized in different categories.
 - As a User, I want to be able to search tickets.
 - As a User, I want to have an overview of all my tickets and other users.  

## MVP
The page consists of main **dashboard** page where the user is able ton see most of the important information about his tickets categorized by **open**, **in progress**, **resolved** and **on hold**.
A **navbar** stays open and have all the main actions available for the user. From the navbar the user can go to different sections of the page: **dashboard**, **stats**, **new ticket**, **profile** and **logout**.
  

✅ Fully responsive.<br>
✅ Register a new account and login.<br>
✅ Edit profile. <br>
✅ View tickets categorized by user. <br>
✅ Create and edit tickets <br>
✅ Search for tickets <br>
✅ Overall stats for all tickets <br>


### Existing Features

- **New Account** <br>
To access the page the user must first create a new account by clicking on the "Register new account" link on the login form. 

- **Login** <br>
To access the page the user must use his credentials to login. In the case of this build there is also an option to login as a "Demo User" which allows the user experience the application utilizing a premade account. 

- **Profile** <br>
Shows your account information such as username, name, date of birth, email and profile picture.

- **Edit Profile** <br>
Allows the user to close or edit account information such as name, date of birth, email, password and profile picture.

- **Dashboard** <br>
Shows all tickets created by the user and categorizes them in different tabs by **Open**, **In Progress**, **Resolved** and **On Hold**. Clicking on a ticket will show a brief description with a **title**, **date created**, **due date**, **description**, **priority** and a **details button** that takes you to the expanded ticket view.

- **Ticket** <br>
Tickets have the following properties: **Number**, **Title**, **Date Created**, **Due Date**, **Priority**, **Status**, **Description** and **Attachment**.

- **Edit Ticket** <br>
Tickets can't be updated after they have been created appart from their status. They can be deleted though.

- **Create a new Ticket** <br>
Clicking on the link "New Ticket" on the navbar will open the ticket creation page. The page have input fields where the user should fill title, due date, description, priority and attachment. All tickets will automatically be created as status OPEN and NORMAL priority.

- **Stats** <br>
The stats page shows to the user the number of tickets he have created divided by categories and a bar chart with all tickets created in the system.


## Design
The whole UI is made utilizing Material Design concepts. For further information, please refer to the official documentation [here](https://material.io/).

### Wireframe
The wireframe for the project can be found [here](https://www.figma.com/file/rLIvFPJnckXF6UsNmM5zhQ/Bug-Tracker-Wireframe?node-id=101%3A5630).

### Color Scheme
This website followed Material Design color pallete and can be found
[here](https://material.io/design/color/the-color-system.html#tools-for-picking-colors).

### Typography

**Body:** Roboto<br>


## Technologies Used

Throughout the project, the following technologies were used.

- [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3](https://developer.mozilla.org/en-US/docs/Archive/CSS3)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [mongoDB](https://www.mongodb.com/)
- [jQuery](https://jquery.com/)
- [MateriazeCSS](https://materializecss.com/)
- [Chart.js](https://www.chartjs.org/)
- [Validate.js](https://validatejs.org/)
	 

## Testing
Detailed tests can be found [here](https://github.com/ThiagoHardt/bug-tracker/blob/main/Tests.md). 

## Deployment

The website is hosted and deployed by [Heroku](https://www.heroku.com/home).
Everything is deployed from the master branch and updates automatically whenever the branch is updated in GitHub.

1.  Log in Heroku (or create a new one if you don't have one.);
2.  Go to your dashboard.
3.  Click on the "New"  -> "Create new app" button located right under the navbar.
4.  Choose a unique name for your app.
5.  Choose a region (preferably close to where you are located).
6.  If everything works fine you should see the overview page of your app.
7.  Click on Settings tab.
8.  Reveal Config vars.
9.  Here we configure the IP, MONGO_DBNAME, MONGO_URI, PORT, SECRET_KEY values (thoose are  not public and are the same values on my env.py file(which is also private)).
10. Click on deploy tab.
11. In the case of this project I chose to conect my app to my repository in GitHub, so it auto updates my heroku app whenever the project is pushed. 
12. Click on the Deploy Branch button. 
13. DONE!

### Forking
If you want to fork the repository to your own GitHub account you can by clicking on the “fork” button under the navbar with your profile.

### Cloning

 1. If you want to clone the repository into a local file you can by:
 2. Clicking on the green button “Code” and copying the url showed.
 3. Open GitBash
 4. Change directory to the desired location where you want to clone the
    files to.
 5. Type “git clone” and paste the copied URL
 6. Press enter and you should have your local file cloned and ready.

## Credits

### Content

- All content on the page was created by me. 

### Media

- All images used are from [Unsplash ](https://unsplash.com/photos/k0KRNtqcjfw)

### Acknowledgements

-   My Mentor, **Oluwafemi Medale** for continuous helpful feedback.
