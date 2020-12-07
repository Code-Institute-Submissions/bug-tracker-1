## Testing User Stories 
---
 
 - As a User, I want to easily understand the main purpose of the site.
   - The page shows the product logo followed by a clear login form that gives me the option to log in with my credentials or register a new account. 
 
 
 - As a User, I want to be able to register a new account.
   - Clicking on the "register new account" link I am presented with a form where I can easily create a new account. 
   - Required fields display an error message in case they are not valid. 
 
 
 - As a User, I want to be able to update and edit my profile.
   - I can update my profile by clicking on the dropdown menu in the navigation bar. 
   - The form let me change my name, date of birth, e-mail, password, and profile picture.
 
 
 - As a User, I want to be able to delete my account.
   - I can delete my account if I want to and clicking on the "delete" button shows me a confirmation message asking if I am sure to delete my account.
 
 
 - As a User, I want to see all tickets created by me with a brief description of each.
   - As soon as I log in the page presents a dashboard with all the relevant information.
   - Tickets are categorized by "Open", "In Progress", "Resolved" and "On Hold".
   - Open tickets can be viewed by all users. The other categories are only visible to the user that is assigned to them.
 
 - As a User, I want to create new tickets.
   - I can easily create new tickets by clicking on the button "New Ticket" in the navigation bar.
   - Required fields display an error message in case they are not valid. 
   - A PDF or image file can be added to the ticket as an attachment.
 
 
 - As a User, I want to delete tickets created by me.
   - Only tickets created by the user can be deleted.
   - I can delete a ticket if I want to by clicking on the "delete" button. This shows me a confirmation message asking if I am sure to delete the ticket.
 
 
 - As a User, I want to update tickets created by me.
   - If I click on the ticket details button I can see an expanded view of the ticket.
   - The only field that can be updated is the status.
  
 - As a User, I want to see tickets organized in different categories.
   - Tickets are categorized by "Open", "In Progress", "Resolved" and "On Hold".
 
 
 - As a User, I want to be able to search for tickets.
   - There is a search field on the top of the tickets tab where I can easily search for tickets by title or description.
 
 
 - As a User, I want to have an overview of all my tickets and other users. 
   - Clicking on the stats link in the navigation bar I can see information about my tickets and a graph showing the number of tickets created in total including other users.
 
 
 
## Validation
---
 
### User Signup 
- Username 
  - Unique 
  - Max Length: 15 characters
  - Required
 
- Name 
  - Max Length: 40 characters
  - Required
 
- Date of Birth 
  - Required
 
- Email 
  - Required
  - Unique
  - Only email forta accepted
 
- Password 
  - Min Length: 5 characters,
  - Max Length: 15 characters
 
- Profile Picture   
  - Only images accepted
 
### New Ticket
- Title
  - Min Length: 5 characters,
  - Max Length: 50 characters,
  - Required
 
- Due date  
  - Required
  - Can't be less than today's date
 
- Description
  - Max Length: 500 characters,
  - Required
 
## General Testing
---
- Login
  - Password and Username must be filled. If not returns an error.
  - If not registered clicking on the login button returns an error.


- Signup form / Edit Profile form
  - Form only submits when all required fields are valid. 
  - Duplicated emails or usernames are not accepted.
  - Error messages are shown properly.

- New Ticket form
  - Form only submits when all required fields are valid. 
  - Error messages are shown properly.

 
### Browsers
 
**FireFox**
 
 ✅ Links <br>
 ✅ Responsiveness<br>
 ✅ Data<br>
 
**Chrome**
 
 ✅ Links <br>
 ✅ Responsiveness<br>
 ✅ Data<br>
 
**Edge**
 
 ✅ Links <br>
 ✅ Responsiveness<br>
 ✅ Data<br>
 

