---

---

- 安装

```
pip3 install Django-2.x
```



- 创建工程

```
django-admin startproject 项目名称
```



- Django项目基本结构

![img](/Users/z_mac/Library/Application Support/typora-user-images/image-20181223142346125.tiff)



- 响应请求

  ![img](/Users/z_mac/Library/Application Support/typora-user-images/image-20181223142315021.tiff)


- 启动本地服务

- ```
  首先执行数据库迁移：python manage.py migrate
  然后再启动服务：python manager.py runserver
  ```



- 创建超级管理员

- ```
  python manage.py createsuperuser
  ```



- 创建模型

- ```
  python manage.py startapp 模型名称
  ```



- 同步数据库，修改模型也需要更新数据库

  先在setting.py里的INSTALLED_APPS注册应用,然后在models.py里面创建模块类，再将该模块类注册到admin.py里面(admin.site.regiester(模块类))

- ```
  制造迁移：python manage.py makemigrations
  迁移：python manage.py migrate
  ```



- 设置中文面版，上海时区(setting.py)

- ```
  LANGUAGE_CODE = 'zh-Hans'
  TIME_ZONE = 'Asia/Shanghai'
  ```



- Objects:模型的objects是获取或操作模型的对象

- ```
  模型类名.objects.get(条件)
  模型类名.objects.all()
  模型类名.objects.filter(条件)
  ```
