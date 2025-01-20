from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post


def post_list(request):
    post = Post.objects.all()
    paginator = Paginator(post, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/post_list.html", {"page_obj": page_obj})
