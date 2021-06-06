from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, Comment
from .forms import Post_form, Comment_form
from cuser.models import User

def greet(request):
    return HttpResponse("Hello World")

@login_required
def new_post(request):
    if request.method == "POST":
        form = Post_form(request.POST, request.FILES)
        if form.is_bound:
            if form.is_valid():
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                img = form.cleaned_data.get('img')
                user = User.objects.get(id = request.user.id)
                Post.objects.create(user = user, title=title, description=description, img=img)
                form = Post_form()
                messages.info(request, 'post created successfully.')
            else:
                return HttpResponse('form is invalid.')
        else:
            return HttpResponse('form is not bounded.') 
    else:
        form = Post_form()
    
    return render(request, 'post/newpost.html', {'form': form})

@login_required
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'post/post_list.html', {'data': posts})

@login_required
def post_details(request, postid):
    post = Post.objects.get(id = postid)
    if request.method == 'GET':
        user = User.objects.get(email = post.user)
        comments = post.comment_post.filter(parent__isnull = True)
        commentform = Comment_form()
        print('#######################Comments###########################')
        print(comments)
        print('##########################################################')
        print('Post user: ', user)
        return render(request, 'post/post_details.html', {'post': post, 'user_obj': user, 'comments':comments, 'commentform':commentform})
    
    elif request.is_ajax():
        if request.method == 'POST':
            print('ajax user:', request.user)
            user_obj = User.objects.get(id = request.user.id)
            print('User object is: ', user_obj)
            form = Comment_form(request.POST)
            if form.is_bound:
                if form.is_valid():
                    
                    try:
                        comment_id = int(request.POST.get('parent_id'))
                    except:
                        comment_id = None

                    if comment_id:
                        parent_comment = Comment.objects.get(id=comment_id)
                        if parent_comment:
                            comm = form.cleaned_data.get('comment_text')
                            print('Comment is: ', comm)
                            Comment.objects.create(comment_text=comm, post=post, user=user_obj, parent=parent_comment)
                            # replies = post.comment_post.all().exclude(parent__isnull = True).filter(parent_id = parent_comment.id)
                            # commentform = Comment_form()
                            # html = render_to_string('post/comments.html', {'comments':replies, 'commentform':commentform}, request=request)
                            # return JsonResponse({'form': html})
                            
                    else:
                        parent_comment = None
                        comm = form.cleaned_data.get('comment_text')
                        print('Comment is: ', comm)
                        Comment.objects.create(comment_text=comm, post=post, user=user_obj, parent=parent_comment)
                    comments = post.comment_post.filter(parent__isnull = True)
                    commentform = Comment_form()
                    html = render_to_string('post/comments.html', {'comments':comments, 'commentform':commentform}, request=request)
                    return JsonResponse({'form': html})
                else:
                    return HttpResponse('form is invalid')
            else:
                return HttpResponse('form not bound')
    
    # elif request.method == 'POST':
    #     comm = request.POST.get('comment_input')
    #     comment = Comment.objects.create(comment_text=comm, post=Post.objects.get(id = postid))
    #     # return redirect('post-detail', postid=postid)
    
def like_comment(request):
    if request.is_ajax():
        if request.method == 'POST':
            print('ajax user:', request.user)
            user_obj = User.objects.get(id = request.user.id)
            print('User object is: ', user_obj)

            comment_id = request.POST.get('comment-id')
            comment = Comment.objects.get(id = comment_id)
            print('comment is: ', comment)
            liked = None
            if request.user in comment.liked.all():
                comment.liked.remove(request.user)
                liked = False
            else:
                comment.liked.add(request.user)
                liked = True
            return JsonResponse({'liked':liked})