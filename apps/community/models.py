
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid

PROPOSAL_STATUS = (
    ('submitted', 'submitted'),
    ('deposited', 'deposited'),
    ('community congress', 'community congress'),
    ('decision congress', 'decision congress'),
    ('passed', 'passed'),
    ('declined', 'declined'),
    ('timeout', 'timeout'),
)

TASK_STATUS = (
    ('available', 'available'),
    ('development', 'development'),
    ('completed', 'completed')
)


class Task(models.Model):
    """ 任务 """
    title = models.CharField(max_length=100)
    description = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                        '/static/youtube/',
                                                                                                        'plugin.js'), (
                                                                                                       'imageresize',
                                                                                                       '/static/imageresize/',
                                                                                                       'plugin.js')])
    amount = models.FloatField(help_text='金额(cpc)', default=0)
    status = models.CharField(
        default='available', choices=TASK_STATUS, max_length=30, help_text='任务状态')
    requirement = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                        '/static/youtube/',
                                                                                                        'plugin.js'), (
                                                                                                       'imageresize',
                                                                                                       '/static/imageresize/',
                                                                                                       'plugin.js')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ClaimEmailReceiver(models.Model):
    """ 认领任务时，需给此 model 中所有的邮箱发送邮件 """
    name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskClaim(models.Model):
    """ 任务认领接口 """
    task_id = models.ForeignKey(Task, models.DO_NOTHING, null=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    advantages = models.CharField(max_length=1000, null=False, blank=False, help_text='优势')
    estimated_date = models.DateField(verbose_name='预计完成日期', help_text='预计完成日期', null=True)
    send_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProposalType(models.Model):
    """ 类型 """
    zh = models.CharField(max_length=50, help_text='中文',
                          null=False, verbose_name='中文名称')
    en = models.CharField(max_length=50, default='',
                          help_text='英文', verbose_name='English name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Proposal(models.Model):
    """ 提案 """
    proposal_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    proposal_type = models.ForeignKey(
        ProposalType, models.DO_NOTHING, null=True)
    title = models.CharField(default='', max_length=100)
    description = RichTextUploadingField(help_text='提案描述', blank=True, null=True,
                                         default='',
                                         external_plugin_resources=[
                                             ('youtube',
                                              '/static/youtube/',
                                              'plugin.js'),
                                             (
                                                 'imageresize',
                                                 '/static/imageresize/',
                                                 'plugin.js')])
    locked_amount = models.FloatField(
        help_text='金额，单位为CPC', null=True, editable=False)
    locked_time = models.DateTimeField(
        help_text='提案时间', null=True, editable=False)
    period = models.IntegerField(help_text='等待时间，单位为秒', null=True)
    likes = models.IntegerField(help_text='赞同数', null=True, editable=False)
    votes = models.IntegerField(help_text='投票数', null=True, editable=False)
    proposer_addr = models.CharField(
        default='', max_length=100, help_text='发起人地址')
    depositor_addr = models.CharField(
        default='', max_length=100, help_text='提案存钱人地址', editable=False)
    status = models.CharField(
        help_text='提案状态', choices=PROPOSAL_STATUS, max_length=30)
    reason = RichTextUploadingField(help_text='理由-决策议会给出的结果', blank=True, null=True,
                                    default='', external_plugin_resources=[
                                        ('youtube',
                                         '/static/youtube/',
                                         'plugin.js'),
                                        (
                                            'imageresize',
                                            '/static/imageresize/',
                                            'plugin.js')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApprovedAddress(models.Model):
    """ 已赞同地址 """
    proposal_id = models.CharField(max_length=36)
    address = models.CharField(max_length=100, help_text='赞同人地址')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VotedAddress(models.Model):
    """ 已投票地址 """
    proposal_id = models.CharField(max_length=36)
    address = models.CharField(max_length=100, help_text='投票人地址')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Congress(models.Model):
    """ 议会 """
    address = models.CharField(
        primary_key=True, max_length=200, help_text='地址')
    created_at = models.DateTimeField(auto_now_add=True)
