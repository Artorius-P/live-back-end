# -*- coding:utf-8 -*-
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header
from random import randint


def send_mail(address, code):
    # 发件人地址，通过控制台创建的发件人地址
    username = 'example@example.com'
    # 发件人密码，通过控制台创建的发件人密码
    password = 'your password'
    # 自定义的回复地址
    # replyto = '***'
    # 收件人地址或是地址列表，支持多个收件人，最多30个
    #receivers = ['xxx@alx.com', 'xxx@xx.com']
    #rcptto = ','.join(rcptto)
    rcptto = address
    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header('【在线直播教育平台】密码重置', 'utf-8')
    msg['From'] = '%s <%s>' % (Header('在线直播教育平台', 'utf-8'), username)
    msg['To'] = rcptto
    # msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    # 构建alternative的text/plain部分
    textplain = MIMEText(
        '您的验证码为：'+code + '（5分钟内有效）。\n您正在修改密码，如非本人操作，请忽略该邮件。请勿直接回复此邮件。', _subtype='plain', _charset='UTF-8')
    msg.attach(textplain)
    # 构建alternative的text/html部分
    # texthtml = MIMEText('自定义HTML超文本部分', _subtype='html', _charset='UTF-8')
    # msg.attach(texthtml)
    # 发送邮件
    try:
        #client = smtplib.SMTP()
        # python 2.7以上版本，若需要使用SSL，可以这样创建client
        client = smtplib.SMTP_SSL(host='smtp.example.com')
        #smtplib.SMTP_SSL(host='smtp.gmail.com').connect(host='smtp.gmail.com', port=465)
        # SMTP普通端口为25或80
        client.connect('smtp.example.com', 465)
        # 开启DEBUG模式
        client.set_debuglevel(0)
        client.login(username, password)
        # 发件人和认证地址必须一致
        # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
        #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        client.sendmail(username, rcptto, msg.as_string())
        # 支持多个收件人
        #client.sendmail(username, receivers, msg.as_string())
        client.quit()
        print('邮件发送成功！')
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', e.message)
    except Exception as e:
        print('邮件发送异常, ', str(e))


if __name__ == '__main__':
    send_mail('example@example.com', '114514')
