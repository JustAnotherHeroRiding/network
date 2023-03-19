
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    
    path("post/send", views.send_post, name='sendpost'),
    path("post/all", views.get_all_posts, name='all_posts'),
    path('check/login', views.check_login, name='check_login'),
    path('post/<int:user_id>', views.get_user_posts, name='user_posts'),
    path('post/user/following', views.get_following_posts, name='posts_following'),
    
    path('post/like/<int:post_id>', views.add_like, name='like_post'),
    path('post/unlike/<int:post_id>', views.remove_like, name='unlike_post'),
    path('user/likes', views.liked_posts, name='liked_posts'),
    
    
    path('user/follow/<int:user_id>', views.follow, name='follow'),
    path('user/unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    path('user/followers/<int:user_id>', views.get_follow_counts, name='followers'),
    path('user/is_following/<int:user_id>', views.is_following, name='check_following')
]
