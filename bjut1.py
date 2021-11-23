import requests
import urllib3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

#发件人
EMAIL_PASSWORD = environ['EMAIL_PASSWORD']

#ID&TOKEN
ID_1 = environ['ID_1']
ID_2 = environ['ID_2']
ID_3 = environ['ID_3']
ID_4 = environ['ID_4']
ID_5 = environ['ID_5']
TOKEN_1 = environ['TOKEN_1']
TOKEN_2 = environ['TOKEN_2']
TOKEN_3 = environ['TOKEN_3']
TOKEN_4 = environ['TOKEN_4']
TOKEN_5 = environ['TOKEN_5']

def send_email(subject, text, receiver):

    #下面的发件人，收件人是用于邮件传输的。
    smtpserver = 'smtp.163.com'
    username = 'bjutclockin@163.com'
    password= EMAIL_PASSWORD
    sender= 'bjutclockin@163.com'

    #构造邮件对象MIMEMultipart对象
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'bjutclockin@163.com <bjutclockin@163.com>'

    #构造文字内容
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    #发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')

    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

# 禁用warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def func(id, token, receiver):

    # 获取JSESSIONID用headers
    url1 = 'http://bjut.sanyth.com:81/nonlogin/qywx/authentication.htm?appId=402880c97b1aa5f7017b1ad2bd97001b&urlb64' \
           '=L3dlaXhpbi9zYW55dGgvaG9tZS5odG1s '
    h1 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'bjut.sanyth.com:81',
        'Cookie': 'id='+id+'; token='+token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.83 Safari/537.36 '
    }
    #模拟GET用cookie登陆 HTTP/1.1
    r1 = requests.get(url=url1, headers=h1)
    print('r1状态码：', r1.status_code)
    setcookie = r1.history[0].headers['Set-Cookie']
    print('r1.history[0]cookie：', setcookie)
    strJSID = setcookie[:setcookie.index(';')]

    # 打卡用headers
    url2 = 'http://bjut.sanyth.com:81/syt/zzapply/operation.htm'
    h2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Origin': 'http://bjut.sanyth.com:81',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                      'like Gecko)  Mobile/15E148 wxwork/3.1.16 MicroMessenger/7.0.1 Language/zh ColorScheme/Dark',
        'Referer': 'http://bjut.sanyth.com:81/webApp/xuegong/index.html',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': strJSID + '; id='+id+'; token='+token,
        'Host': 'bjut.sanyth.com:81',
        'Content-length': '1150'
    }
    # 模拟POST 投寄打卡json
    r2 = requests.post(url=url2, headers=h2,
                       data='data=%7B%22xmqkb%22%3A%7B%22id%22%3A%22402880c97b1c114b017b1c2af13d02d8%22%7D%2C%22c15%22%3A%22%E6%97%A0%E6%83%85%E5%86%B5%22%2C%22c16%22%3A%22%E5%9C%A8%E6%A0%A1%E4%B8%94%E4%BD%8F%E5%AE%BF%22%2C%22c17%22%3A%22%E5%9C%A8%E4%BA%AC%22%2C%22c18%22%3A%22%E4%BD%8E%E9%A3%8E%E9%99%A9%E5%9C%B0%E5%8C%BA%22%2C%22c12%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%2C%E5%8C%97%E4%BA%AC%E5%B8%82%2C%E6%9C%9D%E9%98%B3%E5%8C%BA%2C%22%2C%22type%22%3A%22YQSJSB%22%2C%22location_longitude%22%3A116.21161177441111%2C%22location_latitude%22%3A39.98611115356111%2C%22location_address%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%E6%9C%9D%E9%98%B3%E5%8C%BA%E5%B9%B3%E4%B9%90%E5%9B%AD100%E5%8F%B7%E5%8C%97%E4%BA%AC%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6%22%7D&msgUrl=syt%2Fzzapply%2Flist.htm%3Ftype%3DYQSJSB%26xmid%3D402880c97b1c114b017b1c2af13d02d8&uploadFileStr=%7B%7D&multiSelectData=%7B%7D&type=YQSJSB')
    print('\nr3状态码：', r2.status_code)
    # success->成功打卡 error->失败 Applied today->今天已经打过卡
    if r2.text == 'success':
        print('成功打卡')
        send_email('打卡成功！', '今天好好学习了吗？\n：）', receiver)
    else:
        if r2.text == 'Applied today':
            print('今天已经打过卡')
            send_email('测试邮件，不必理会。', ':（', receiver)
        else:
            print('打卡失败')
            send_email('失败了失败了！！！', 'ID和TOKEN过期了！！！\n：(\n火速联系管理员更换，一次八百', receiver)
    r2.close()


if __name__ == '__main__':

    #每七天重新获取一次id和token
    id = [ID_1, ID_2, ID_3, ID_4, ID_5]

    token = [TOKEN_1, TOKEN_2, TOKEN_3, TOKEN_4, TOKEN_5]

    #收件人
    EMAIL_RECEIVER_1 = environ['EMAIL_RECEIVER_1']
    EMAIL_RECEIVER_2 = environ['EMAIL_RECEIVER_2']
    EMAIL_RECEIVER_3 = environ['EMAIL_RECEIVER_3']
    EMAIL_RECEIVER_4 = environ['EMAIL_RECEIVER_4']
    EMAIL_RECEIVER_5 = environ['EMAIL_RECEIVER_5']
    receiver = [EMAIL_RECEIVER_1, EMAIL_RECEIVER_2, EMAIL_RECEIVER_3, EMAIL_RECEIVER_4, EMAIL_RECEIVER_5]

    for i in range(len(id)):
        func(id[i], token[i], receiver[i])
