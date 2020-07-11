import datetime

from django.shortcuts import render, render_to_response, redirect, reverse

# Create your views here.
from base.models import *
from base.forms import CommentForm
from django.http import Http404


def get_blogs(request):

    blogs = Blog.objects.all().order_by('-created')
    return render_to_response('blog_list.html', {'blogs': blogs})


def get_details(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cleaned_data['blog'] = blog
        Comment.objects.create(**cleaned_data)
    ctx = {
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-created'),
        'form': form
    }
    return render(request, 'blog_details.html', ctx)

def send_blog(request):

    if request.method == "GET":
        catagorys = Catagory.objects.all()
        tags = Tag.objects.all()
        ctx = {
            'catagorys':catagorys,
            'tags':tags
        }
        return render(request,'send_blog.html',ctx)
    elif request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        created = datetime.datetime.now()
        catagory = request.POST.get('catagory')
        tags = request.POST.get('tags')
        blog = Blog(
            title=title,
            author=author,
            content=content,
            created=created,
            catagory=Catagory.objects.get(id=catagory),
            tags=int(tags)
        )
        blog.save()
        return redirect(reverse('all_blogs'))
