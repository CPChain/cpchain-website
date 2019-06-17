from django.shortcuts import render


# Create your views here.

def community_detail(req):
    title = 'title'
    datetime = 'datetime'
    content = 'content'

    return render(req, 'wallet/community_detail.html', locals())
