#-*-encoding:utf-8-*-
import argparse
import urllib.request, urllib.parse, urllib.error
import time, ast

username = ''
password = ''

portal_url = 'http://p.nju.edu.cn'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
language = 'cn'
io_url = '/portal_io/'
auth_type = 'pap'
pageNum = 5
userinfo = None
selfservice = None
service = {
        'current' : None,
        'next' : None,
        'chose' : []
    }
refresh = True,
server_time = None

#https://www.cnblogs.com/MnCu8261/p/5880764.html
def long2ip(long):
    floor_list=[]
    yushu=long
    for i in reversed(range(4)):
        res=divmod(yushu,256**i)
        floor_list.append(str(res[0]))
        yushu=res[1]
    return '.'.join(floor_list)

def letterorcharacter(ch):
    if ord(ch) <= 127 and ord(ch) >= 0:
        return 1
    else :
        return 0
        
#def addSpace(str, symbol='\s')

def myFormatPrint(string, length=0, align='l', symbol='\s'):
    i = 0
    temp = ''
    str_len = len(string)
    while i < length:
        temp += symbol
        i += 1
    i = 0
    str_sp = 0
    while i < str_len:
        str_sp += 1 if letterorcharacter(string[i]) else 2
        i += 1
    if align == 'l':
        return string + temp[str_sp:]
    if align == 'r':
        return temp[:-str_sp] + string
    if align == 'c':
        l_c = (length - str_sp)//2
        r_c = length - l_c - str_sp
        return temp[:-(str_sp+r_c)] + string + temp[l_c+str_sp:]

def loginRequest(user, passwd):
    params = {
        'username': username if user == '' else user,
        'password': password if passwd == '' else passwd
    }
    if params['username'] == '' or params['password'] == '':
        return
    params_encode = urllib.parse.urlencode(params).encode('utf8')
    request_url = portal_url + io_url + 'login'
    login_request = urllib.request.Request(url = request_url, data = params_encode, headers = headers)
    try:
        response_data = urllib.request.urlopen(login_request)
        response = response_data.read().decode('utf8')
        return response
    except urllib.error.HTTPError as e:
        print("HTTPError")
        print(e.code)
    except urllib.error.URLError as e:
        print("URLError")
        print(e.reason)
    
def getInformation():
    request_url = portal_url + io_url + 'selfservice/volume/getlist'
    request = urllib.request.Request(url = request_url, headers = headers)
    try:
        response_data = urllib.request.urlopen(request)
        response = response_data.read().decode('utf8')
        return response
    except urllib.error.HTTPError as e:
        print("HTTPError")
        print(e.code)
    except urllib.error.URLError as e:
        print("URLError")
        print(e.reason)


def getOnline():
    request_url = portal_url + io_url + 'selfservice/online/getlist'
    params = {
        'page': 1,
        'rows': 5
    }
    params_encode = urllib.parse.urlencode(params).encode('utf8')
    request = urllib.request.Request(url = request_url, data = params_encode, headers = headers)
    try:
        response_data = urllib.request.urlopen(request)
        response = response_data.read().decode('utf8')
        return response
    except urllib.error.HTTPError as e:
        print("HTTPError")
        print(e.code)
    except urllib.error.URLError as e:
        print("URLError")
        print(e.reason)

def logoutRequest():
    request_url = portal_url + io_url + 'logout'
    request = urllib.request.Request(url = request_url, headers = headers)
    try:
        response_data = urllib.request.urlopen(request)
        response = response_data.read().decode('utf8')
        return response
    except urllib.error.HTTPError as e:
        print("HTTPError")
        print(e.code)
    except urllib.error.URLError as e:
        print("URLError")
        print(e.reason)


def convertTime(time, type):
	h = 0
	m = 0
	s = 0
	if type == 'S':
		h = time // 3600
		m = (time - h * 3600) // 60
		return str(m) + '分钟' if h == 0 else str(h) + '小时' + str(m) + '分钟'
	elif type == 'D':
		h = time // 3600
		m = (time - h * 3600) // 60
		s = time - h * 3600 - m * 60
		return (("" if h > 9 else "0") + str(h)) + ":" + (("" if m > 9 else "0") + str(m)) + ":" + (("" if s > 9 else "0") + str(s))

def printLoginInformation(response):
    #查询在线信息
    online_information = ast.literal_eval(getInformation())
    print(myFormatPrint('', 35, align='l', symbol = '*'))
    print(myFormatPrint('用户名：', 15, align='r', symbol = ' ') + response['userinfo']['username'])
    print(myFormatPrint('登录信息：', 15, align='r', symbol = ' ') + response['reply_msg'])
    print(myFormatPrint('全名：', 15, align='r', symbol = ' ') + response['userinfo']['fullname'])
    print(myFormatPrint('账户余额：', 15, align='r', symbol = ' ') + str(int(response['userinfo']['balance'])//100)+'元'+str(int(response['userinfo']['balance'])%100)+'分')
    print(myFormatPrint('累计时长：', 15, align='r', symbol = ' ') + convertTime(online_information['rows'][0]['total_ipv4_volume'], 'S'))
    print(myFormatPrint('当前套餐：', 15, align='r', symbol = ' ') + response['userinfo']['service_name'])
    print(myFormatPrint('所在区域：', 15, align='r', symbol = ' ') + response['userinfo']['area_name'])
    print(myFormatPrint('', 35, align='l', symbol = '*'))

def printState(online_information, total_time):
    print(myFormatPrint('', 35, align='l', symbol = '*'))
    print(myFormatPrint('用户名：', 15, align='r', symbol = ' ') + online_information['rows'][0]['username'])
    print(myFormatPrint('登录信息：', 15, align='r', symbol = ' ') + online_information['rows'][0]['area_type_name'])
    print(myFormatPrint('全名：', 15, align='r', symbol = ' ') + online_information['rows'][0]['fullname'])
    print(myFormatPrint('累计时长：', 15, align='r', symbol = ' ') + convertTime(total_time['rows'][0]['total_ipv4_volume'], 'S'))
    print(myFormatPrint('IP地址：', 15, align='r', symbol = ' ') + long2ip(online_information['rows'][0]['user_ipv4']))
    print(myFormatPrint('MAC地址：', 15, align='r', symbol = ' ') + online_information['rows'][0]['mac'])
    print(myFormatPrint('当前套餐：', 15, align='r', symbol = ' ') + online_information['rows'][0]['service_name'])
    print(myFormatPrint('所在区域：', 15, align='r', symbol = ' ') + online_information['rows'][0]['area_name'])
    print(myFormatPrint('', 35, align='l', symbol = '*'))

if __name__ == '__main__':
    ## hyperparameters
    parser = argparse.ArgumentParser(description='南京大学校园网认证')
    parser.add_argument('-do', type=str, default='l', help='用来指定登录login，登出logout和查询')
    parser.add_argument('-user', type=str, default='', help='用户名')
    parser.add_argument('-passwd', type=str, default='', help='密码')
    args = parser.parse_args()
    
    if args.do in ['login','Login', 'l']:
        response = loginRequest(args.user, args.passwd)
        if response is None:
            print('请检查网络连接或检查用户名和密码')
        else:
            response = ast.literal_eval(response)
            if response['reply_code'] != 1:
                print('请检查网络连接或检查用户名和密码')
                print('服务器信息：', response['reply_msg'])
            else:
                time.sleep(2)
                printLoginInformation(response)
    if args.do in ['logout','Logout', 'exit','o']:
        response = logoutRequest()
        if response is None:
            pass
        else:
            response = ast.literal_eval(response)
            if response['reply_code'] != 101:
                print('请检查网络连接或服务器信息')
                print('服务器信息：', response['reply_msg'])
            else:
                print(myFormatPrint('', 35, align='l', symbol = '*'))
                print(myFormatPrint('服务器返回码：', 15, align='r', symbol = ' ')+str(response['reply_code']))
                print(myFormatPrint('当前状态：', 15, align='r', symbol = ' ')+response['reply_msg'])
                print(myFormatPrint('', 35, align='l', symbol = '*'))
    if args.do in ['i','I']:
        total_time_resp = getInformation()
        online_info_resp = getOnline()
        if total_time_resp is None or online_info_resp is None:
            print('请检查网络连接')
        else:
            total_time = ast.literal_eval(total_time_resp)
            online_information = ast.literal_eval(online_info_resp)
            if total_time['reply_code'] == 0 and online_information['reply_code'] == 0:
                printState(online_information, total_time)
            else :
                print('未登录校园网')
                print('服务器信息：', online_information['reply_msg'])
