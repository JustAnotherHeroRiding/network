
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
-   **Edit Post**: Users should be able to click an “Edit” button or link on any of their own posts to edit that post. #DONE 
	#### Another variable to check, clicking the edit button will set the variable to true and then render the text area prefilled with the text of the body. This will also create the save button, which upon being clicked will set the PUT request on the django side which will change the body of the post
    -   When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a `textarea` where the user can edit the content of their post. #DONE 
    -   The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page. #DONE 
    -   For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts. #DONE 

##### This Should be easy, check if the user has already liked or not then render the appropriate button. like count should be updated with a PUT request to the django back end to update the post's likes in the DB
-   **“Like” and “Unlike”**: Users should be able to click a button or link on any post to toggle whether or not they “like” that post. #DONE 
    -   Using JavaScript, you should asynchronously let the server know to update the like count (as via a call to `fetch`) and then update the post’s like count displayed on the page, without requiring a reload of the entire page. #DONE 

##### Turned out to be not as easy as i thought, needed to add a couple of new use states and api routes to keep track of the liked posts and the liking and unliking


## [Hints](https://cs50.harvard.edu/web/2020/projects/4/network/#hints)

-   For examples of JavaScript `fetch` calls, you may find some of the routes in Project 3 useful to reference.
-   You’ll likely need to create one or more models in `network/models.py` and/or modify the existing `User` model to store the necessary data for your web application.
-   Django’s [Paginator](https://docs.djangoproject.com/en/4.0/topics/pagination/) class may be helpful for implementing pagination on the back-end (in your Python code).
-   Bootstrap’s [Pagination](https://getbootstrap.com/docs/4.4/components/pagination/) features may be helpful for displaying pages on the front-end (in your HTML).


## Alright so the basic requirements are done
### I'm sure many of them will break as i now focus on the design, for a first React project it was fun using useState for everything. The dificulty compared to the mail project was about the same considering i was new with vanilla JS and now i was new with React. I cannot even imagine what it must be like to code this up with vanilla JS
#### Let's add all of these features like likes and editing to the profile component


##### Ok now i need to figure out how to resize the text area when editing posts, i have separated it from the new post text area but resizing does not still work
Right now in the uselayouteffect for the edit text area it is not returning true on the if check which is why it is not resizing, i need to figure out why it works for the new post but not for this one #DONE 
make the sidebar go on top on the smallest screens #DONE 
Get the page buttons to look nicer #DONE 
Add an emoji selector to the new post and edit textareas - I will do this for my final project, working with the cdn has proven to limit me as i cannot import libraries #NextProject
When trying to like a post as a non user, show the user a pop up error message #DONE 
These error messages are clunky, getelementbyid does not work because the div has not yet been rendered by react when i try to find that element #DONE 
For some reason now only the first post is not triggering the transition the others work #FIXED
Fix the profile css
	Lets improve the follow button, maybe top left corner
Make the new post button open a pop up window with the textarea for writing a new post, maybe make it a separate component #DONE 
	Need to add it to profile component also maybe- Nevermind it worked without it as it is outside the showAllPosts if check #DONE 
	Resizing textarea is not working for the popup, same issues as the the edit field i suppose, let's take a closer look at what I did before for the edit field #DONE 
	Cross top right for closing the popup #DONE 
## Need to add a next and previous buttons for the pages as this is in the reqs #DONE 
Lets put two arrows for next and previous page #DONE 
Make background transparent when the popup is active
rounded border for the layout sidebar #DONE

Add error message if trying to make a new post as a non user #DONE 
when the background is dimmed, the back to all posts in the profile view is not dimmed #DONE 
Let's add some comments now to make sense of the code #DONE 
Put the cross in the popup in the right corner and it should peak out a little
