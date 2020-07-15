 

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
    list_display = ['title', 'status', 'amount', 'updated_at']
    search_fields = ['title']
    ordering = ['-updated_at']

class ProposalTypeAdmin:
    model = communityModels.ProposalType
    list_display = ['id', 'zh', 'en']

class ProposalAdmin:
    model = communityModels.Proposal
    list_display = ['proposal_id', 'title', 'status', 'likes', 'votes']
    search_fields = ['proposal_id', 'title']
    list_filter = ['status']
    ordering = ['-updated_at']

class ClaimEmailReceiverAdmin:
    model = communityModels.ClaimEmailReceiver
    list_display = ['id', 'name', 'email']
    ordering = ['-updated_at']

class TaskClaimAdmin:
    model = communityModels.TaskClaim
    list_display = ['task_id', 'name', 'email', 'estimated_date']
    ordering = ['-updated_at']

    _actions = None

    def get_actions(self, request):
        #Disable delete
        actions = super().get_actions(request)
        print(actions)
        self._actions = actions
        del actions['delete_selected']
        del actions['editing']
        del actions['add']
        return actions

    def has_delete_permission(self, obj=None):
        #Disable delete
        return False

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
xadmin.site.register(communityModels.ClaimEmailReceiver, ClaimEmailReceiverAdmin)
# xadmin.site.register(communityModels.TaskClaim, TaskClaimAdmin)
