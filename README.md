![Hero Image](Readme_files/Hero_Image/Hero_Image_Readme.png)

<h1 align="center"> The Book Nook </h1>
<p align="center"><a href="https://booknook-megan-9235b81ca921.herokuapp.com" target="_blank" rel="noopener noreferrer">| Live Link Here |</a></p>

<h1 align="center"> Introduction: </h1>

<p>
The Book Nook is my last assessed portfolio project developed as part of the Code Institute Full Stack Software Developer Bootcamp, consisting of learning outcomes to utilise HTML5, CSS3, Bootstrap, JavaScript, Python, Django, Cloudinary & Heroku in order to fulfil the necessary requirements for the brief.

The live project can found here: <a href="https://booknook-megan-9235b81ca921.herokuapp.com" target="_blank" rel="noopener noreferrer">| Live Link Here |</a>


<h2 align="center"> Table of Contents:</h2>

1. [Introduction](#introduction)
2. [Project Outline](#project-outline)
   - [Key Objectives](#key-objectives)
3. [UX Design](#ux-design)
   - [User Stories](#user-stories)
   - [Color Design](#color-design)
4. [Wireframes](#wireframes)
5. [Imagery](#imagery)
6. [Features](#features)
   - [General Features](#general-features)
7. [Agile Section](#agile-section)
8. [Responsive Design](#responsive-design)
9. [AI Implementation](#ai-implementation)
10. [Testing](#testing)
    - [Optimization](#optimization)
11. [Database](#database)
12. [Deployment](#deployment)
13. [Credit](#credit)


## Project Outline

The Book Nook is a fictional library harnessing Django. The website primary use is to access information on published books and make reviews, as my MVP. However my extended goal is to have it function fully as online library with adding features such as having the ability to read the books online, having author accounts that can publish theyre books with ease and the admin can review the content before allowing to be released to the main site. I'm aiming to have it so that the users can hide specific topics, authors or books that they'd not like to see on their pages, so the website is fully customised to the user. 


#### Key Objectives

 - A clear and easy to navigate website,
 - The ability for users to Create, Read, Update and Delete book reviews,
 - A large collection of books for Users to review.
 - I want it to be fully responsive across various sizes, especially phone and tablet due to that being more practical for reading.
 - I want the website to be customizeable for logged in Users.

## UX Design

### User Stories

- As a Reader,
  I would like to purchase books directly from the website,
  So that I can easily obtain books I want to read.

  For this to be done, these goals need to be met:

    - Books should have clear pricing.
    - Purchased books should be accessible from a user’s library.
    - The books purchased should be viewable from the account purchase history,

- As a Reader,
  I would like to leave reviews on books
  So that I can share my opinions and help others decide whether to read a book.

  For this to be done, these goals need to be met:

    - A review system must be implemented with a rating system (e.g., stars, thumbs up/down).
    - Users must be able to write, edit and delete reviews.
    - Reviews should be visible on the book’s page.
    - When reviews are deleted they should be notified.

- As a New User,
  I would like to be able to create an account that matches me
  So that I can See things appropriate for my age.

  For this to be done, these goals need to be met:

    - Two main reader accounts i.e. Child and Adult available at account creation,
    - Create an account Page, Sign in and Account Pages.

- As a Reader,
  I would like to create a Wishlist of books
  So that I can keep track of books I want to read or buy later.

  For this to be done, these goals need to be met:

    - Users should be able to add books to a personal Wishlist,
    - The Wishlist should be accessible from a Users personal Library,
    - When a User purchases a book it gets removed from the wishlist,

- As a Reader,
  I would like personalised homepage
  So that I can easily find books that match my interests.

  For this to be done, these goals need to be met:

    - The homepage should recommend books based on previous purchases, Wishlist, and reviews.
    - A section should highlight trending books and new releases.
    - Books should be broken up by genre also.

- As a Admin,
  I would like to have a quick overview of important statistics
  So that I can provide a more optimal service to the customers.

  For this to be done, these goals need to be met:

    - Total User count available through admin,
    - Total Book Count,
    - Total Author Count,



### Color Design

For this project I have mimicked a previous project I completed on a similar topic to help speed up time, I have chosen simple reds to mimic old fashioned ribbon bookmarks. I have used a wooden background to mimic the back of a library shelf with the actual shelves themselves having shelf images. The design of this webpage is to represent an actual library bookshelf but digitally.

![Colour Palette](Readme_files/Color_Palette/Colour_Palette.png)

This is the original design plan.

## Wireframes

These wireframes have been created using Balsamiq to define the key feature layout to guide the user experience design as well as blocking out the rough color pallete to identify any key issues. I will be utilising Bootstrap's framework to help blockout the website key elements. 

#### Index Page
![Index Page](Readme_files/Wireframes/Home_Page.png)

This is the home page. I wanted it so that you can see a full genre list of titles as well as having two customised shelves at the top. 

Recommended shows the user what it recommends based on their current reading list it will take into account what is their current favourite genre, author and if theyve hidden any topics, authors or books so that it will only display books that will interest the user without any of the topics, books or authors that might have come up within that query.

Most popular is less specific to the user and more specific to the site, it shows what is currently 'trending' on the site. So it will display books with high ratings, high wishlists and high currently reading. This allows the user to see what other readers are currently interested in. 

#### Search Page
![Pre Search](Readme_files/Wireframes/Search_Page_Pre_Search.png)

This page I wanted it so that user can get even more customised shelves pre-search.

New additions is customised to the site more than the user, this is to advertise recent additions to the site that wouldnt necessairly show up through recommended or most popular, due to the lack of reviews, wishlists or currently reading as they are new to the site.

From Authors you've liked section takes in account your reviews and Authors who you've read a larger percentage of their books. This is so you can see if an author you've liked has any more works for the user to read.

Books similar to {{Book Name}} would work by finding out what book the user has read and enjoyed and display books that are within that books genre and contain similar topics to the book listed.

![After Search](Readme_files/Wireframes/Search_Page_After_Search.png)

After Search it will display the books that match the search. Ie if you search for fantasy books it will display all fantasy books in the database bar the books that contain any of the three hide-able characteristics so that viewers can avoid topics that they might find triggering or simply dislike.

#### My Library
![User Library](Readme_files/Wireframes/My_library.png)

This is the users personaly library shelves that they can customise as they want. 

The Wishlist shelf is for books that the user would like to purchase at a future date. This is automatically added when the player clicks the heart icon on the book page. 

Currently Reading would display books that have been purchased.

Add a new shelf is where the user customisation comes in, they can create a new shelf and customise its title ie to 'Finished' and books they have finished can now be selected and moved to that shelf manually. This is another part of the project that is a 'Could Have' using the 'MoSCow' Method.

#### My Account (Admin, Author, Regular User)
![Account Reader](Readme_files/Wireframes/Account_Page.png)

This is the account information page for a Regular User, it will show the username and account type (Could Have Feature). As well as theyre favourite genre as depicted above by the % they've read of that genre so if out of 10 books 7 of those are fantasy, fantasy would become the favourite genre. The same calculation would go for depicting the Users favourite Author.

The next section is where the users hidden topics, authors, books can be seen as well as a collection of all the users reviews. The reviews are shown by default on page loading. 

When you select see hidden another page element is shown below which shows the three options Authors, Books and Topics. If you click Authors you can see the authors name, the date hidden and a fav-icon to unhide the author, Hidden Books is similar except it also shows the Book title as well as the three other elements listed before. Hidden topics shows the Topic name, date hidden and a fav-icon to unhide the topic.

The review section shows the title of the book the review was on, your rating out of 5, the date of the review and the main text of the review paired with a go to review button that will take the User to that review so that they can edit it or delete it.

Lastly, is the list of purchases so that the user has an itemised list of all books purchased, the price they paid and the date of purchase.

![Admin Review](Readme_files/Wireframes/Admin_Review_Page.png)

This is what an Admin would see on their account page. It is more buisness focused showing statistics on the total user count to see how the website is doing in terms of popularity, the popular genre so the admin knows what genre of books is currently the most popular. This would aid in what they would add to the site to satisfy the largest consumer base.

It also displays the recent requested features by the Users, so the admin knows what the site is missing and what could be improved upon.

The last section is the recent Bug Reports section, which showcases recent bug reports so that the admins can keep up with maintanence and keep the site bug free.

Lastly, is the 'Admin Tools' button which takes the admin straight to the indepth admin tools ie the Django Backend Admin panel. This makes the site more userfriendly for the less technically minded Admins.

![Author Review](Readme_files/Wireframes/Author_Review_Page.png)

This is what the Authors would see on their Account page, It gives them quick and easy to understand statistics about their Books performance on the site. 

The top section shows the total reader that have currently purchased their book through the site, the total amount of users who have the authors books wishlisted as well as the total reviews on the site across all books. 

The other section is comprised of three dropdown tables, the first for published books, the second for Books that are awaiting admin approval and lastly the drafts. The first drop down showcases the total amount of published books in numerical form and once clicked would drop down a list with the book title and two fav-icons one for extra information and one to take the author to that books store page. The extra information you would get about that book would be the date it was published on the site, How many users have purchased the book and wishlisted it. As well as total reviews and the average rating across all of those reviews. The middle drop down for books awaiting follows a similar pattern, except the extra information fav-icon shows the status of the books awaiting approval and the other icon would take the author to its draft form to review. The draft dropdown is the same as the previous two except the extra information icon is swapped for the edit icon as since its not been submitted to the admin team it can still be edited. An example of the extra information can be found below, for the purchased books.

#### Author Public Profile
![Author Public Profile](Readme_files/Wireframes/Author_Account_Page.png)

This is the customisable Public Profile for Authors that is connected to their book pages. It shows the authors name and the authors rating which is the average rating on each of their published books. As well as a small Bio about the author. This is customiseable through their account page.

The Published works shelf shows the whole collection of works published by the author. 

Series A is an automtically created shelf for the author that showcases books that are within a series. 

Series B is exactly the same as above but showcases books that are in a different series, ie one shelf per series. These shelves would be hidden if the author didnt have any published books within a series yet. For example if they have book 1 out of 3 published and have not yet publsihed the second the Series bookshelf would not show up until they published the second book and connected the two together.

#### Book Page
![Book Page](Readme_files/Wireframes/Book_Page.png)

This is what the Users see when they click the covers displayed on the shelves. It will show the Book title in the ribbon at the top of the page with the Fav-Icons for the wishlist (Heart) the settings (Cog). The settings icon would pop up a model which shows the options to hide the Book, Author and to select topics out fo the list to hide.

Below is the Book Cover with a Purchase button which will display the price set by the author. As well as in the other box it shows the Author's name, the genre of the book, how many chapters it has as well as the average rating shown in stars and numerically. 

The box below is a short about of the book usually a condensed version of the blurb. As well as underneathe includes the topics the author has selected from a list.

Similar to the author public profile, the series shelf only appears if this books is apart of a published series. 

The similar shelf, shows books that have the same genre and topics, once again minus any of the hidden catagories. 

The By Author shelf is a replica of the Published works shelf on the author page minus any of the hidden catagories. 

The review section has the amount of reviews published and the average star rating for that book. Create a review drops down the form which allows the user to give the books a rating, title and review text and submit it. It will then display at the top for the user to then access to edit or delete the review. Below in scroll format is other Users reviews.

#### Author Publish Page
![Book Page](Readme_files/Wireframes/Author_Book_Creation_Page.png)

This is another part of the project that is a 'Could Have' using the 'MoSCow' Method. This is the Author book creation page that the author fills out to publish a new book, they can upload their own book cover and fill out all the information necessary like price, genre, age rating, the about and the topics. Then they would upload their a PDF of their book through the upload text button. If the book being published is the second book of a series they then can connect the books together by selecting the book through the shelf, if no book is selected it doesnt become part of a series. The view Book shows the book pages as a reader you will see below and publish would set the book as a un-editable draft for admin's to review.

#### Book Reading Page
![Book Page](Readme_files/Wireframes/Book_Viewer.png)

This is another part of the project that is a 'Could Have' using the 'MoSCow' Method. This is the reading section of the project where once you've purchased the books, you can read the books. The data would be saved to the profile so you can leave a book and it'll remember where you are so the user can pick it straight up right where they left off. They also have a lot of accessibility functions like changing the font size, the page mode and wether or not they would like the page turn effect and sound effects. 

## Imagery

In terms of imagery in this website it is going to be minimal, this is due to the fact that the main focus should ideally be on the book covers themselves. Due to the amount of covers going to be visible on a device at a time if the page has too many visual elements outside of whats necessary i feel like it would quickly overwhelm the user. 

Any extra images, aka a hero image, should be simplistic and complementary to the theme. 

Book Cover Credits: 
Each book cover is designed by seperate artists, They are used for educational purposes (aka this project).

Hero Image:
The hero image is a free image hosted on Adobe Stock images by RPL-Studio.

## Features
#### General Features
In order to fulfil the criteria set out by the user stories, listed above, the page will consist of various sectioned information each with a variety of links, resources or other elements that contribute to the website fullfilling its goals and aiding the user. 

Upon coding the projectand implementing the Bootstrap Framework the features the design shifted slightly from the original wireframes.
Some key adjustments are as follow:
- The removal of the Book Purchase date on account due to it on page load defaulting to today's date.
- The Fav-icons on the individual book store pages being move to opposite sides of the title due to on mobile it was hard to press the one you would like and not the other icon.
- The ability to create your own shelf and move books between shelves as it became over-complicated for my first time using Django and for the shelves to be saved it had to be part of a model and then display correctly.
- I also had to relocate the recommended shelf from the index.html to the search due to the amount of shelves causing some optimazation issues.

### Agile Section

I have throughout this project followed an agile workflow and methodology. I iterated and bug tested throughout due to the time constraint paired with dailing back on the overall scope of the project, for example in this final project the author's can publish themselves and the reading function had to be put off. I primarily focused on the must haves and really tried to perfect them before moving onto the next.

At the start of the project i set up a project board to keep track of user stories and my progress on them using the 'To do', 'In Progress' and the 'Done' columns. I created a list of user stories each assigned a 'MOSCOW' prioritisation (must have, should have, could have, won't have) tag. This is following the KanBan method of tracking progress for a better workflow management.

You can see how the project has developed from looking at the original wireframes in the images below to the current deployed website.
Here is my project board: <a href="https://github.com/users/MeganOtton/projects/5/views/1" target="_blank" rel="noopener noreferrer">| Here |</a>

#### Index Page
![Index Page](Readme_files/WebPage_Final_SC/Index.png)

This is the final version of the website. This is the index. I am overall really happy with how it came out and how quick the website is to run despite over 60+ books being loaded. 

#### Search Page
![Search Page](Readme_files/WebPage_Final_SC/Search_Page.png)

This is the final search page which turned out really well and for my first time coding a search bar into any of my websites im surprised with how well it functions. 

#### Library Page
![Search Page](Readme_files/WebPage_Final_SC/My_Library.png)

#### Account Page (Reader)
![Account Page (Reader)](Readme_files/WebPage_Final_SC/Account_Page_Reader.png)

#### Account Page (Admin)
![Account Page (Admin)](Readme_files/WebPage_Final_SC/Account_Admin.png)

#### Individual Book Page
![Individual Book Page](Readme_files/WebPage_Final_SC/Bookstore_Page.png)

#### Sign In
![Sign In Page](Readme_files/WebPage_Final_SC/Sign_in.png)

#### Sign Out
![Sign Out Page](Readme_files/WebPage_Final_SC/Sign_out.png)

#### Register
![Register Page](Readme_files/WebPage_Final_SC/Register.png)

## Responsive Design

I will be utilising the Bootstrap Framework to speed up my effeciency when it comes to media queries and the overall project. With some experimentation I have been able to create a page that is fully responsive to modern standards with the use of media queries and a JavaSript script for the shelves due to Bootstraps carousels causing some technical glitches that would take the project away from my wireframes. 

Below is an image of my website from different devices.

![Responsive Design](Readme_files/Responsive_Image/Responsive_Image.png)
Due to the way my project detects which device the user is using the regular method of showcasing a website's responsivity did not work, so the above image is replacement using inspect tools device sizing.

## AI Implementation

#### Use Cases and Reflections:
#### - Code Creation
  - I used AI like Copilot, Claude and Chatgpt to help implement and generate elements from bootstrap without having to source it from bootstraps website. This sped up creation time exponentially in a project where time is limited.
  - I used it to also generate, edit and fix code that I was stuck on to save time during development.

#### - Debugging 
  - I used Copilot, Claude and Chatgpt to fix or change elements of my own code to make them more aligned with the websites vision. This was a useful time saving technique which if nto used could have taken hours of research to fix/edit manually.

#### - Overall Impact
  - AI tools streamlined repetive tasks and basic jobs, enabling me to focus on the more complex elements of the development. (Same goes for the Bootstrap elements)

More Information:
 
In terms of how i used AI to optimize my workflow I found it very helpful to highlight segments of code and give very specific prompts to Claude or Copilot to optimize, debug or fix code that i created. Also when generating code from scratch i broke down what the function of the code down into small bulletpoints and was very precise in order to ensure the result of the ai generated code to be as close to its prompt as possible, I then went and tweaked and edited the code to refine it to match the purpose even further. When it came to Debugging with copilot, I found it useful to highlight the sections of code and ask Copilot to debug why this section had broken.  When it came to optimazation of the project it was also quite useful in the production and debugging of Media Queries in CSS. Following a similar method as above I found highlighting the specific section that was broken a good way of narrowing the AI's attention onto the specific task at hand.

## Testing
- Please see [testing.md](testing.md) file for all testing.

Testing was done throughout the project to ensure after each feature was added in that it worked effectively and did not break any previous features. 

### Optimization

Due to my lack of experience with both Python and Django this project was quite ambitious to take on when it came to removing my placeholders and filling the database with real books the website that ran smoothly before started to breakdown and slow loading times became prevelant. Using Django Debug tool, and Charlie Flockharts help, it helped track down where my problems where and what I should be optimizing.

![Pre Optimazation](Readme_files/Optimisations/Bad_Optimisation.png)

This was what could be seen pre-optimazation in the Django debug tool, as you can see on my index alone it was running over 578 queries for all of the various shelves on the index to create the customisable user experience. By adding all those filters that ran per shelf each time on page load it severly bottlenecked the website.

![Post Optimazation](Readme_files/Optimisations/Good_Optimisation.png)

This is what I managed to optimize it down to. Instead of 578 queries i managed to simplify the index code to only run 6 queries with help of changing the way the users are set up. Instead of running all of those filters to customise the website on the shelves themselves instead I used a many to many field of all accessible books to the user that updates when certain conditions are met so i could effectvely bypass using all the front end filters that had to re-read all 60+ books and sort it per shelf. This got the load time from 20 Seconds down to 1/2 a second.

### Validation

#### HTML Validation
##### Index Validation
![Index Validation](Readme_files/Code_Validation/HTML/Index_Html_Validation.png)

##### Book Page Validation
![BookPage Validation](Readme_files/Code_Validation/HTML/Bookpage_Validation.png)

##### Search Page Validation
![Search Validation](Readme_files/Code_Validation/HTML/Search_Validation.png)

##### My Library Validation
![My Library Validation](Readme_files/Code_Validation/HTML/my_library_validation.png)
Two warning occur on this page that ive hidden which is from two sections of code that have the attribute 'display: None;', These sections are code that works but didnt have the Django backend functionality so the code is a placeholder, so that i can finish off that section after the hand-in on my own seperate forked branch.

##### Account Validation Admin
![Admin Account Validation](Readme_files/Code_Validation/HTML/account_validation_reader.png)

##### Account Validation Reader
![Reader Account Validation](Readme_files/Code_Validation/HTML/Admin_Account_Validation.png)


##### Sign In Page Validation
![Sign In Validation](Readme_files/Code_Validation/HTML/sign_in_validation.png)

##### Register Page Validation
![Register Validation](Readme_files/Code_Validation/HTML/Register_Validation.png)

#### CSS Validation
![CSS Validation](Readme_files/Code_Validation/CSS/CSS_Validation.png)

#### JavaScript Validation
##### Character Count Script (Book About Section) Validation
![JS Validation](Readme_files/Code_Validation/JS/Char_Count_JS_Validation.png)

##### Comments Validation
![JS Validation](Readme_files/Code_Validation/JS/Comments_JS_Validation.png)

##### Device Detection Validation
![JS Validation](Readme_files/Code_Validation/JS/Device_Detection_JS_Validation.png)

##### Eye (Hide Books & Topics Model) Validation
![JS Validation](Readme_files/Code_Validation/JS/eye_js_Validation.png)

##### Hidden Book, Topics List Validation
![JS Validation](Readme_files/Code_Validation/JS/Hidden_Account_JS_Validation.png)

##### Index Inline Script Validation
![JS Validation](Readme_files/Code_Validation/JS/Inline_Index_JS_Validation.png)

#### Python Validation
##### Profile Validation
###### Admin Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Admin_Validation.png)

###### APPS Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Apps_Validation.png)

###### Check User Ages Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Check_User_Ages_Validation.png)

###### Forms Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Forms_Validation.png)

###### Models Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Models_Validation.png)

###### Tasks Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Tasks_Validation.png)

###### URLS Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Urls_Validation.png)

###### Views Validation
![PY Validation](Readme_files/Code_Validation/PY/Profile/Views_Validation.png)

##### Store Validation
###### Admin Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Admin_Validation.png)

###### APPS Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Apps_Validation.png)

###### Context Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Context_Validation.png)

###### Custom Filters Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Custom_Filters_Validation.png)

###### Forms Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Forms_Validation.png)

###### Models Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Models_Validation.png)

###### URLS Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Urls_Validation.png)

###### Views Validation
![PY Validation](Readme_files/Code_Validation/PY/Store/Views_Validation.png)

##### Root Validation
###### ASGI Validation
![PY Validation](Readme_files/Code_Validation/PY/TheBookNook/Asgi_Validation.png)

###### Settings Validation
![PY Validation](Readme_files/Code_Validation/PY/TheBookNook/Settings_Validation.png)

###### URLS Validation
![PY Validation](Readme_files/Code_Validation/PY/TheBookNook/Urls_Validation.png)

###### WSGI Validation
![PY Validation](Readme_files/Code_Validation/PY/TheBookNook/Wsgi_Validation.png)

### Lighthouse

#### Mobile
![Mobile Lighthouse](Readme_files/Lighthouse/Mobile_Lighthouse.png)

#### Desktop
![Desktop Lighthouse](Readme_files/Lighthouse/Desktop_Lighthouse.png)

## Database
- I used Code Institute's PostgreSQL database.

### Database planning 
- I created ERD Diagrams using DBDiagram.io to plan out the database models and fields.

### Creating a database
1. Navigate to [PostgreSQL]() from Code Institute.
2. Enter your student email address in the input field provided.
3. Click Submit.
4. Wait while the database is created.
5. Check your email.
6. You now have a URL you can use to connect your app to your database.

## Deployment

The website was deployed to Heroku and can be found at the top.

### Heroku

Heroku is a cloud platform that lets developers create, deploy, monitor and manage apps.

You will need a Heroku log-in to be able to deploy a website to Heroku.

Once you have logged into Heroku:

Click 'New' > 'Create new app'

Choose a unique name, choose your region and press 'Create app'

Click on 'Settings' and then 'Reveal Config Vars'

Add a key of 'DISABLE_COLLECTSTATIC' with a value of '1'.

Add a key of 'DATABASE_URL' - the value will be the URL you were emailed when creating your database.

Add a key of 'SECRET_KEY' - the value will be any random secret key (google 'secret key generator' and use it to generate a random string of numbers, letters and characters)

In your terminal, type the code you will need to install project requirements:

pip3 install gunicorn~=20.1

pip3 install -r requirements.txt

pip3 freeze --local > requirements.txt

Create an 'env.py' file at the root directory which contains the following:

import os

os.environ["DATABASE_URL"]='CI database URL'

os.environ["SECRET_KEY"]=" Your secret key"

Create a file at the root directory called Procfile. In this file enter: "web: gunicorn my_project.wsgi" (without the quotes)

In settings.py, set DEBUG to False.

YOU SHOULD ALWAYS SET DEBUG TO FALSE BEFORE DEPLOYING FOR SECURITY

Add ",'.herokuapp.com' " (without the double quotes) to the ALLOWED_HOSTS list in settings.py

Add, commit and push your code.

Go back to Heroku, click on the 'Deploy' tab.

Connect your project to GitHub.

Scroll to the bottom and click 'Deploy Branch' and your project will be deployed!

### Cloning

To clone a GitHub repository:

On GitHub.com, navigate to the repository you want to clone.

Click the "Code" button (found above the list of files).

Copy the URL for the repository.

Open Git Bash or your chosen terminal.

Navigate to the directory where you want to clone the repository.

Type: git clone https://github.com/MeganOtton/BookNook.git

Press Enter to create your local clone.


### Forking

'Forking' the GitHub repository means creating a copy which can be viewed/changed without changing the original.

To fork a GitHub repository:

Login to GitHub and navigate to the repository you want to fork.

Click the "Fork" button (found above the Settings button).

You will now have a copy of the original repository in your GitHub account.

*Once the project is cloned or forked, in order to run it locally, you'll need to follow these steps:

Run the server: python3 manage.py runserver

Stop the app once it's loaded: CTRL+C or ⌘+C

Make any necessary migrations: python3 manage.py makemigrations

Migrate the data to the database: python3 manage.py migrate

Create a superuser: python3 manage.py createsuperuser

## Credit

As one of my final modules, I am exceptionally thankful for the team at Code Institute for their exceptional lesson plans, Guidance and Professionalism. I have learnt so much in the last 16 weeks and i'd have not been able to do this incredible feat without their patience and guidance.

Lastly, for his tremendous help and genious level expertise Charlie Flockhart, who helped debug and test the website and offering expertise when needed. 
