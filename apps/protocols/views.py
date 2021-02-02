from django.views.generic.base import View
from django.shortcuts import render

class PrivacyCNView(View):
    def get(self, req):
        return render(req, 'protocols/private_policy_cn.html')

class PrivacyZHView(View):
    def get(self, req):
        return render(req, 'protocols/private_policy_zh.html')

