from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailPostForm, CommentForm, PostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def post_list(request, tag_slug=None):    
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    paginator =Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', { 'page':page, 'posts':posts, 'tag':tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published', 
                                    publish__year=year, 
                                    publish__month=month, 
                                    publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.owner = request.user
                new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similiar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similiar_posts = similiar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',{'post':post, 'comments':comments, 
                        'new_comment': new_comment, 'comment_form': comment_form,
                        'similiar_posts':similiar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n " \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'mehedi.hassan202111@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post, 'form':form, 'sent':sent})

def postCreate(request):
    new_post = None
    if request.user.groups.filter(name='Instructors'):
        if request.method == 'POST':
            form = PostForm(data=request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
            return HttpResponseRedirect(new_post.get_absolute_url())
        else:
            form = PostForm()
    else:
        return HttpResponseRedirect(reverse('blog:post_list'))
    return render(request, 'blog/post/create_post.html', {'form':form})

def postEdit(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(instance=post, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            form = PostForm(instance=post)
    else:
        return HttpResponseRedirect(reverse('blog:post_list'))
    return render(request, 'blog/post/edit_post.html', {'form':form, 'post':post })
        
def InstructorPosts(request):
    if request.user.groups.filter(name='Instructors'):
        user = request.user
        all_posts = Post.objects.filter(author=user)
        return render(request, 'blog/post/instructor_posts.html', {'all_posts':all_posts})
    else:
        return HttpResponseRedirect('/articles')

def postDelete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return HttpResponseRedirect('/articles/my-articles')
        return render(request, 'blog/post/delete_post.html', {'post':post})
    return HttpResponseRedirect('/articles')

def post_search(request):
    query = request.GET.get('search')
    results = []
    
    if query:
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    return render(request, 'blog/post/search.html', {'query':query, 'results':results})