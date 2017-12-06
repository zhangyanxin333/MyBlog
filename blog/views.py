from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from .forms import CommentForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count
# Create your views here.
####视图带有一个可选的tag_slug参数默认为none
def post_list(request,tag_slug=None):
    ####获取对象将其分页,每页展示多少内容和有多少页
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        #####用给定的slug来获取标签对象
        tag = get_object_or_404(Tag,slug=tag_slug)
        ######过滤所有帖子只留下给定标签的帖子
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list,5)
    page = request.GET.get('page')
    try:
        ###通过paginator的page方法在期望的页面中获取对象
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'page': page,'tag': tag}
    return render(request,'blog/post_list.html',context)
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    #####获取所有有效评论并
    comments = post.comments.filter(activate=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        ####如果评论有效生成新的评论但不保存倒数据库
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            ##我们为我们刚创建的帖子分配一个评论
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
        ####values_list() 查询集返回包含给定的字段值的元祖。
        ## 我们传给元祖flat=True来获取一个简单的列表类似[1,2,3,...]。
        post_tags_ids = post.tags.values_list('id',flat=True)
        similar_posts =Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts =similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    context ={'post': post,'comments':comments,'comment_form':comment_form,
              'new_comment':new_comment,'similar_posts':similar_posts}

    return render(request,
                  'blog/post_detail.html',
                  context)
####使post_list视图转变为一个基于类的视图
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'






