import xadmin
from .models import *
from xadmin import views


# 开启后台主题样式选择
class BaseSetting(object):
    enable_themes = True
    user_bootswatch = True


# 后台全局设置
class GlobalSettings(object):
    # 后台标签
    site_title = 'Cpchain Admin'
    # 后台页脚
    site_footer = 'cpchain'


class TeamMatesAdmin:
    list_display = ['name', 'name_zh', 'title', 'title_zh', 'image', 'desc', 'desc_zh', 'department', ]
    search_fields = ['name', 'name_zh', 'title', 'title_zh', 'image', 'desc', 'desc_zh', 'department', ]
    list_filter = ['name', 'name_zh', 'title', 'department', ]


class DeptAdmin:
    list_display = ['name']


class PartnerAdmin:
    list_display = ['name', 'type', 'link']


class NewsAdmin:
    list_display = ['title', 'update_time', 'category']
    list_filter = ['update_time', 'category']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(TeamMate, TeamMatesAdmin)
xadmin.site.register(Department, DeptAdmin)
xadmin.site.register(Partner, PartnerAdmin)
xadmin.site.register(New, NewsAdmin)
