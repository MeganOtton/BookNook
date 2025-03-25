# Testing Document

| Location                    | Feature                     | Expected Outcome                                                                                | Pass/Fail       |
| --------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------- | --------------- |
| Navbar                      | Book Icon                   | On click goes to home webpage                                                                   | Pass            |
| Navbar                      | The Title                   | On click goes to home webpage                                                                   | Pass            |
| Navbar                      | Home link                   | On click goes to home webpage                                                                   | Pass            |
| Navbar                      | Search link                 | On click goes to Search webpage                                                                 | Pass            |
| Navbar                      | My Library link             | Only Shown if User Logged In + click goes to Library webpage                                    | Pass            |
| Navbar                      | Admin link                  | Only Shown if User Admin + On click goes to Admin Panel                                         | Pass            |
| Navbar                      | Account link                | Only Shown if User Logged In + On click goes to Account webpage                                 | Pass            |
| Navbar                      | Logout link                 | Only Shown if User Logged In + On click goes to Sign out webpage                                | Pass            |
| Navbar                      | Register Link               | Only Shown if User Logged Out + On click goes to Sign up webpage                                | Pass            |
| Navbar                      | Login Link                  | Only Shown if User Logged Out + On click goes to Sign in webpage                                | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Footer                      | Github Link                 | On click goes to Github in new tab                                                              | Pass            |
| Footer                      | Youtube Link                | On click goes to Youtube in new tab                                                             | Pass            |
| Footer                      | Facebook Link               | On click goes to Facebook in new tab                                                            | Pass            |
| Footer                      | Instagram Link              | On click goes to Instagram in new tab                                                           | Pass            |
| Footer                      | X Link                      | On click goes to X in new tab                                                                   | Pass            |
| Footer                      | Email Link                  | On click goes to Email app                                                                      | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Sign Out Page               | Sign Out Button             | On click goes Signs User Out                                                                    | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Sign In Page                | Username Input              | Allows User to input their Username                                                             | Pass            |
| Sign In Page                | Password Input              | Allows User to input their Password                                                             | Pass            |
| Sign In Page                | Remember Me Checkbox        | Allows User to select their info to be remembered                                               | Pass            |
| Sign In Page                | Sign In Button              | Allows User to Sign into their account if all details = correct                                 | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Sign Up User Page           | Sign In Redirect            | On click goes to Sign In webpage                                                                | Pass            |
| Sign Up User Page           | Sign Up As Author Redirect  | On click goes to Sign Up Author webpage                                                         | Pass            |
| Sign Up User Page           | Username Input              | Allows User to input their Username                                                             | Pass            |
| Sign Up User Page           | Email Input                 | Allows User to input their Email                                                                | Pass            |
| Sign Up User Page           | Password Input              | Allows User to input their Password                                                             | Pass            |
| Sign Up User Page           | Password Input 2            | Allows User to input their Password Again to match First Password Input                         | Pass            |
| Sign Up User Page           | Sign Up Button              | Allows User to Sign Up to an account if all details = correct                                   | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Sign Up Author Page         | Sign In Redirect            | On click goes to Sign In webpage                                                                | Pass            |
| Sign Up Author Page         | Sign Up As Reader Redirect  | On click goes to Sign Up Reader webpage                                                         | Pass            |
| Sign Up Author Page         | Username Input              | Allows User to input their Username                                                             | Pass            |
| Sign Up Author Page         | Email Input                 | Allows User to input their Email                                                                | Pass            |
| Sign Up Author Page         | Password Input              | Allows User to input their Password                                                             | Pass            |
| Sign Up Author Page         | Password Input 2            | Allows User to input their Password Again to match First Password Input                         | Pass            |
| Sign Up Author Page         | Sign Up Button              | Allows User to Sign Up to an account if all details = correct                                   | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Account Page                | Display Username            | Displays the Signed In Username                                                                 | Pass            |
| Account Page                | Display Account Type        | Displays the Signed In Account Type (Child, Adult, Author)                                      | Pass            |
| Account Page                | Favourite Genre             | Displays the Favourite Genre based on Users Purchases                                           | Pass            |
| Account Page                | Purchased Book Dropdown     | On click toggles Dropdown                                                                       | Pass            |
| Account Page                | Display Book Title          | Displays Recent Book Title Name Purchased                                                       | Pass            |
| Account Page                | Display Book Price          | Displays Recent Book Price Purchased                                                            | Pass            |
| Account Page                | See Hidden Dropdown         | On click toggles Dropdown                                                                       | Pass            |
| Account Page                | Hidden Authors Dropdown     | On click toggles Dropdown                                                                       | Pass            |
| Account Page                | Hidden Books Dropdown       | On click toggles Dropdown                                                                       | Pass            |
| Account Page                | Display Hidden Books        | Displays all Hidden Books                                                                       | Pass            |
| Account Page                | Hidden Books Unhide Button  | On click Unhides Specific Book                                                                  | Pass            |
| Account Page                | Hidden Topics Dropdown      | On click toggles Dropdown                                                                       | Pass            |
| Account Page                | Display Hidden Topics       | Displays all Hidden Topics                                                                      | Pass            |
| Account Page                | Hidden Topics Unhide Button | On click Unhides Specific Topic                                                                 | Pass            |
| Account Page                | Your Reviews Dropdown       | On click toggles Dropdown                                                                       | Pass            |
| Account Page                | Display Your Reviews        | Displays all Users Reviews                                                                      | Pass            |
| Account Page                | View Review Button          | On click goes to Book Page And Scrolls to Review                                                | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Index Page                  | Generate Shelf and Title    | Generate All Shelves if Book In Genre and Put Genre in Title                                    | Pass            |
| Index Page                  | Shelf Carousel              | If More than 8 Books on Desktop Arrows Appear and Clickable to scroll                           | Pass            |
| Index Page                  | Shelf Carousel              | If More than 4 Books on Tablet Arrows Appear and Clickable to scroll                            | Pass            |
| Index Page                  | Shelf Carousel              | If More than 3 Books on Mobile Arrows Appear and Clickable to scroll                            | Pass            |
| Index Page                  | Display Book Image          | On click goes to Book Slug ID                                                                   | Pass            |
| Index Page - Optimisation   | Changing Resolution         | Changing Resoultion Brings up Optimisation Message and Calculates new Amount of Books on Shelf  | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Search Page                 | Generate Shelf and Title    | Generate All Shelves if Book In Genre and Put Genre in Title                                    | Pass            |
| Search Page                 | Shelf Carousel              | If More than 8 Books on Desktop Arrows Appear and Clickable to scroll                           | Pass            |
| Search Page                 | Shelf Carousel              | If More than 4 Books on Tablet Arrows Appear and Clickable to scroll                            | Pass            |
| Search Page                 | Shelf Carousel              | If More than 3 Books on Mobile Arrows Appear and Clickable to scroll                            | Pass            |
| Search Page                 | Display Book Image          | On click goes to Book Slug ID                                                                   | Pass            |
| Search Page                 | Changing Resolution         | Changing Resoultion Brings up Optimisation Message and Calculates new Amount of Books on Shelf  | Pass            |
| Search Page                 | Search Bar                  | Searching (Titles, Genres, Authors and Topic)                                                   | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Library Page                | Empty Library               | If No User Purchases Show Notification Empty                                                    | Pass            |
| Library Page                | Generate Shelf and Title    | Generate Purchased Books Shelf if User has Purchases                                            | Pass            |
| Library Page                | Shelf Carousel              | If More than 8 Books on Desktop Arrows Appear and Clickable to scroll                           | Pass            |
| Library Page                | Shelf Carousel              | If More than 4 Books on Tablet Arrows Appear and Clickable to scroll                            | Pass            |
| Library Page                | Shelf Carousel              | If More than 3 Books on Mobile Arrows Appear and Clickable to scroll                            | Pass            |
| Library Page                | Display Book Image          | On click goes to Book Slug ID                                                                   | Pass            |
| Library Page                | Changing Resolution         | Changing Resoultion Brings up Optimisation Message and Calculates new Amount of Books on Shelf  | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Book Page                   | Display Book Title          | Displays Book Title                                                                             | Pass            |
| Book Page                   | Wishlist Button             | Adds to Wishlist and Notifies User / If already Purchased wont allow user to add to wishlist    | Pass            |
| Book Page                   | Settings Button             | Opens Setting Window                                                                            | Pass            |
| Book Page                   | Display Book Image          | Displays Book Image                                                                             | Pass            |
| Book Page                   | Display Book Author         | Displays Book Author                                                                            | Pass            |
| Book Page                   | Display Genres              | Displays All Book Genres                                                                        | Pass            |
| Book Page                   | Display Book Pages          | Displays Number Of Book Pages                                                                   | Pass            |
| Book Page                   | Display Rating Numbers      | Displays Books Average As Rating Numbers                                                        | Pass            |
| Book Page                   | Display Rating Stars        | Displays Books Average As Rating Stars                                                          | Pass            |
| Book Page                   | Display About Book          | Displays About Book of Max 490 Characters                                                       | Pass            |
| Book Page                   | Display Book Topics         | Displays All Book Topics                                                                        | Pass            |
| Book Page                   | Purchase Button             | On click adds Book to Users Purchased List and removes wishlist of book if already wishlisted   | Pass            |
| Book Page                   | Shelf and Title             | Shows Shelf with Books of the Same Genre and Topics                                             | Pass            |
| Book Page                   | Shelf Carousel              | If More than 8 Books on Desktop Arrows Appear and Clickable to scroll                           | Pass            |
| Book Page                   | Shelf Carousel              | If More than 4 Books on Tablet Arrows Appear and Clickable to scroll                            | Pass            |
| Book Page                   | Shelf Carousel              | If More than 3 Books on Mobile Arrows Appear and Clickable to scroll                            | Pass            |
| Book Page                   | Display Book Image          | On click goes to Book Slug ID                                                                   | Pass            |
| Book Page                   | Changing Resolution         | Changing Resoultion Brings up Optimisation Message and Calculates new Amount of Books on Shelf  | Pass            |
| Book Page                   | Display Book Image          | On click goes to Book Slug ID                                                                   | Pass            |
| Book Page                   | Display Total Book Reviews  | Displays Total Book Reviews in Numbers                                                          | Pass            |
| Book Page                   | Display Rating Stars        | Displays Books Average As Rating Stars                                                          | Pass            |
| Book Page                   | Create a Review Button      | Only Allows Child/Adult + Only Purchased                                                        | Pass            |
| Book Page                   | Review Title Form           | Allows User to input a Title                                                                    | Pass            |
| Book Page                   | Review Rating Form          | Allows User to input a Rating out of 5 Stars                                                    | Pass            |
| Book Page                   | Review Body Form            | Allows User to input text of the review                                                         | Pass            |
| Book Page                   | Submit Button               | On click submits the Review Form only if all fields are filled                                  | Pass            |
| Book Page                   | Display Reviews             | Displays All Reviews but Keeps the Users Reviews at the top of the list                         | Pass            |
| Book Page                   | Edit Button                 | On click opens Review Form and Inputs All Data                                                  | Pass            |
| Book Page                   | Update Button               | On click submits the new Review Form only if all fields are filled                              | Pass            |
| Book Page                   | Delete Button               | On click opens window showing close button or delete button, going back or deleting the comment | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |
| Book Page - Settings Window | Close Button                | On click closes settings window                                                                 | Pass            |
| Book Page - Settings Window | Hide Book Eye               | On click toggles eye to be visible or hidden                                                    | Pass            |
| Book Page - Settings Window | Generates All Hide Topics   | Displays all Topics of the book with eye icon to click                                          | Pass            |
| Book Page - Settings Window | Hide Topic Eye              | On click toggles eye to be visible or hidden                                                    | Pass            |
| Book Page - Settings Window | Save Changes Button         | On click submits the hide options + goes back to Book Page + Notifies User                      | Pass            |
| \--------------             | \--------------             | \--------------                                                                                 | \-------------- |