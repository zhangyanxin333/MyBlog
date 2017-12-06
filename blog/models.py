from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
##这个管理器允许你对post对象添加获取删除标签
from taggit.managers import TaggableManager
# Create your models here.

####定义管理器方法是Django自带的
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=200)
####   重点slug看似没用但是他将来将会在URL中使用url的帖子返回一个相对地址
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    #####管理器objects 为默认的,published为我们创建的这样我们就可以用published管理器了
    ###Post.published.filter而不是post.objects
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
#####创建一个评论系统
class Comment(models.Model):
    name = models.CharField(max_length=25)
    body = models.TextField()
    post = models.ForeignKey(Post,related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    ###用来自动过滤不好的评论
    activate = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)