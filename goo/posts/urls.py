from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/update/<int:pk>/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/delete/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("<int:pk>/like/", views.PostLikeToggleView.as_view(), name="post_like_toggle"),
    path("post/<int:pk>/comment/", views.create_comment, name="create_comment"),
    path(
        "post/<int:pk>/comments/", views.CommentListView.as_view(), name="comment_list"
    ),  # 수정
    path("comment/<int:comment_id>/edit/", views.update_comment, name="update_comment"),
    path(
        "comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
]
