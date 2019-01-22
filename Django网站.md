- 如何用Django开发网站

  ![img](/Users/z_mac/Library/Application Support/typora-user-images/image-20181224160102531.tiff)



- 步骤

  ![img](/Users/z_mac/Library/Application Support/typora-user-images/image-20181224173406822.tiff)



- 网站的功能模块=》Django App

  - 博客：博文，博客分类，博客标签
  - 评论
  - 点赞
  - 阅读
  - 用户：第三方登陆




- 创建虚拟环境

  - 避免多个项目之间python库的冲突

  - 完整便捷导出python库的列表

  - ```
    下载：pip install virtualenv
    创建：virtualenv(python3 -m venv) 虚拟环境名称
    启动：Scripts\activate(source activate)
    退出：deactivate
    ```




- pip一键导出和安装

  ```
  pip freze > requirements.txt
  pip install -r  requirements.txt
  ```




- 常用模版标签

  ```
  循环：for
  条件：if（可逻辑判断）, ifequal, ifnotequal
  链接：url
  模版嵌套：block, extends, indlude
  注释：{# #}
  ```




- 常用的过滤器

  ```
  日期：date
  字数截取：truncatechars, truncatechars_html, 
  		truncatewords, truncatewords_html
  是否信任：safe
  长度：length
  ```



- 打开shell模式

- ```
  python manage.py shell
  ```



- shell下保存到数据库

- ```
  对象名.save()
  ```


- Django分页器的使用

  ![img](/Users/z_mac/Library/Application Support/typora-user-images/image-20181228110348134.tiff)



- filter筛选条件, exclude排除条件

  ```
  大于：__gt(greater than)
  大于等于：__gte
  小于：__lt(less than)
  小于等于：__lte
  包含：__contains(__icontains忽略大小写)
  开头是：__startswith
  结尾是：__endswith
  其中之一：__in
  范围：__range
  ```



- 富文本编辑器

- ```
  1.安装
  	pip install django-ckeditor
  2.注册应用（settings.py）
  	'ckeditor'
  3.配置model
  	把字段改成RichTextField
  	models.TextField()  -->  RichTextField()
  ```



- 过滤标签

- ```
  |striptags
  ```




- 上传图片

- ```python
  1.安装
  	pip install pillow
  2.注册应用
  	'ckeditor_uploader'
  3.配置setting.py
  	# 配置media
  	MEDIA_URL = '/media/'
  	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  	# 配置ckeditor
  	CKEDITOR_UPLOAD_PATH = 'upload/'
  4.配置url.py
  	path('cheditor', include('ckeditor_uploader.urls'))
  	urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
  5.配置model
  	把字段改成RichTextUploadingField
  ```



- 统计阅读数

  ```python
  1.创建阅读统计app
  	python manage.py startapp read_statistics
  2.创建ReadNum模型类
  	read_num = models.IntegerField(default=0)
      content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
      object_id = models.PositiveIntegerField()
      content_object = GenericForeignKey('content_type', 'object_id')
  3.注册ReadNumAdmin
  	@admin.register(ReadNum)
  	class ReadNumAdmin(admin.ModelAdmin):
      	list_display = ('read_num', 'content_object')
  4.创建阅读计数扩展方法
  	class ReadNumExpendMethod(object):
      def get_read_num(self):
          try:
              ct = ContentType.objects.get_for_model(self)
              read_num_object = ReadNum.objects.get(content_type=ct, object_id=self.pk)
              return read_num_object.read_num
          except exceptions.ObjectDoesNotExist:
              return 0
  5.新建utils.py
  	from django.contrib.contenttypes.models import ContentType
  	from .models import ReadNum
      def read_statistics_once_read(request, obj):
          ct = ContentType.objects.get_for_model(obj)
          key = "%s_%s_read" % (ct.model, obj.pk)
          if not request.COOKIES.get(key):
              if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
                  # 存在记录
                  read_num_object = ReadNum.objects.get(content_type=ct,		  															  object_id=obj.pk
              else:
                  # 不存在对应的记录
                  read_num_object = ReadNum(content_type=ct, object_id=obj.pk)
              # 或者
              #read_num_object, created= ReadNum.objects.get_or_create(content_type=ct，								object_id=obj.pk)		                          
              # 计数+1
              read_num_object.read_num += 1
              read_num_object.save()
          return key
  
  ```



- 应用缓存

  ```
  1.配置setting.py
  	CACHES = {
          'default':{
             'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
              'LOCATION': 'my_cache_table',
          }
      }
  2.创建缓存表
  	python manage.py createcachetable
  3.获取七天热门博客的缓存数据
      hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
      if hot_blogs_for_7_days is None:
          hot_blog_for_7_days = get_7_days_hot_blogs()
          cache.set('hot_blogs_for_7_days', hot_blog_for_7_days, 3600)
  ```




- 返回当前页面

- ```
  referer = request.META.get('HTTP_REFERER', reverse('找不到时返回的指定页面'))
  render(request, 'error.html')
  ```




- Django Form的作用

- ```
  Django用Form类描述html表单，帮助或简化操作
  1.接收和处理用户提交的数据
    可检查提交的数据
    可将数据转换成python的数据类型
  2.可自动生成html代码
  ```




- Django Form的使用

- ```
  创建forms.py
  字段 ->html input标签
  每个字段类型都有一个适当的默认的Widget类
  
  from django import forms
  class NameForm(forms.Form):
  	your_name = forms.CharField(label='Your name', max_length=100)
  ```



- 自定义模板标签

  降低耦合，代码更加独立和使用更加简单

  ```
  在app内创建templatetags包
  创建py文件
  load标签加载该文件
  ```

  

- 级联删除

- ```
  DO_NOTHING --> CASCADE
  保证数据完整性
  ```



- 前后端开发建议

- ```
  功能需求分析-->模型设计-->前端初步开发-->后段实现-->完善前端代码
  ```

  

- 继承Django用户模型

- ```
  方法：
  	1.自定义模型继承AbstractUser
  	2.配置settings的AUTH_USER_MODEL
  使用：
  	1.外键关联settings.AUTH_USER_MODEL
  	2.用get_user_model的方法获取User模型
  ```

  ```
  优点：
  	1.自定义强
  	2.没有不必要的字段（需要继承AbstractBaseUser）
  缺点：
  	1.需要删库重来或者要项目一开始就使用
  	2.配置admin麻烦
  ```

  

- 新的模型拓展

- ```
  方法：
  	1.创建自定义模型
  	2.外键关联User
  ```

  ```
  优点：
  	1.使用方便
  	2.不用删库重来影响整体构架
  缺点：
  	1.存在不必要的字段
  	2.对比继承的方法，查询速度稍稍慢一丁点
  ```

  **admin.py**

  ```
  from django.contrib import admin
  from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
  from django.contrib.auth.models import User
  from .models import Profile
  
  
  class ProfileInline(admin.StackedInline):
      model = Profile
      can_delete = False
  
  
  class UserAdmin(BaseUserAdmin):
      inlines = (ProfileInline,)
      list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')
  
      def nickname(self, obj):
          return obj.profile.nickname
  
      nickname.short_description = '昵称'
  
  
  # Re-register UserAdmin
  admin.site.unregister(User)
  admin.site.register(User, UserAdmin)
  
  
  @admin.register(Profile)
  class ProfileAdmin(admin.ModelAdmin):
      list_display = ('user', 'nickname')
  
  ```

  **models.py**

  ```
  from django.db import models
  from django.contrib.auth.models import User
  
  
  class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="昵称")
      nickname = models.CharField(max_length=20)
  
      def __str__(self):
          return '<Profile>: %s for %s' % (self.nickname, self.user.username)
  ```

  

- Django邮箱配置

  ```
  # 发送邮件设置
  # https://docs.djangoproject.com/en/2.0/ref/settings/#email
  # https://docs.djangoproject.com/en/2.0/topics/email/
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.qq.com'
  EMAIL_PORT = 25
  EMAIL_HOST_USER = '2307451983@qq.com'
  EMAIL_HOST_PASSWORD = 'hfzmpqtjqhrkdifi'  # 授权码，qq邮箱设置后给的
  EMAIL_SUBJECT_PREFIX = '[vous的博客] '
  EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)
  ```



- git使用

- ```
  初步使用
      1.进入github，然后点击 Start a project，按提示进行下一步操作
      2.创建了repository后点击Clone or download,复制url
      3.下载代码:git clone 刚刚复制的url（https://github.com/vous111/test.git）
      4.将要上传的文件复制到刚刚下载的文件夹里面
      5.创建.gitignore文件，可将不想上传的文件或文件夹写到里面
      6.添加代码到缓存区:git add .(前提是处于该git文件下)
      7.提交代码:git commit -m “描述”
      8.将代码上传到github上面:git push
  其他命令
  	1.将github上最新的代码更新到本地:git pull
  	2.查看状态: git status
  	3.删除文件或文件夹:
  		git rm 文件 //本地中该文件会被删除
  		git rm --cached 文件 //本地中该文件不会被删除
  		git rm -r 文件夹 //删除文件夹
  		git rm -r  --cached  文件夹 //删除文件夹
  ```



- 将mysql路径加入环境变量

  ```
  mac:
  	1.打开终端,输入： cd ~
      2.然后输入：touch .bash_profile
      3.再输入：open -e .bash_profile
      4.在里面输入:export PATH=${PATH}:/usr/local/mysql/bin,保存退出
  windows:
  	1.复制bin绝对地址
  	2.进入系统属性-高级-环境变量
  	3在变量名为path中的最后加入 ;bin的路径,确定即可
  ```

  

- Django中使用mysql

- ```
  1.创建数据库:create database mysite_db default charset=utf8mb4 default collate utf8mb4_unicode_ci;;
  2.创建用户: create user 'vous'@'localhost' identified by 'vous123456';
  3.给vous用户授权mysite_db数据库权限:grant all privileges on mysite_db.* to 'vous'@'localhost';
  4.刷新系统权限表:flush privileges;
  5.退出mysql用vous登录:mysql -u vous -p;
  6.修改settings.py中DATABASES
  	DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'mysite_db',
              'USER': 'vous',
              'PASSWORD': 'vous123456',
              'HOST': 'localhost',
              'POST': '3306',
          }
      }
  7.安装mysqlclient:pip install mysqlclient(如果存在python2，要用pip3);
  	windows下,https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient下载对应版本的whl		包，然后pip install 下载的whl包名
  8.应用迁移文件:python manage.py migrate
  9.生成缓存表:python manage.py createcachetable
  10.将原来sqlite3数据库迁移到mysql
  	导出命令:python manage.py dumpdata > data.json(将settings.py中DATABASES换回sqlite3)
  	倒入命令:python manage.py loaddata data.json(将settings.py中DATABASES换回mysql)
  	如果因为数据库原因报错，直接删除报错的表
  11.mysql时区支持问题，需要使用mysql_tzinfo_to_sql将时区表加载到mysql数据库中
  	mac/linux: mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u -p root mysql
  	windows: 1.在https://dev.mysql.com/downloads/timezones.html下载timezone_posix.sql
  			 2.在timezone_posix.sql下载目录打开cmd输入mysql -u root -p mysql < 							timezone_posix.sql
  
  ```

  