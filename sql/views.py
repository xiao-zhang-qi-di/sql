import json
import re
import time

from django import http
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .dao import Dao
from .models import users, master_config, workflow
from .const import Const
from .inception import InceptionDao

dao = Dao()
inceptionDao = InceptionDao()

def login(request):
    return render(request, 'login.html')

def logout(request):
    if request.session.get('login_username', False):
        del request.session['login_username']
    return render(request, 'login.html')

# ajax接口, 登录页面调用, 用来验证用户名密码
# 取消csrf—token验证
@csrf_exempt
def authenticate(request):
    """认证机制做的非常简单"""
    # 判断当前是否为 AJAX 请求
    if request.is_ajax():
        strUsername = request.POST.get('username')
        strPassword = request.POST.get('password')
    else:
        strUsername = request.POST['username']
        strPassword = request.POST['password']
    # 服务端二次验证参数
    result = {}
    if strUsername == "" or strPassword == "" or strUsername is None or strPassword is None:
        result = {
            "status": 2,
            "msg": "登录用户名或密码为空, 请重新输入！",
            "data": ""
        }
        return http.HttpResponse(json.dumps(result), content_type="application/json")

    correct_users = users.objects.filter(username=strUsername)
    if len(correct_users) == 1 and check_password(strPassword, correct_users[0].password) == True:
        #调用了django内置函数check_password函数检测输入的密码是否与django默认的PBKDF2算法相匹配
        request.session['login_username'] = strUsername
        result = {
            "status": 0,
            "msg": "ok",
            "data": ""
        }
    else:
        result = {
            "status": 1,
            "msg": "用户名或密码错误，请重新输入！",
            "data": ""
        }
    return http.HttpResponse(json.dumps(result), content_type="application/json")

# 首页, 也是查看所有SQL工单页面, 具备翻页功能
def allworkflow(request):
    # 一个页面展示
    PAGE_LIMIT = 12

    pageNo = 0
    navStatus = ''
    listAllWorkflow = []

    # 参数检查
    if 'pageNo' in request.GET:
        pageNo = request.GET['pageNo']
    else:
        pageNo = '0'

    if 'navStatus' in request.GET:
        navStatus = request.GET['navStatus']
    else:
        navStatus = 'all'

    # isinstance判断类型
    if not isinstance(pageNo, str) or not isinstance(navStatus, str):
        raise TypeError('pageNo或navStatus页面传入参数不对')
    else:
        try:
            pageNo = int(pageNo)
            if pageNo < 0:
                pageNo = 0
        except ValueError as ve:
            context = {'errMsg': 'pageNo参数不是int'}
            return render(request, 'error.html', context)

    loginUser = request.session.get('login_username', False)
    # 查询workflow model, 根据pageNo和navStatus获取对应的内容
    offset = pageNo * PAGE_LIMIT
    limit = offset + PAGE_LIMIT

    listWorkflow = []
    # 查询全部流程
    if navStatus == 'all':
        # 这句话等同于select * from sql_workflow order by create_time desc limit {offset, limit};
        listWorkflow = workflow.objects.exclude(status=Const.workflowStatus['autoreviewwrong']).order_by('-create_time')[offset:limit]
    elif navStatus == 'waitingforme':
        listWorkflow = workflow.objects.filter(status=Const.workflowStatus['manreviewing'], review_man=loginUser).order_by(
            '-create_time')[offset:limit]
    elif navStatus == 'finish':
        listWorkflow = workflow.objects.filter(status=Const.workflowStatus['finish']).order_by('-create_time')[offset:limit]
    else:
        context = {'errMsg': '传入的navStatus参数有误'}
        return render(request, 'error.html', context)

    context = {
        'currentMenu': 'allworkflow',
        'listWorkflow': listWorkflow,
        'pageNo': pageNo,
        'navStatus': navStatus
    }

    return render(request, 'allWorkflow.html', context)

# 提交SQL的页面
def submitSql(request):
    masters = master_config.objects.all()
    if len(masters) == 0:
        context = {'errMsg': '集群树为0, 可能后端数据没有配置集群'}
        return render(request, 'error.html', context)

    # 获取所有集群名称
    listAllClusterName = [master.cluster_name for master in masters]

    dictAllClusterDb = {}
    # 每一个都首先获取主库地址在哪里
    for clusterName in listAllClusterName:
        listMasters = master_config.objects.filter(cluster_name=clusterName)
        if len(listMasters) != 1:
            context = {'errMsg': '存在两个集群名称一样的集群, 请修改数据库'}
            return render(request, 'error.html', context)
        # 取出该集群的名称以及连接方式, 为了后面连进去获取所有databases
        masterHost = listMasters[0].master_host
        masterPort = listMasters[0].master_port
        masterUser = listMasters[0].master_user
        masterPassword = listMasters[0].master_password

        listDb = dao.getAlldbByCluster(masterHost, masterPort, masterUser, masterPassword)
        dictAllClusterDb[clusterName] = listDb

    # 获取所有的审核人, 当前登录用户不可以审核
    loginUser = request.session.get('login_username', False)
    reviewMen = users.objects.filter(role='审核人').exclude(username=loginUser)
    if len(reviewMen) == 0:
        context = {'errMsg': '审核人为0, 请配置审核人'}
        return render(request, 'error.html', context)
    listAllReviewMen = [user.username for user in reviewMen]

    context = {'currentMenu': 'submitsql', 'dictAllClusterDb': dictAllClusterDb, 'reviewMen': listAllReviewMen}

    return render(request, 'submitSql.html', context)

# 提交SQL给inception进行解析
def autoreview(request):
    sqlContent = request.POST['sql_content']
    workflowName = request.POST['workflow_name']
    clusterName = request.POST['cluster_name']
    isBackup = request.POST['is_backup']
    reviewMan = request.POST['review_man']

    # 服务器端参数验证
    if sqlContent is None or workflowName is None or clusterName is None or isBackup is None or reviewMan is None:
        context = {'errMsg': '页面提交参数可能为空'}
        return render(request, 'error.html', context)
    elif sqlContent[-1] != ";":
        context = {'errMsg': "SQL语句结尾没有以;结尾，请后退重新修改并提交！"}
        return render(request, 'error.html', context)

    # 交给inception进行自动审核
    result = inceptionDao.sqlautoReview(sqlContent, clusterName, isBackup)
    if result is None or len(result) == 0:
        context = {'errMsg': 'inception返回的结果集为空! 可能是SQL语句有语法错误'}
        return render(request, 'error.html', context)

    # 要把result转成JSON存进数据库里, 方便SQL单子详细信息展示
    jsonResult = json.dumps(result)
    print('jsonResult', jsonResult)

    # 遍历result, 看是否有任何自动审核不通过的地方, 一旦有, 则为自动审核不通过, 没有的话, 则为等待人工审核状态
    workflowStatus = Const.workflowStatus['manreviewing']
    for row in result:
        if row[2] == 2:
            # 状态为2表示严重错误, 必须修改
            workflowStatus = Const.workflowStatus['autoreviewwrong']
            break
        elif re.match(r"\w*comments\w*", row[4]):
            workflowStatus = Const.workflowStatus['autoreviewwrong']
            break
    # 存进数据库里
    newWorkflow = workflow()
    newWorkflow.workflow_name = workflowName
    newWorkflow.engineer = request.session.get('login_username', False)
    newWorkflow.review_man = reviewMan
    newWorkflow.create_time = getNow()
    newWorkflow.is_backup = isBackup
    newWorkflow.review_content = jsonResult
    newWorkflow.cluster_name = clusterName
    newWorkflow.sql_content = sqlContent
    newWorkflow.save()
    workflowId = newWorkflow.id
    return HttpResponseRedirect('/detail/' + str(workflowId) + '/')


# 展示SQL工单详细内容, 以及可以人工审核, 审核通过即可执行
def detail(request, workflowId):
    workflowDetail = get_object_or_404(workflow, pk=workflowId)
    listContent = None
    if workflowDetail.status in (Const.workflowStatus['finish'], Const.workflowStatus['exception']):
        listContent = json.loads(workflowDetail.execute_result)
    else:
        listContent = json.loads(workflowDetail.review_content)
    context = {'currentMenu': 'allworkflow', 'workflowDetail': workflowDetail, 'listContent': listContent}
    return render(request, 'detail.html', context)

# 人工审核也通过, 执行SQL
def execute(request):
    workflowId = request.POST['workflowid']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空'}
        return render(request, 'error.html', context)

    workflowId = int(workflowId)
    workflowDetail = workflow.objects.get(id=workflowId)
    clusterName = workflowDetail.cluster_name

    # 服务器端二次验证, 正在执行人工审核动作的当前登录用户必须为审核人, 避免攻击或被接口测试工具强行绕过
    loginUser = request.session.get('login_username', False)
    if loginUser is None or loginUser != workflowDetail.review_man:
        context = {'errMsg': '当前登录用户不是审核人, 请重新登录'}
        return render(request, 'error.html', context)

    # 服务器端二次验证, 当前工单状态必须为等待人工审核
    if workflowDetail.status != Const.workflowStatus['manreviewing']:
        context = {'errMsg': '当前工单状态不是等待人工审核中, 请刷新当前页面'}
        return render(request, 'error.html', context)

    dictConn = getMasterConnStr(clusterName)

    # 将流程状态修改为执行中, 并更新reviewok_time字段
    workflowDetail.status = Const.workflowStatus['executing']
    workflowDetail.reviewok_time = getNow()
    workflowDetail.save()

    # 交给inception先split, 再执行
    (finalStatus, finalList) = inceptionDao.executeFinal(workflowDetail, dictConn)

    # 封装成JSON格式存进数据库字段里
    strJsonResult = json.dumps(finalList)
    workflowDetail.execute_result = strJsonResult
    workflowDetail.finish_time = getNow()
    workflowDetail.status = finalStatus
    workflowDetail.save()

    return HttpResponseRedirect('/detail/' + str(workflowDetail.id) + '/')

# 终止流程
def cancel(request):
    workflowId = request.POST['workflowid']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空'}
        return render(request, 'error.html', context)

    workflowId = int(workflowId)
    workflowDetail = workflow.objects.get(id=workflowId)

    # 服务器端二次验证, 如果正在执行终止动作的当前登录用用户不是发起人也不是审核人, 则异常
    loginUser = request.session.get('login_username', False)
    if loginUser is None or (loginUser != workflowDetail.review_man and loginUser != workflowDetail.engineer):
        context = {'errMsg': '当前登录用户不是审核人也不是发起人, 请重新登录'}
        return render(request, 'error.html', context)

    # 服务器端二次验证, 如果当前单子状态是结束状态, 则不能发起终止
    if workflowDetail.status in (Const.workflowStatus['abort'], Const.workflowStatus['finish'], Const.workflowStatus['autoreviewwrong'], Const.workflowStatus['exception']):
        return HttpResponseRedirect('/detail/' + str(workflowId) + '/')

    workflowDetail.status = Const.workflowStatus['abort']
    workflowDetail.save()

    return HttpResponseRedirect('/detail/' + str(workflowDetail.id) + '/')

# 展示回滚的SQL
def rollback(request):
    workflowId = request.GET['workflowid']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空'}
        return render(request, 'error.html', context)
    workflowId = int(workflowId)
    listBackupSql = inceptionDao.getRollbackSqlList(workflowId)
    context = {'listBackupSql': listBackupSql}
    return render(request, 'rollback.html', context)

# 根据集群名获取主库连接字符串, 并封装成一个dict
def getMasterConnStr(clusterName):
    listMasters = master_config.objects.filter(cluster_name=clusterName)
    masterHost = listMasters[0].master_host
    masterPort = listMasters[0].master_port
    masterUser = listMasters[0].master_user
    masterPassword = listMasters[0].master_password
    dictConn = {
        'masterHost': masterHost,
        'masterPort': masterPort,
        'masterUser': masterUser,
        'masterPassword': masterPassword
    }
    return dictConn

# 获取当前时间
def getNow():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())










