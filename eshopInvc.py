#coding:utf-8
__author__ = 'li.pei.jie'

import os
from selenium import webdriver
from time import sleep

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)

login_url = "https://192.168.50.4:4443/eshopadmin/faces/index.jsp"
login_nam = "li.pei.jie"
login_pass = "lai1983"

submit_elem = None

max_try_time = 20

driver.get(login_url)
inputs = driver.find_elements_by_tag_name("input")

results = []

for i in range(0, len(inputs)):
    elem = inputs[i]
    nam = elem.get_property("name")
    value = elem.get_property("value")
    if "name" in nam:
        elem.send_keys(login_nam)
    elif "password" in nam:
        elem.send_keys(login_pass)
    elif u"登录" in value:
        submit_elem = elem

submit_elem.click()



def readOrderKey(file_path):
    order_keys = []
    f = open(file_path)
    for line in f:
        key = line.strip()
        order_keys.append(key)

    f.close()
    return order_keys


def writResult(results, file_path):
    f = open(file_path, 'w')
    for line in results:
        f.write(line + '\n')

    f.close()
    return order_keys



order_keys = readOrderKey('order_keys.txt')

for i in range(0, len(order_keys)):
    try:
        order_key = order_keys[i]
        order_url = "https://192.168.50.4:4443/eshopadmin/faces/update_order_addr.jsp?order_key=" + order_key + "&ind=title"

        driver.get(order_url)

        but = driver.find_element_by_link_text(u"冲红")
        but.click()

        driver.switch_to_alert().accept()
        try_time = 0
        while True:
            alert_msg = driver.page_source
            if u"成功" in alert_msg:
                results.append(order_key+' : ok')
                print i, ':', order_key, 'ok,try_time', try_time
                break
            elif u"已有其他程序处理" in alert_msg:
                results.append(order_key+' : other prossing')
                print i, ':', order_key, 'other prossing'
                break
            elif u"不是有效" in alert_msg:
                results.append(order_key+' : not effective invc')
                print i, ':', order_key, 'not effective invc'
                break
            elif u"系统处理中" in alert_msg and try_time < max_try_time:
                try_time = try_time + 1
                sleep(2)
            elif try_time >= max_try_time:
                results.append(order_key+' : try to much')
                print i, ':', order_key, 'try to much'
                break
            else:
                results.append(order_key+' : other')
                print i, ':', order_key, 'other '
                break
    except:
        results.append(order_key+' : except')
        print i, ':', order_key,  'except'

writResult(results, 'results.txt')

driver.close()




