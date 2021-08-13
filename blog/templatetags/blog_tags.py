from django import template
from ..models import Post
from taggit.models import Tag
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe
import calendar

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.filter()
def month_name(value):
    return calendar.month_abbr[value]

@register.filter()
def total_comments(post):
    comments = post.comments.filter(active=True)
    return comments.count()

@register.simple_tag
def all_tags():
    return Tag.objects.all()