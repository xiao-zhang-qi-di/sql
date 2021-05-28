# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql', '0004_auto_20210526_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_config',
            name='cluster_name',
            field=models.CharField(verbose_name='集群名称', max_length=50),
        ),
        migrations.AlterField(
            model_name='master_config',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='master_config',
            name='master_host',
            field=models.CharField(verbose_name='主库地址', max_length=50),
        ),
        migrations.AlterField(
            model_name='master_config',
            name='master_password',
            field=models.CharField(verbose_name='登录主库的密码', max_length=50),
        ),
        migrations.AlterField(
            model_name='master_config',
            name='master_port',
            field=models.IntegerField(verbose_name='主库端口', default=3306),
        ),
        migrations.AlterField(
            model_name='master_config',
            name='master_user',
            field=models.CharField(verbose_name='登录主库的用户名', max_length=50),
        ),
        migrations.AlterField(
            model_name='master_config',
            name='update_time',
            field=models.DateTimeField(verbose_name='更新时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='display',
            field=models.CharField(verbose_name='显示的中文名', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(verbose_name='密码', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.CharField(verbose_name='角色', choices=[('工程师', '工程师'), ('审核人', '审核人')], max_length=20, default='工程师'),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(verbose_name='用户名', max_length=50),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='engineer',
            field=models.CharField(verbose_name='发起人', max_length=50),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='review_man',
            field=models.CharField(verbose_name='审核人', max_length=50),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='workflow_name',
            field=models.CharField(verbose_name='工单内容', max_length=50),
        ),
    ]
