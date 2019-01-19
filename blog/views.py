# Create your views here.
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from blog.models import Blog, BlogType
from mysite import settings
# from user.forms import LoginForm
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blog_all_list):
    context = {}
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10篇进行分页
    page_num = request.GET.get('page', 1)  # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    cur_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码的前后两页
    page_range = list(filter(lambda x: 0 < x < paginator.num_pages, range(cur_page_num - 2, cur_page_num + 3)))
    # 加上省略页码标记
    if page_range:
        # 加上省略页码标记
        if page_range[0] - 1 >= 2:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append('...')
        # 加上首页和尾页
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)
    else:
        page_range.append(1)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context["blogs"] = page_of_blogs.object_list
    context["page_of_blogs"] = page_of_blogs
    context["blog_types"] = BlogType.objects.annotate(blog_count=Count('blog'))  # 获取博客分类的对应博客数量
    context["page_range"] = page_range
    context["blog_dates"] = blog_dates_dict
    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blog_all_list)
    return render(request, "blog/blog_list.html", context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blog_all_list)
    context["blog_type"] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    # blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)

    context["blog"] = blog
    context["previous_blog"] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 获取当前博客的上一条博客
    context["next_blog"] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取当前博客的下一条博客
    # context["login_form"] = LoginForm()
    # context['comments'] = comments.order_by('-comment_time')
    # context['comment_count'] = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count()
    # context['comment_form'] = CommentForm(
    #     initial={'content_type': blog_content_type.model, 'object_id': blog_pk, 'reply_comment_id': 0})
    response = render(request, "blog/blog_detail.html", context)  # 用render会有user字段
    # context['user'] = request.user
    # response = render_to_response("blog/blog_detail.html", context)
    response.set_cookie(read_cookie_key, 'true', max_age=60)  # 阅读cookie标记
    return response
