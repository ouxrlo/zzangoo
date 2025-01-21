from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("post/update/<int:pk>/", views.post_update, name="post_update"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("create/", views.post_create, name="post_create"),
    path("post/delete/<int:pk>/", views.post_delete, name="post_delete"),
]
