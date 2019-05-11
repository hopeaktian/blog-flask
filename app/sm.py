#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
发送txt文本邮件
'''
import smtplib
from email.mime.text import MIMEText
import os, time

mailto_list=["hopeaktian@foxmail.com"] 
mail_host="smtp.sohu.com"  #设置服务器
mail_user="hopeaktian@sohu.com"    #用户名
mail_pass="*********"   #口令
mail_postfix="sohu.com"  #发件箱的后缀

def send_mail(to_list,sub,content):
    me="peaktian"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content, 'plain', 'utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔  
    try:  
        server = smtplib.SMTP_SSL()  
        server.connect(mail_host, 465)                            #连接服务器  
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False
def mail_admin(urls,email,mes):
    message = str(urls) + " " + str(email) + " " + str(mes)
    for i in range(1):                             #发送1封，上面的列表是几个人，这个就填几
        if send_mail(mailto_list,"互加友链请求",message):
            return 1
        else:
            return 0

