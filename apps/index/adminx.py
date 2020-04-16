 

import xadmin
from wallet.models import *
from xadmin import views

from community import models as communityModels

from .models import *


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
    list_display = ['name', 'type', 'link', 'weight']
    list_filter = ['type', ]
    ordering = ['-weight']


class NewsAdmin:
    list_display = ['title', 'update_time', 'category']
    list_filter = ['update_time', 'category']


class MediaAdmin:
    list_display = ['title', 'update_time', 'category']
    list_filter = ['update_time', 'category']


class WalletNewsAdmin:
    list_display = ['title', 'update_time', 'category']
    list_filter = ['update_time', 'category']


class SwipeAdmin:
    model = SwipeBanner
    list_display = ['news', 'lang', 'banner_time', 'is_active']
    list_filter = ['lang', 'is_active']


class FAQAdmin:
    model = FAQ
    list_display = ['title', 'lang', 'weight', 'isActive']
    list_filter = ['lang', 'isActive']


class TermAdmin:
    model = Term
    list_display = ['title']


class NotificationAdmin:
    model = Notification
    list_display = ['content', 'time_start', 'time_end']


class IndexVideoAdmin:
    model = IndexVideo
    list_display = ['name', 'name_en', 'ispublish', 'weight', 'time','placeHolderTime']
    ordering = ['-weight']

class TasksAdmin:
    model = communityModels.Task
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title']
    ordering = ['-updated_at']

class ProposalTypeAdmin:
    model = communityModels.ProposalType
    list_display = ['zh', 'cn']

class ProposalAdmin:
    model = communityModels.Proposal
    list_display = ['proposal_id', 'title', 'status', 'likes', 'votes']
    search_fields = ['proposal_id', 'title']
    list_filter = ['status']
    ordering = ['-updated_at']

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(TeamMate, TeamMatesAdmin)
xadmin.site.register(Department, DeptAdmin)
xadmin.site.register(Partner, PartnerAdmin)
xadmin.site.register(New, NewsAdmin)
xadmin.site.register(Media, MediaAdmin)
xadmin.site.register(Notification, NotificationAdmin)
xadmin.site.register(IndexVideo, IndexVideoAdmin)

xadmin.site.register(WalletNew, WalletNewsAdmin)
xadmin.site.register(SwipeBanner, SwipeAdmin)
xadmin.site.register(FAQ, FAQAdmin)
xadmin.site.register(Term, TermAdmin)

xadmin.site.register(communityModels.Task, TasksAdmin)
xadmin.site.register(communityModels.ProposalType, ProposalTypeAdmin)
xadmin.site.register(communityModels.Proposal, ProposalAdmin)
