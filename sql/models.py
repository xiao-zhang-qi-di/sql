from django.db import models

# Create your models here.

# 角色分两种
# 1.工程师: 可以提交SQL上线单的工程师们，username字段为登录用户名，display字段为展示的中文名
# 2.审核人: 可以审核并执行SQL上线单的管理者、高级工程师、系统管理员们
class users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    display = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=(
        ('工程师', '工程师'),
        ('审核人', '审核人')
    ), default='工程师')

    def __str__(self):
        return self.username


# 各个线上主库地址
class master_config(models.Model):
    cluster_name = models.CharField(max_length=50)
    master_host = models.CharField(max_length=50)
    master_port = models.IntegerField(default=3306)
    master_user = models.CharField(max_length=50)
    master_password = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cluster_name


# 存放各个SQL上线工单的详细内容，可定期归档或清理历史数据，也可通过alter table workflow row_format=compressed; 来进行压缩
class workflow(models.Model):
    workflow_name = models.CharField(max_length=50)
    engineer = models.CharField(max_length=50)
    review_man = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=(
        ('已正常结束', '已正常结束'),
        ('人工终止流程', '人工终止流程'),
        ('等待审核人审核', '等待审核人审核'),
        ('执行中', '执行中'),
        ('自动审核不通过', '自动审核不通过'),
        ('执行有异常', '执行有异常')
    ))
    is_backup = models.IntegerField(choices=(
        (0, 0),
        (1, 1)
    ))
    review_content = models.TextField()
    cluster_name = models.CharField(max_length=50)
    reviewok_time = models.DateTimeField()
    sql_content = models.TextField()
    execute_result = models.TextField()

    def __str__(self):
        return self.workflow_name