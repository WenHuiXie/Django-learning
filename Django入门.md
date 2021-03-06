Django入门
============

Django的结构
---------

Django使用Python写的web框架。

Django 中比较重要文件介绍：

 - urls.py 网址入口，关联对应的views.py 中的一个函数，访问网址就对应一个函数。
 - views.py ：处理用户发出的请求，从urls.py中对应过来，通过渲染templates中的网页可以将显示内容输出到网页。
 - models.py：与数据库操作相关，存入或读取数据时用到这个
 - forms.py ：表单，用户在浏览器上输入数据提交，对数据的验证与输入框的生成工作
 - templates 文件夹：views.py 中函数渲染的templates中的html模板，得到动态内容的网页，当然可以用缓存来提高速度。
 - admin.py ：后台，可以用很少的代码就拥有一个强大的后台。
 - settings.py：Django的设置，配置文件，比如DEBUG的开关，静态文件位置等

Django 视图与网址
------------

在pycharm专业版里头新建Django项目mysite,其目录结构如下：

    mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

在mysite目录下再新建一个应用learn，打开manage.py 命令行，输入`startapp learn` ，新建了一个名为learn的应用，目录如下：

    learn/
    ├── migrations
    ├── __init__.py
    ├── admin.py
    ├── models.py
    ├── tests.py
    └── views.py

我们将新定义的app加到网站mysite的settings.py 中的`INSTALL_APPS` 中：

修改mysite/mysite/settings.py:

    INSTALLED_APPS = 
    (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
       
        'learn',  #新加入的部分
    )

这一步将新建的app加入到INSTALL_APPS 中的目的是为了让Django自动找到该app的模板文件（learn/templates/文件）以及静态文件（learn/static/文件）

定义视图函数（访问页面）
------------

打开learn的view.py文件，写入如下代码：

    #coding:utf-8
    from django.http import HttpResponse
    
    def index(request):
        return HttpResponse(u"我是超市管理系统")

第一行声明编码为：`utf-8` 。第二行引入HttpResponse，用来向网页返回内容。我们还定义了一个index()，其第一个参数必须是request，用于响应页面发来的请求，request中有get和post的内容，用于信息的交互。但是如何调用这个函数呢？  继续往下看。

定义视图函数相关的URL（网址）
----------------

打开mysite/mysite/urls.py 文件，修改如下：

    from django.conf.urls import url
    from django.contrib import admin
    from learn import views as learn_views  # new
     
    urlpatterns = [
        url(r'^$', learn_views.index),  # new
        url(r'^admin/', admin.site.urls),
    ]
   
这时候访问页面 `127.0.0.1:8000` 就会访问到这个index函数了。

在views.py 中在新建一个函数add:

    def add(request):
        a = request.GET['a']  #request.GET类似一个字典，可以用request.GET('a',0)
        b = request.GET['b']
        c = int(a)+int(b)
        return HttpResponse(str(c))

这时候urls添加一条：

    url(r'add/$',learn_views.add,name='add')


这时候访问这个函数需要这样：

    http://127.0.0.1:8000/add/?a=4&b=5

传参数的方式后有一种，在views中定义add2：

    def add2(request,a,b):
        c = int(a)+int(b)
        return HttpResponse(str(c))

在url在定义网址：

    url(r'add/(\d+)/(\d+)/$',learn_views.add2,name='add2')
访问时输入网址：

     http://127.0.0.1:8000/add/4/5/

对于上面在url文件中的新添的url语句：

    url(r'^add/$',learn_views.add,name='add')

这里`name='add'` 用于在`templates` ，`models` ，`views` ... 中得到对应的网址，相当于给网址取了个名字。

接下来我们建立一个有html渲染过的页面，并试验name的作用。

修改learn/views.py 中index函数为：

    def index(request):
        return render(request,'home.html')

render是渲染模板，当执行到render的时候，Django会自动找到在mysite下注册的各个app的templates中的文件。

在learn中新建一个templates文件夹，或者直接在`mysite`的`templates`文件夹上新建`home.html` :

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>超市销售记录</title>
    </head>
    <body>
    <a href = '/add/4/5/'>计算4+5</a>
    <a href = '{% url 'add2' 4 5 %}'>计算4+5</a>
    </body>
    </html>

在urls中修改访问url:

    url(r'^$',learn_views.index,name='home')
    url(r'^add/(\d+)/(\d+)/$', learn_views.add2, name='add2')
    ...

运行服务器，访问`127.0.0.1:8000/` 可以看到我们先去访问learn中的index函数，然后index函数返回一个home.html的渲染（去所有app中的templates中寻找这个文件）。

然而在我的HTML代码中有` <a href = '/add/4/5/'>计算4+5</a>` 可以通过`/add/4/5/` 这个链接链接到这个add这个函数，但是如果在url的位置做如下修改：

    url(r'^add_new/(\d+)/(\d+)/$', learn_views.add2, name='ad1d2')

那么函数就无法使用了。不过只要name不发生改变的话就可以通过name来访问这个函数：

     <a href = '{% url 'add2' 4 5 %}'>计算4+5</a>

这就是name用来找函数的一个作用。

用法如下：

    不带参数的：
    {% url 'name' %}
    带参数的：参数可以是变量名
    {% url 'name' 参数 %}

如果希望访问旧的链接也能定位到新的函数，可以写如下转换函数：

在view中写：

    def old_add2_redirect(request, a, b):
        return HttpResponseRedirect(
            reverse('add2', args=(a, b))
        )

url中补充：

      url(r'^add/(\d+)/(\d+)/$', calc_views.old_add2_redirect),
        url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),

Django模板
--------

我们在模板中设计出html页面用于浏览器显示：

base.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>超市销售记录</title>
    </head>
    <body>
    {% include 'nav.html' %}
    {% block content %}
    <div>这里是默认内容，如果不覆盖就显示这个</div>
    {% endblock %}
    <a href = '/add/4/5/'>计算4+5</a>
    <a href = '{% url 'add2' 4 5 %}'>计算4+5</a>
    </body>
    </html>

其中`{%include 'nav.html'%}` 含义是包含nav.html这个html页面。`'{%block content%} ...{%endblock%}'` 这一部分内部的内容代表默认可替代的部分。我们可以写一个html继承这个页面：

我们可以在首页home.html中写：

    {% extends 'base.html' %}
     
    {% block title %}欢迎光临首页{% endblock %}
     
    {% block content %}
    {% include 'ad.html' %}
    这里是首页，欢迎光临
    {% endblock %}

给模板传递参数
-------

例如：

    def home(request):
        str = u"我是超市人"
        return render(request,'nav.html',{'strin':str})

这样在nav.html中可以通过{{strin}}  来访问这个变量

传入list:

alist = ['1','b','c','d']
render(request,'nav.html',{'alist':alist})

在nav.html中使用：

    {% for i in TutorialList %}
    {{ i }}
    {% endfor %}

若传入字典（strin = {'site':'位置'}），可以用{}{{strin.site}} 的方式来读取数据。

同样，也可以使用：

    {% for key, value in info_dict.items %}
        {{ key }}: {{ value }}
    {% endfor %}

在模板中使用`if` 判断：

{% for item in alist %}
    {{ item }}{% if not forloop.last %},{% endif %}
{% endfor %}

其中`forloop.last` 指循环到最后一个元素它为真。

当判断空值的时候：

    {%for ...%}
    {% empty %}
        当为空的时候执行这里
    {%endfor%}
    
模板中的判断语句：
    
    {% if aint >= 60 %}
        <li>jige</li>
    {% elif aint < 60 %}
        <li>不及格</li>
    {% endif %}

其中大于小于号的前后必须有空格。

获取当前网址：

    {{request.path}}

获取当前GET参数：

    {{request.GET.urlencode}}

Django 数据库模型
------------

Django模型是与数据库相关的，与数据库相关的代码一般写在`models.py` 中，Django支持多种数据库，只需要在settings.py中配置数据库，不需要修改models中的代码就可以使用。

在learn的models中写入如下代码：

    from django.db import models
    
    class Person(models.Model):
        name = models.CharField(max_length=30)
        age = models.IntegerField()
	    def __unicode__(self):  #显示出查询结果
        return self.name
此时进入命令行（shell）状态，输入`makemigrations` ，之后再输入`migrate` 就在后台生成了一张Person的表。有age和name的字段。

使用Django提供的QuerySet API 对数据库进行操作（shell环境下）：

    from learn.models import Person
    Person.objects.create(name='aa',age=23) #创建一条记录
    Person.objects.get(name='aa') #查询
    Person.objects.all()#获取对象
    Person.objects.filer(name='a')#筛选
   
使用以上的表（Person[name,age]）进行数据库的操作：

**插入记录：**

 - Person.objects.create(name='11',age=11)
 - Person.objects.get_or_create(name='11',age=11)
 - p = Person(name='11')   p.age = 11 p.save()

**数据对象的获取**

 - a = Person.objects.all() #a 是一个QuerySet,通过a= list(a) 的方式来获取一个存在list中的数据
 - Person.objects.filiter(name='11')  #选出name=11 的那个
 - Person.objects.exclude(name__contains='qq') 排除name中函数qq的对象

**删除记录**

 - Person.objects.filiter(name__contains='aa').delete()

**更新操作**

 - Person.objects.filiter(name__contains='aa').update(name='xxx')

**单个对象的更新**

    tw = Person.objects.get(name = 'xxx')
    tw.age = 11
    tw.name = 12

**获取某些字段**

    person = Person.objects.values_list('name','age')
    这时候person 就是一个函数两项元素的QuerySet
    list(person) 可以得到这个元组的list

如果只要一个字段：

    Person.objects.values_list('name',flat=True)

**获得字典形式的结果**

    使用value
    a=Person.objects.values('name','q')
    得到的结果a是一个list里头装着dict

使用Django的后台
-----------

后台的网址是：127.0.0.1.8000/admin

首先我们在manage.py 的环境下输入createsuperuser 来创建一个管理员。紧接着要求输入用户名和密码，输完之后就可以了。

这时候还没完，要在后台显示创建的数据库还需要如下操作：

假设我们已经在blog应用中创建好了一个数据库Person[name,age]。打开blog应用下的admin.py文件。修改如下：

    from django.contrib import admin
    from .models import Person
    class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','age',)
    Admin.site.register(Person,PersonAdmin)

就可以在后台显示出数据库了。其中class
的作用是在数据表中显示出每个字段。

注意：在我们在models中建表的时候，在最后添上函数：

    def __str__(self):
        return self.name
这样在查询的时候，返回一个QuerySet，由于添加了这个函数，可以在显示出记录的时候就能显示他的name了

**表单操作**

在blog应用程序中新建一个`form.py` 文件：

    from django import forms
     
    class AddForm(forms.Form):
        a = forms.IntegerField()
        b = forms.CharField(max_length=10)

视图函数：

    # coding:utf-8
    from django.shortcuts import render
    from django.http import HttpResponse
     
    # 引入我们创建的表单类
    from .forms import AddForm
     
    def index(request):
        if request.method == 'POST':# 当提交表单时
         
            form = AddForm(request.POST) # form 包含提交的数据
             
            if form.is_valid():# 如果提交的数据合法
                a = form.cleaned_data['a']
                b = form.cleaned_data['b']
                return HttpResponse(str(int(a) + int(b)))
         
        else:# 当正常访问时
            form = AddForm()
        return render(request, 'index.html', {'form': form})

对应模板：

    <form method='post'>
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="提交">
    </form>
