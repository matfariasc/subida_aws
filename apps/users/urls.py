from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index , name='index_login'),
    path('signin', views.signin, name="signin_view"),
    path('register', views.register, name="register_view"),
    path('logout', views.log_out, name="log_out"),
    path('users/edit', views.user_edit, name="user_edit"),
    path('users/edit/info', views.update_info, name="user_update_info"),
    path('users/edit/password', views.update_password, name="user_update_password"),
    path('users/edit/desc', views.update_desc, name="user_update_desc"),
    path('users/<int:user_id>/delete', views.remove_user, name="user_remove"),
    path('users/edit/<int:user_id>', views.edit_user_info, name="admin_user_edit"),
    path('users/edit/<int:user_id>/password', views.admin_update_password, name="admin_update_password"),
    path('users/new', views.new_user, name="user_new"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('users/show/<int:user_id>', views.user_view, name="user_view"),
    path('users/show/<int:user_id>/message', views.message_new, name="message_new"),
    path('users/show/new/comment', views.comment_new, name="comment_new"),
]
