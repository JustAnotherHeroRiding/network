
# Let's make django render the react project
### Will use React cdn as rendering the vite project will not use the django network app
#### Vite + Django for final project


Using Python, JavaScript, HTML, and CSS, complete the implementation of a social network that allows users to make posts, follow other users, and “like” posts. You must fulfill the following requirements:

**New Post**: Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post. #DONE 
- The screenshot at the top of this specification shows the “New Post” box at the top of the “All Posts” page. You may choose to do this as well, or you may make the “New Post” feature a separate page. #DONE 
**All Posts**: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first. #DONE 
### The likes are currently a manytomany field. Needs more work in order to display them.
#### Never mind they are still being passed in the serialize method()
- Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later). #DONE 

## I will need a django view to pull up all posts for a user
###### Current problem in the React code is that i'm not passing the data from the post.user but from the logged in user
##### Let's make the profile page a separate page instead of a single page, i can pass the user id from the posts and render the component there.
**Profile Page**: Clicking on a username should load that user’s profile page. This page should: #DONE 
#### Need to add followers and following to the user model
- Display the number of followers the user has, as well as the number of people that the user follows. #DONE 
- Display all of the posts for that user, in reverse chronological order. #DONE 
#### Let's try and do this with django
#### What if i just pass true if the user is already following from the follow/user_id view, if its true then the user is following and the button will be unfollow
- For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.  #DONE 

### Let's think how would i implement this. Maybe another state check for ShowFollowing, if yes then load all posts from users that are being follewed by current_user_id
#### This means that in the posts compoment it will be an if elif elif etc statement that decides what to render instead of the current binary check. I will maybe also need a showProfile state.
##### Or maybe if showPosts is true, check if ShowFollowing or showAllPosts, so two more variables within the show posts, or just check for ShowFollowing then make a GET request for all posts from users that the logged in user is following
-   **Following**: The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows. #DONE 
    -   This page should behave just as the “All Posts” page does, just with a more limited set of posts. #DONE 
    -   This page should only be available to users who are signed in. #DONE 
-   **Pagination**: On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well. #DONE 
    -   See the **Hints** section for some suggestions on how to implement this. #DONE 
-   **Edit Post**: Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
	#### Another variable to check, clicking the edit button will set the variable to true and then render the text area prefilled with the text of the body. This will also create the save button, which upon being clicked will set the PUT request on the django side which will change the body of the post
    -   When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a `textarea` where the user can edit the content of their post.
    -   The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.
    -   For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.

##### This Should be easy, check if the user has already liked or not then render the appropriate button. like count should be updated with a PUT request to the django back end to update the post's likes in the DB
-   **“Like” and “Unlike”**: Users should be able to click a button or link on any post to toggle whether or not they “like” that post. #DONE 
    -   Using JavaScript, you should asynchronously let the server know to update the like count (as via a call to `fetch`) and then update the post’s like count displayed on the page, without requiring a reload of the entire page. #DONE 

##### Turned out to be not as easy as i thought, needed to add a couple of new use states and api routes to keep track of the liked posts and the liking and unliking


## [Hints](https://cs50.harvard.edu/web/2020/projects/4/network/#hints)

-   For examples of JavaScript `fetch` calls, you may find some of the routes in Project 3 useful to reference.
-   You’ll likely need to create one or more models in `network/models.py` and/or modify the existing `User` model to store the necessary data for your web application.
-   Django’s [Paginator](https://docs.djangoproject.com/en/4.0/topics/pagination/) class may be helpful for implementing pagination on the back-end (in your Python code).
-   Bootstrap’s [Pagination](https://getbootstrap.com/docs/4.4/components/pagination/) features may be helpful for displaying pages on the front-end (in your HTML).