# V-Board: 一站式管理协作平台

![](https://img.shields.io/badge/language-Python-green.svg)
![](https://img.shields.io/badge/Powered%20By-Django%20Bootstrap%20JQuery-blue)
![](https://img.shields.io/badge/Database-MySQL-green.svg)

## 项目概述

​	V-Board看板是由装满卡片、由你和你的团队使用的各种列表的列表。他核心要素也就只有看板、列表、卡片这三者。从这三个最基础的组件派生出许多有趣且实用的功能。符合大多数用户不同的需求。从个人的日程管理，记录生活琐事，工作计划到团队的项目开发，团队合作都可以提供一种简单有效的管理和记录方式。可以私用或者公用，不论是用作团队协作的进度展示，还是日程管理，V-board都可以完成。

## 项目结构

> 暂定

## 开发日志

### 2019-11-8

> 搭建基础框架，配置基础环境，配置Django setting.py (模板、主语言、时区、静态文件等)

#### 配置 Django 模板寻找目录

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # 添加此行增加模板目录
        'APP_DIRS': True,# 使其可以在APP目录下寻找
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### 配置 Django 静态文件寻找目录

```python
# APP下的静态文件位置
STATIC_URL = '/static/'
# 全局静态文件位置
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

#### 配置 MySQL

> 此处开发需在 MySQL中新建用户 stranger 配置其密码为123456（仅开发使用）
>
> 创建新数据库 v-board 供项目使用

在Django setting.py 中 配置 MySQL为默认数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "v-board",
        'USER': "stranger",
        "PASSWORD":'123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

