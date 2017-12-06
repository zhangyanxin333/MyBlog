from django import template
register = template.Library()
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
@register.simple_tag
def total_posts():
    return Post.published.count()
##注册模版标签必须传入要注册的模版
@register.inclusion_tag('blog/post_latest_posts.html')
####count=5意思是默认值是五
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}
@register.assignment_tag
def get_most_commented_posts(count=5):
    ###annocate函数
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))