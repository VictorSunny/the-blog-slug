from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from . forms import BlogForm, edit_blogForm, CommentForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .trendcatcher import datafetcher
from .models import UserBlog, Comment, Notifications, Category
from .custom_functions import notification_cleanser



# Create your views here.

from .new import dict
#Import custom authentication user model and assign to variable 'User'
User = get_user_model()

# Home view for retrieving and displaying constantly updating news article headlines source from
# aa reputable local news website known as the punch nigeria using a webscraping the datafetcher module
def home_view(request):
    # article_dict = datafetcher()
    article_dict = dict
    page = request.GET.get('p')

    paginator_class = Paginator(article_dict, 10)
    article_dict = paginator_class.get_page(page)

    return render(request, "index.html", {"article_dict": article_dict})

    
# view for creating blog articles
@login_required()
def create_blog_view(request):

    if request.method == 'POST':

        #retrieve form data and save if data is acceptable
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit= False)
            blog.author = request.user
            blog.save()

            #send new post notications to all followers of the poster
            for follower in blog.author.followers.all():
                body= f"new post from {blog.author.username}: {blog.headline[:20]}..."

                alert = Notifications.objects.create(
                    owner= follower,
                    blog= blog,
                    label= f'new post',
                    body= body,
                    connected_account= blog.author
                )
                alert.save()

            #redirect to blog page after saving
            return redirect("core:blog", blog.pk)
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {"form": form})

#view for editing blog
@login_required()
def edit_blog_view(request, pk):

    #retrieve blog for editing
    blog = get_object_or_404(UserBlog, pk=pk, author= request.user)

    initial_headline = blog.headline
    initial_body = blog.body

    if request.method == 'POST':
        form = edit_blogForm(request.POST, instance= blog)
        if form.is_valid():

            updated_headline = form.cleaned_data["headline"]
            updated_body = form.cleaned_data["body"]

            #save changes only if the request user is the author of the article
            #raise permission error is request user is not the author of the article
            if request.user.id == blog.author.id:

                if updated_headline == initial_headline or updated_body == initial_body:
                    form.add_error("body", "No changes detected")
                else:
                    form.save()
                    return redirect("core:blog", blog.pk)
            else:
                return HttpResponseForbidden("access forbidden")
    else:
        form = edit_blogForm(initial={'headline': blog.headline, 'body': blog.body})

    return render(request, 'edit_blog.html', {"form": form})


# view for fully viewing an article
def blog_view(request, pk):
    blog = get_object_or_404(UserBlog, id= pk)

    all_comments = blog.comments.all()

    #get page number for comments
    comment_page = request.GET.get("cp")

    paginator_class = Paginator(all_comments, 4)

    all_comments = paginator_class.get_page(comment_page)

    #post method for handling user comment posting
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():

            #save comment only if user is logged in
            if request.user.is_authenticated:
                comment = form.save(commit= False)
                comment.author = request.user
                comment.blog = blog
                comment.save()

                #send notication to book creator if comment is not by book creator and notifications are allowed for book
                if blog.alerts:
                    if request.user != blog.author:
                        if blog.alerts:
                            unparsed_body= f"new comment from {request.user.username}: {str(blog.headline[:10]) + '...'}"

                            body = notification_cleanser(blog.author.id, unparsed_body)
                            alert = Notifications.objects.create(
                                owner= blog.author,
                                blog= blog,
                                label= f'new comment from {request.user.username}',
                                body= body,
                                connected_account = request.user,
                            )
                            alert.save()
            else:
                return HttpResponseForbidden("access forbidden")
            
        return redirect(request.path)
    else:
        form = CommentForm()

    return render(request, 'blog_page.html', {'blog': blog, 'form': form, 'comments': all_comments})

#view for retrieving and displaying all blogs posted by users
#allows filtering by category
def all_blogs_view(request):

    #retrieve all blogs
    all_blogs = UserBlog.objects.all()
    #retrive all categories for filtering
    blog_categories = Category.objects.all()

    #retrieve url parameters for filtering and pagination
    category_filter = request.GET.get("cat")
    page = request.GET.get("p")

    if category_filter:
        all_blogs = all_blogs.filter(category__slug= category_filter)
    
    paginator_class = Paginator(all_blogs, 8)
    all_blogs = paginator_class.get_page(page)

    return render(request, "all_blogs.html", {'all_blogs': all_blogs, 'categories': blog_categories, 'category_filter': category_filter, 'page_title': 'Blogs By Users'})

#view for retrieving and displaying blogs that have been bookmarked by user
def bookmarked_blogs_view(request):
    all_blogs = request.user.bookmarks.all()
    blog_categories = Category.objects.all()

    category = request.GET.get("category")
    page = request.GET.get("p")

    if category:
        all_blogs = all_blogs.filter(category__slug= category)
    
    paginator_class = Paginator(all_blogs, 3)
    all_blogs = paginator_class.get_page(page)

    return render(request, "all_blogs.html", {'all_blogs': all_blogs, 'categories': blog_categories, 'page_title': 'Your Bookmarks'})

#view for confirming delete action for blog
@login_required()
def confirm_delete_view(request, blog_id):
    return render(request, "delete.html", {"blog_id": blog_id})
 

#view for deleting blog after confirmation
@login_required()
def delete_view(request, blog_id):
    
    #try to retrieve blog and delete if the user is the blog's author
    #redirect to all_blogs page if blog has already been deleted instead of raising an error
    try:
        blog = UserBlog.objects.get(id= blog_id)

        if request.user == blog.author:
            blog.delete()
        else:
            return HttpResponseForbidden({"message": "you are not authorized to delete this post"})
        
        return redirect("authapp:profile", blog.author.username)
    
    except:
        return redirect("authapp:profile", request.user.username)

#view for deleting comment from blog
@login_required()
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, id= pk)
    blog_id = comment.blog.id
    if request.user == comment.author:
        comment.delete()
    else:
        return HttpResponseForbidden({"message": "forbidden. you do not have permissions to carry out this action"})
    return redirect("core:blog", blog_id)

#view for bookmarking blogs for later read
@login_required()
def bookmark_view(request, blog_id):

    prev_page = request.META.get("HTTP_REFERER", "/")

    blog = get_object_or_404(UserBlog, id= blog_id)

    #bookmark blog if it has not been bookmarked by user
    #remove blog from user's bookmarks if it has already been bookmarked
    if request.user in blog.bookmarkers.all():
        blog.bookmarkers.remove(request.user)
        print("unsaved")
    else:
        blog.bookmarkers.add(request.user)
        print("saved")

    return redirect(prev_page)

@login_required()
def blog_alert_view(request, blog_id):
    
    prev_page = request.META.get("HTTP_REFERER", "/")

    blog = UserBlog.objects.get(id= blog_id)

    #reset state of notifications to opposite of it's current state if book is owned by user
    if request.user.id == blog.author.id:
        print('user can access notification settings')
        if blog.alerts:
            blog.alerts = False
            blog.save()
        else:
            blog.alerts = True
            blog.save()
    else:
        return HttpResponseForbidden({"message": "forbidden. you do not have permissions to carry out this action"})
    
    return redirect(prev_page)