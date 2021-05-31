# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('display', models.CharField(max_length=50, verbose_name='显示的中文名')),
                ('role', models.CharField(choices=[('工程师', '工程师'), ('审核人', '审核人')], max_length=20, default='工程师', verbose_name='角色')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', verbose_name='groups', related_query_name='user', blank=True, related_name='user_set')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', related_query_name='user', blank=True, related_name='user_set')),
            ],
            options={
                'verbose_name': '用户配置',
                'verbose_name_plural': '用户配置',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='master_config',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('cluster_name', models.CharField(max_length=50, verbose_name='集群名称')),
                ('master_host', models.CharField(max_length=50, verbose_name='主库地址')),
                ('master_port', models.IntegerField(default=3306, verbose_name='主库端口')),
                ('master_user', models.CharField(max_length=50, verbose_name='登录主库的用户名')),
                ('master_password', models.CharField(max_length=50, verbose_name='登录主库的密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '主库地址',
                'verbose_name_plural': '主库地址',
            },
        ),
        migrations.CreateModel(
            name='workflow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('workflow_name', models.CharField(max_length=50, verbose_name='工单内容')),
                ('engineer', models.CharField(max_length=50, verbose_name='发起人')),
                ('review_man', models.CharField(max_length=50, verbose_name='审核人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('finish_time', models.DateTimeField(null=True, blank=True, verbose_name='结束时间')),
                ('status', models.CharField(choices=[('已正常结束', '已正常结束'), ('人工终止流程', '人工终止流程'), ('自动审核中', '自动审核中'), ('等待审核人审核', '等待审核人审核'), ('执行中', '执行中'), ('自动审核不通过', '自动审核不通过'), ('执行有异常', '执行有异常')], max_length=50)),
                ('is_backup', models.CharField(choices=[('否', '否'), ('是', '是')], max_length=20, verbose_name='是否备份')),
                ('review_content', models.TextField(verbose_name='自动审核内容的JSON格式')),
                ('cluster_name', models.CharField(max_length=50, verbose_name='集群名称')),
                ('reviewok_time', models.DateTimeField(null=True, blank=True, verbose_name='人工审核通过的时间')),
                ('sql_content', models.TextField(verbose_name='具体sql内容')),
                ('execute_result', models.TextField(verbose_name='执行结果的JSON格式')),
            ],
            options={
                'verbose_name': '工单管理',
                'verbose_name_plural': '工单管理',
            },
        ),
    ]
