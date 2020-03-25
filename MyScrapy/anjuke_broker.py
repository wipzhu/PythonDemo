import json
import re
import time

import pymysql
import requests
import random

from lxml import etree


class AnjukeBrokerSpider():
    """安居客经纪人爬虫"""

    def __init__(self):
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        ]
        self.req_header = {
            'User-Agent': random.choice(self.user_agent_list)
        }
        self.cookie = {
            'Cookie': 'sessid=13DD1C54-3819-9142-050A-B0A82F111BBC; aQQ_ajkguid=6F942F31-11F7-5A95-472D-8EFD97F3CED3; lps=http%3A%2F%2Fshanghai.anjuke.com%2Ftycoon%2F%3Ffrom%3Dnavigation%25EF%25BC%258C%25E7%2588%25AC%25E4%25B8%25AD%25E4%25BB%258B%25E4%25BF%25A1%25E6%2581%25AF%7C; ctid=11; twe=2; 58tj_uuid=3e632b17-efb0-4f06-9e55-72e6b19f763f; wmda_uuid=002c3f7e4e14aca258a5d135397c15b2; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; als=0; ajk_member_captcha=71453eaf0101f721f654c8e754f3feb0; _ga=GA1.2.1638043374.1584935290; _gid=GA1.2.1558921645.1584935290; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1584953974; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1584953974; browse_comm_ids=990259; propertys=wzoiys-q7n75s_; wmda_session_id_6289197098934=1585035153349-48371f54-4ddb-17d9; init_refer=https%253A%252F%252Fwww.anjuke.com%252Fcaptcha-verify%252F%253Fcallback%253Dshield%2526from%253Dantispam%2526namespace%253Danjuke_c_pc%2526serialID%253D3223a70b99b31ec792da96e693674fd5_881e9f437b6d48a1ac087f6d31a6aafb%2526history%253DaHR0cHM6Ly9zaGFuZ2hhaS5hbmp1a2UuY29tL3R5Y29vbi8%25253D; new_uv=10; new_session=0; __xsptplusUT_8=1; __xsptplus8=8.12.1585035153.1585037612.19%232%7Cwww.baidu.com%7C%7C%7C%7C%23%23A3QsYwvj_nE8i5qSkrh8XS1dSXIMnELe%23; xzfzqtoken=NIHhOswqixd8PoqSmqobYivQ07lsa25d9xVXvkQmuNXTFS7f1ijdokKJzwmNhbogin35brBb%2F%2FeSODvMgkQULA%3D%3D'
        }
        # 设置代理,原文链接：https://www.cnblogs.com/z-x-y/p/9355223.html
        # 如果代理需要验证，只需要在前面加上用户名密码，如下所示
        # proxy='username:password@124.243.226.18:8888'
        # 阿布云代理隧道配置
        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": 'http-dyn.abuyun.com',
            "port": '9020',
            "user": 'H1PI166TUMLU94SD',
            "pass": '93D0180B4F7CE78C',
        }
        self.proxy = {
            "http": self.proxyMeta,
            "https": self.proxyMeta,
        }

        # self.proxy = {
        #     "http": 'http://125.110.112.46:9000',
        #     "https": 'https://222.94.148.166:808',
        # }
        # self.maxPage = 2

    def get_brokers_list(self, broker_list_url, area):
        """获取经纪人列表"""
        # 地区处理
        if area == 'pudong':
            area_type = 1
            area_name = '浦东'
        elif area == 'minhang':
            area_type = 2
            area_name = '闵行'
        elif area == 'baoshan':
            area_type = 3
            area_name = '宝山'
        elif area == 'xuhui':
            area_type = 4
            area_name = '徐汇'
        elif area == 'songjiang':
            area_type = 5
            area_name = '松江'
        elif area == 'jiading':
            area_type = 6
            area_name = '嘉定'
        elif area == 'jingan':
            area_type = 7
            area_name = '静安'
        elif area == 'putuo':
            area_type = 8
            area_name = '普陀'
        elif area == 'yangpu':
            area_type = 9
            area_name = '杨浦'
        elif area == 'hongkou':
            area_type = 10
            area_name = '虹口'
        elif area == 'changning':
            area_type = 11
            area_name = '长宁'
        elif area == 'huangpu':
            area_type = 12
            area_name = '黄浦'
        elif area == 'qingpu':
            area_type = 13
            area_name = '青浦'
        elif area == 'fengxian':
            area_type = 14
            area_name = '奉贤'
        elif area == 'jinshan':
            area_type = 15
            area_name = '金山'
        elif area == 'chongming':
            area_type = 16
            area_name = '崇明'
        elif area == 'shanghaizhoubian':
            area_type = 17
            area_name = '上海周边'
        else:
            area_type = 0
            area_name = '全部'

        # result = requests.get(broker_list_url, headers=self.req_header, proxies=self.proxy)
        result = requests.get(broker_list_url, headers=self.req_header)
        # print(result.content)
        print(result.status_code)
        broker_list = []
        if result.status_code == requests.codes.ok:
            print('---------请求成功---------')
            doc = etree.HTML(result.content)
            div_list = doc.xpath('//div[@id="list-content"]/div[@class="jjr-itemmod"]')
            print(div_list)

            for div in div_list:
                # 经纪人一些基本信息
                broker_name = div.xpath('./a/@title')[0]
                # print(broker_name)
                detail_url = div.xpath('./a/@href')[0]
                broker_id = re.findall('jjr-\d+', detail_url)[0]
                broker_id = broker_id.replace('jjr-', '')
                avatar_url = div.xpath('./a/img/@src')[0]
                # 门店信息
                company_obj = div.xpath('./div[@class="jjr-info"]/p[@class="jjr-desc"]')[0]
                shop_name = company_obj.xpath('./a/text()')
                if shop_name:
                    shop_name = shop_name[0]
                else:
                    shop_name = ''
                shop_address = company_obj.xpath('./span[2]/text()')
                if shop_address:
                    shop_address = shop_address[0]
                else:
                    shop_address = ''

                print('-----' + broker_name + '---开始爬取手机号-----')
                # 根据detail_url爬取经纪人的电话号码,需要获取token和prop_city_id
                # 示例:token=7d995c3ada4b7ceca210b91fb649c56a
                phone_no = self.get_phone_no(detail_url)
                # print(phone_no)
                # return


                item = {'broker_name': broker_name, 'broker_id': broker_id, 'detail_url': detail_url,
                        'avatar_url': avatar_url, 'shop_name': shop_name, 'shop_address': shop_address,
                        'phone_no': phone_no, 'area_type': area_type, 'area_name': area_name}

                # 数据入库:爬取一条插入一条
                self.add_data('anjuke_brokers', item)
                print('-----' + broker_name + '---入库成功-----')
                print('\n')

                # 休眠一秒
                time.sleep(1)

                broker_list.append(item)
        return broker_list

    def get_phone_no(self, detail_url):
        """获取经纪人的电话号码"""
        # 根据detail_url爬取经纪人的电话号码,需要获取token和prop_city_id
        # 示例:token=7d995c3ada4b7ceca210b91fb649c56a

        # 先获取broker_id
        broker_id = re.findall('jjr-\d+', detail_url)[0]
        broker_id = broker_id.replace('jjr-', '')
        # print(broker_id)

        # res = requests.get(detail_url, cookies=self.cookie, headers=self.req_header, proxies=self.proxy)
        res = requests.get(detail_url, cookies=self.cookie, headers=self.req_header)
        if res.status_code == requests.codes.ok:
            print('-----手机号页面请求成功，开始爬取-----')
            doc = etree.HTML(res.content)
            js_obj = doc.xpath('//script[@type="text/javascript"]')[5]
            # normalize-space 去掉空格和换行符
            js_str = str(js_obj.xpath('normalize-space(./text())').replace(' ', ''))
            js_str = str(js_str)
            # print(js_str)
            time.sleep(1)

            t_pat = "'token':'(.*)','prop_city_id'"
            c_pat = "'prop_city_id':'(\d+)','isRequestQRCode'"
            token = re.findall(t_pat, js_str)[0]
            prop_city_id = re.findall(c_pat, js_str)[0]
            # print(token)
            # print(prop_city_id)
            # return

            # 请求host
            regular = re.compile(r'[a-zA-Z]+://[^\s]*[.com]/')
            detail_host = re.findall(regular, detail_url)[0]

            # 获取到token之后请求获取电话号码
            # 拼接电话号码的请求地址
            phone_url = detail_host + 'v3/ajax/broker/phone/?broker_id=' + str(broker_id) + '&token=' + str(
                token) + '&prop_city_id=' + str(prop_city_id) + '&captcha='
            # print(phone_url)

            print('-----token获取成功，开始请求手机号-----')
            # jsons = requests.get(phone_url, cookies=self.cookie, headers=self.req_header, proxies=self.proxy)
            jsons = requests.get(phone_url, cookies=self.cookie, headers=self.req_header)
            # print(jsons)
            loaded_json = json.loads(jsons.text)
            # print(loaded_json)

            # in 判断json中是否存在这个key
            if 'val' in loaded_json:
                phone_no = str(loaded_json['val']).replace(' ', '')
                print('-----手机号获取成功!-----')
            else:
                phone_no = ''

            # 返回电话号码
            return phone_no

    def __get_conn(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test_demo',
                                        charset='utf8')
        except pymysql.Error as e:
            print(e, '数据库连接失败')

    def __close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e, '数据库连接关闭失败')

    def add_data(self, table_name, data):
        """插入数据"""
        if table_name == 'anjuke_brokers':
            ins_data = [data['broker_name'], data['broker_id'], data['detail_url'], data['avatar_url'],
                        data['shop_name'],
                        data['shop_address'], data['phone_no']]
            sql = """insert into anjuke_brokers (`broker_name`, `broker_id`, `detail_url`, `avatar_url`, `shop_name`, `shop_address`, `phone_no`) values (%s,%s,%s,%s,%s,%s,%s);"""

        else:
            ins_data = []
            sql = ''

        # print(data['rank'])
        # print(data['movie_name'])
        # print(sql)
        # return

        self.__get_conn()
        cursor = self.conn.cursor()
        try:
            # print(ins_data)
            # return
            cursor.execute(sql, ins_data)
            self.conn.commit()
        except AttributeError as e:
            print(e, '数据失败')
            # self.conn.rollback()
            return 0
        except pymysql.DataError as e:
            print(e, '数据插入失败')
            # self.conn.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()
            self.__close_conn()


def main():
    # print('取消注释以执行对应代码~~')
    # return
    spider = AnjukeBrokerSpider()

    # 爬取某页经纪人列表
    page = 1
    area = 'pudong'
    # area == 'pudong'
    # area == 'minhang'
    # area == 'baoshan'
    # area == 'xuhui'
    # area == 'songjiang'
    # area == 'jiading'
    # area == 'jingan'
    # area == 'putuo'
    # area == 'yangpu'
    # area == 'hongkou'
    # area == 'changning'
    # area == 'huangpu'
    # area == 'qingpu'
    # area == 'fengxian'
    # area == 'jinshan'
    # area == 'chongming'
    # area == 'shanghaizhoubian'

    while True:
        if page >= 50:
            print('-----pudong-本地区爬取完成-----')
            break

        print('---正在爬取第【' + str(page) + '】页...')
        broker_list = spider.get_brokers_list('https://shanghai.anjuke.com/tycoon/' + area + '/p' + str(page) + '/', area)
        print('---第【' + str(page) + '】页爬取完毕。')

        # 页码 +1
        page += 1

    # # 爬取经纪人电话号码
    # detail_url = 'https://yijufangyou1.anjuke.com/gongsi-jjr-5369884/'
    # phone_no = spider.get_phone_no(detail_url)

    # page = 1
    # while True:
    #     list_info = spider.get_brokers_list('https://shanghai.anjuke.com/tycoon/p' + str(page) + '/')
    #     print(list_info)
    #     # 本页爬取数目 < 30 或 页码 > 指定的最大页码
    #     if len(list_info) < 30 or page > spider.maxPage:
    #         print('***' * 20 + '爬取完成！')
    #         break
    #
    #     # 页码 +1
    #     page += 1


if __name__ == "__main__":
    main()
