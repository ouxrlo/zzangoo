from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/update/<int:pk>/", views.post_update, name="post_update"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("create/", views.post_create, name="post_create"),
    path("post/delete/<int:pk>/", views.post_delete, name="post_delete"),
    path("<int:post_id>/like/", views.post_like_toggle, name="post_like_toggle"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/comment/", views.create_comment, name="create_comment"),
    path("comment/<int:comment_id>/edit/", views.update_comment, name="update_comment"),
]
