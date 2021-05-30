# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql', '0005_auto_20210528_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='cluster_name',
            field=models.CharField(max_length=50, verbose_name='集群名称'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='execute_result',
            field=models.TextField(verbose_name='执行结果的JSON格式'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='finish_time',
            field=models.DateTimeField(null=True, blank=True, verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='is_backup',
            field=models.CharField(max_length=20, choices=[('否', '否'), ('是', '是')], verbose_name='是否备份'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='review_content',
            field=models.TextField(verbose_name='自动审核内容的JSON格式'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='reviewok_time',
            field=models.DateTimeField(null=True, blank=True, verbose_name='人工审核通过的时间'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='sql_content',
            field=models.TextField(verbose_name='具体sql内容'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='status',
            field=models.CharField(choices=[('已正常结束', '已正常结束'), ('人工终止流程', '人工终止流程'), ('自动审核中', '自动审核中'), ('等待审核人审核', '等待审核人审核'), ('执行中', '执行中'), ('自动审核不通过', '自动审核不通过'), ('执行有异常', '执行有异常')], max_length=50),
        ),
    ]
