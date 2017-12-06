from django.contrib.sitemaps import Sitemap
from .models import Post
###要创建一个站点地图，只需写一个 Sitemap类并指向你的 URLconf。主urls设置url
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.publish