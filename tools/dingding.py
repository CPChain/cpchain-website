#!/usr/bin/env python3
"""
For detailed markdown format, cf. https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq
"""
import requests

# ピカチュウ robot
url = "https://oapi.dingtalk.com/robot/send?access_token=0f869ba2ac6397c89bdf277df8a9683857764f7944e1a10ce7d9b6054978a349"

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



