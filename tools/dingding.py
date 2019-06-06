#!/usr/bin/env python3
"""
For detailed markdown format, cf. https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq
"""
import requests

from cpchain_test.config import cfg
# ピカチュウ robot
url = cfg['pikachu']['url']

def post_message(message, title="pikachu"):
    headers = {"Content-Type": "application/json"}
    data = {'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': message
            },
            'at': {
                "isAtAll": True
            }
    }
    response = requests.post(url=url, headers=headers, json=data)
    result = response.json()
    print(result)



