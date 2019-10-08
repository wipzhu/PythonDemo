import re

import requests
from lxml import etree
from op_mysql import OperateMysql


def crawl_main(s_index):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    res = requests.get('https://movie.douban.com/top250?start=' + str(s_index), headers=req_header)
    if res.status_code == requests.codes.ok:
        doc = etree.HTML(res.text)
        ol = doc.xpath('//ol[@class="grid_view"]/li')

        # 实例化数据库操作类
        op_mysql = OperateMysql()

        i = 0
        for data in ol:
            rank = s_index + i + 1

            # 封面图片地址
            cover_pic_url = data.xpath('./div[@class="item"]/div[@class="pic"]/a/img/@src')[0]
            # 电影简介地址
            summary_url = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/@href')[0]
            title = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]'
                               '/a/span[@class="title"]/text()')
            # print(title[0])
            if len(title) >= 2:
                movie_name = title[0] + title[1]
            else:
                movie_name = title[0]

            staff_and_type = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p/text()')
            # 演职人员
            staff = staff_and_type[0].replace('\n', '').replace(' ', '').replace('\xa0', ' ')
            # 年代/类型
            age_type = staff_and_type[1].replace('\n', '').replace(' ', '').replace('\xa0', ' ')
            # 评分
            score = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                               '/div[@class="star"]/span[2]/text()')[0]
            # 评分人数
            people = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                                '/div[@class="star"]/span[4]/text()')[0]
            people_num = re.findall('\d+', people)[0]

            # 描述
            quote = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                               '/p[@class="quote"]/span[@class="inq"]/text()')
            if quote:
                quote = quote[0]
            else:
                quote = ''
            # print(quote + '\n')

            # -------------------- 写入数据库 --------------------
            # CREATE TABLE `douban_movie_top250` (
            # 	`id` INT ( 11 ) UNSIGNED NOT NULL AUTO_INCREMENT,
            # 	`rank` VARCHAR ( 10 ) NOT NULL COMMENT '排名',
            # 	`movie_name` VARCHAR ( 150 ) NOT NULL DEFAULT '' COMMENT '电影名称',
            # 	`staff` VARCHAR ( 180 ) NOT NULL DEFAULT '' COMMENT '演职人员',
            # 	`age_type` VARCHAR ( 120 ) NOT NULL DEFAULT '' COMMENT '年代/类型',
            # 	`score` VARCHAR ( 20 ) NOT NULL DEFAULT '' COMMENT '豆瓣评分',
            # 	`people_num` VARCHAR ( 50 ) NOT NULL DEFAULT '' COMMENT '评分人数',
            # 	`quote` VARCHAR ( 255 ) NOT NULL DEFAULT '' COMMENT '描述',
            # 	`cover_pic_url` VARCHAR ( 255 ) NOT NULL DEFAULT '' COMMENT '封面图片地址',
            # 	`summary_url` VARCHAR ( 255 ) NOT NULL DEFAULT '' COMMENT '简介地址',
            # PRIMARY KEY ( `id` )
            # ) ENGINE = MyISAM AUTO_INCREMENT = 100001 DEFAULT CHARSET = utf8;

            ins_data = {'rank': 'No.' + str(rank), 'movie_name': movie_name,
                        'staff': staff, 'age_type': age_type,
                        'score': score, 'people_num': people_num, 'quote': quote,
                        'cover_pic_url': cover_pic_url, 'summary_url': summary_url}
            # print(ins_data)

            op_mysql.add_data('douban_movie_top250', ins_data)

            # -------------------- 写入文件 --------------------
            # with open('./豆瓣/电影评分top250.txt', 'a', encoding='utf-8') as f:
            #     f.write('NO.' + str(rank) + '\n')
            #     f.write('电影名称：\   t' + movie_name + '\n')
            #     f.write('演职人员：\t' + staff + '\n')
            #     f.write('年代/类型：\t' + age_type + '\n')
            #     f.write('豆瓣评分：\t' + score + '分\n')
            #     f.write('评分人数：\t' + people_num + '\n')
            #     f.write('描    述：\t' + quote + '\n')
            #     f.write('封面地址：\t' + cover_pic_url + '\n')
            #     f.write('简介地址：\t' + summary_url)
            #     f.write('\n\n' + ('==' * 35) + '\n\n')

            i += 1


for i in range(10):
    print('-' * 50 + '开始爬取第' + str(i + 1) + '页...' + '-' * 50)
    crawl_main(25 * i)
    # break
