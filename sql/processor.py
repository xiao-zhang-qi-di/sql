leftMenuBtns = (
    {'key': 'allworkflow', 'name': '查看历史工单', 'url': '/allworkflow/', 'class': 'glyphicon glyphicon-home'},
    {'key': 'submitsql', 'name': '发起SQL上线', 'url': '/submitsql/', 'class': 'glyphicon glyphicon-asterisk'},
    {'key': 'masterconfig', 'name': '主库地址配置', 'url': '/masterconfig/', 'class': 'glyphicon glyphicon-user'},
    {'key': 'userconfig', 'name': '用户权限配置', 'url': '/userconfig/', 'class': 'glyphicon glyphicon-th-large'},
)

def global_info(request):
    """存放用户、会话信息等"""
    return {
        'loginUser': request.user,
        'leftMenuBtns': leftMenuBtns,
    }