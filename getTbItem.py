#coding:utf-8
__author__ = 'lai'

import requests
from bs4 import BeautifulSoup
import re
import sys
import getopt
import csv
import os

class TbProduct(object):

    def __init__(self, title, shop, trans, comment):
        self.title = title
        self.shop = shop
        self.trans = trans
        self.comment = comment


def get_soup(url):
    request = requests.get(url)
    return BeautifulSoup(request.text)

def get_product_list(soup):
    temp_list = []
    for product in soup.select('.product  '):
        if len(product.select('.productImg-wrap')) > 0:
            try:
                tb_product = TbProduct(product.select('.productTitle')[0].select('a')[0].text, product.select('.productShop')[0].select('a')[0].text,
                                    product.select('.productStatus')[0].select('em')[0].text, product.select('.productStatus')[0].select('a')[0].text)
                temp_list.append(tb_product)
            except:
                print 'error : ', product

    return temp_list


def write_file(patch_name, product_list):

    with open(patch_name + '.csv', 'wb') as csvfile:
        spam_writer = csv.writer(csvfile, dialect='excel')
        for tb_product in product_list:
            try:
                spam_writer.writerow([tb_product.title.encode(code), tb_product.shop.encode(code), tb_product.trans.encode(code), tb_product.comment.encode(code)])
            except:
                pass

    print 'write', patch_name + '.csv done'


def usage():
    print 'get Tb item list Tool'
    print
    print 'Usage: getTbItem.py -k search_keyword -n save file name'
    print '-k --keyword          '
    print '-n --name=file_to_save'
    print
    print
    print 'Examples: '
    print u'getTbItem.py -k 珍珠 -n c:\\target'
    sys.exit(0)

init_url = u'https://list.tmall.com/search_product.htm?q='
page_pattern = re.compile(u'\D*?共(\d*)页\D*?')
page_num = 0
keyword = ''
patch_name = ''
code = 'utf-8'


if __name__ == '__main__':

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:k:n:', ['help', 'keyword', 'name'])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    if os.name == 'nt':
        code = 'gbk'

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-k', '--keyword'):
            keyword = unicode(a, code)
        elif o in ('-n', '--name'):
            patch_name = a
        else:
            assert False, 'Unhandled Option'

    print 'keyword', keyword, 'patch_name', patch_name

    soup = get_soup(init_url+keyword)
    try:
        page_num = int(re.findall(page_pattern, soup.select('.ui-page-skip')[0].text)[0])
    except:
        pass

    product_list = get_product_list(soup)

    if page_num > 1:
        for i in range(1, page_num):
            url = init_url + keyword + '&s=' + str(i*60)
            soup = get_soup(url)
            product_list += get_product_list(soup)

    write_file(patch_name, product_list)


