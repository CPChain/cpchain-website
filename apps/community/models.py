
from django.db import models

PROPOSAL_STATUS = (
    ('submitted', 'submitted'),
    ('deposited', 'deposited'),
    ('community congress', 'community congress'),
    ('decision congress', 'decision congress'),
    ('passed', 'passed'),
    ('declined', 'declined'),
    ('timeout', 'timeout'),
)

class Tasks(models.Model):
    """ 任务 """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Proposals(models.Model):
    """ 提案 """
    proposal_id = models.CharField(max_length=36)
    proposal_type = models.CharField(default='', max_length=100)
    title = models.CharField(default='', max_length=100)
    description = models.CharField(default='', max_length=1000)
    locked_amount = models.FloatField(help_text='金额，单位为CPC')
    locked_time = models.DateTimeField(help_text='提案时间')
    period = models.IntegerField(help_text='等待时间，单位为秒')
    likes = models.IntegerField(help_text='赞同数')
    votes = models.IntegerField(help_text='投票数')
    proposer_addr = models.CharField(default='', max_length=100, help_text='发起人地址')
    depositor_addr = models.CharField(default='', max_length=100, help_text='提案存钱人地址')
    status = models.CharField(help_text='提案状态', choices=PROPOSAL_STATUS, max_length=30)
    reason = models.CharField(help_text='理由-决策议会给出的结果', max_length=500, default='')
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
    address = models.CharField(primary_key=True, max_length=200, help_text='地址')
    created_at = models.DateTimeField(auto_now_add=True)
