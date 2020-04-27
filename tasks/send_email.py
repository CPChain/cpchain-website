"""

Send Email

You need configure the SMTP in GSuite.

"""

import django
import os
import pytz

from datetime import datetime as dt
from log import get_log

import smtplib
from email.mime.text import MIMEText
from email.header import Header

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpchain_test.settings')
django.setup()

# import models
from community.models import Email

log = get_log('send-email')

sender = 'liaojl@cpchain.io'
mail_host = 'smtp-relay.gmail.com'
mail_port = 587

def send_email():
    log.info('send email')
    for item in Email.objects.filter(sent=False):
        try:
            log.info(f'send email, id: {item.id}')
            to = [item.to]
            message = MIMEText(item.content, 'html', 'utf-8')
            message['From'] = Header(sender, 'utf-8')
            message['To'] =  Header(item.to, 'utf-8')
            message['Subject'] = Header('任务认领通知', 'utf-8')
            smtpObj = smtplib.SMTP(mail_host, mail_port)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.sendmail(sender, to, message.as_string())
            log.debug('send success')
            item.sent = True
            item.sent_at = dt.now(tz=pytz.timezone('Asia/Shanghai'))
            item.save()
        except Exception as e:
            log.error(e)

def test():
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    sender = 'liaojl@cpchain.io'
    mail_host = 'smtp-relay.gmail.com'
    mail_port = 587
    to = [sender]
    message = MIMEText("just a test", 'html', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] =  Header(sender, 'utf-8')
    message['Subject'] = Header('Email Test', 'utf-8')
    smtpObj = smtplib.SMTP(mail_host, mail_port)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.sendmail(sender, to, message.as_string())
    print('send success')

if __name__ == '__main__':
    send_email()
