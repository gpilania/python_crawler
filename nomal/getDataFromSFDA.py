# -*- coding: utf-8 -*-
import requests
import traceback
import time
import os
import json
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText

def get_data(url):
	try:
		response = requests.get(url)
		html = response.text
		return html
	except Exception as e:
		traceback.print_exc()
		pass

def get_random(begin, end):
    index = random.randint(begin, end)
    return index

def sleep_moment():
    begin = 1
    end = 5
    index = get_random(begin, end)
    time.sleep(index)

def parse_data(index, arr):
    try:
        data = json.loads(arr)
    except Exception:
        print('index: ' + str(index) + ' err')
        return
    name = ''
    content = ''
    apply_name = ''
    for i in data:
        if i['NAME'] == '产品名称':
            # print('产品中文名称', i['CONTENT'])
            name = i['CONTENT']
        if i['NAME'] == '批准文号':
            content = i['CONTENT']
        if i['NAME'] == '申请人中文名称':
            apply_name = i['CONTENT']
            # print('批准文号', i['CONTENT'])

    base_dir = os.getcwd()
    today = time.strftime('%Y%m%d', time.localtime())
    fiename = base_dir + "/" + today + 'x.txt'
    # 从内存以追加的方式打开文件，并写入对应的数据
    with open(fiename, 'a', encoding='GBK') as f:
        f.write(str(index) + '  ')
        f.write(name + '  ')
        f.write(content + '  ')
        f.write(apply_name + '  \n')

class SendMsg():

    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.163.com"  # SMTP服务器
        self.mail_user = "maduar@163.com"  # 用户名
        self.mail_pass = "x"  # 授权密码，非登录密码

    def sendEmail(self, sender, receivers, content, title):
        # content = '我用Python'
        # title = '人生苦短'  # 邮件主题
        # receivers = ['310173679@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        # sender = 'maduar@163.com'  # 发件人邮箱(最好写全, 不然会失败)
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message['Subject'] = title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)


    def send_email2(SMTP_host, from_account, from_passwd, to_account, subject, content):
        email_client = smtplib.SMTP(SMTP_host)
        email_client.login(from_account, from_passwd)
        # create msg
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')  # subject
        msg['From'] = from_account
        msg['To'] = to_account
        email_client.sendmail(from_account, to_account, msg.as_string())
        email_client.quit()

if __name__ == "__main__":
    #     国家食品药品监督管理局-特殊食品-进口保健品
    #    request_url = 'http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=31&searchF=ID&searchK='

    #     国家食品药品监督管理局-特殊食品-国产保健品
    request_url = 'http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=30&searchF=ID&searchK='

    sendMsg = SendMsg()
    for index in range(1,5):
        exec_url = request_url + str(index)
        print('crowler: ' + str(index) + ',  url=' + exec_url)
        arr = get_data(exec_url)
        parse_data(index, arr)
        sleep_moment()
        if index % 3 == 0:
            content = 'crowler: ' + str(index)
            title = 'crowler'  # 邮件主题
            receivers = ['maduar@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
            sender = 'maduar@163.com'  # 发件人邮箱(最好写全, 不然会失败)
            sendMsg.sendEmail(sender, receivers, content, title)

    content = 'request_url: ' + request_url + 'is finsish'
    title = 'success!'  # 邮件主题
    receivers = ['maduar@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    sender = 'maduar@163.com'  # 发件人邮箱(最好写全, 不然会失败)
    sendMsg.sendEmail(sender, receivers, content, title)







