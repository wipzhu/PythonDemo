import requests
from lxml import etree


def crawl_main(s_index):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    res = requests.get('https://movie.douban.com/top250?start=' + str(s_index), headers=req_header)
    if res.status_code == requests.codes.ok:
        doc = etree.HTML(res.text)
        ol = doc.xpath('//ol[@class="grid_view"]/li')
        i = 0
        for data in ol:
            rank = s_index + i + 1

            # 封面图片地址
            cover_pic_url = data.xpath('./div[@class="item"]/div[@class="pic"]/a/img/@src')[0]
            # 电影简介地址
            subject_intro_url = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/@href')[0]
            title = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]'
                               '/a/span[@class="title"]/text()')
            print(title[0])

            staff_and_type = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p/text()')
            # 演职人员
            staff = staff_and_type[0].replace('\n', '').replace(' ', '')
            # 年代/类型
            age_type = staff_and_type[1].replace('\n', '').replace(' ', '')
            # 评分
            score = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                               '/div[@class="star"]/span[2]/text()')[0]
            # 评分人数
            people = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                                '/div[@class="star"]/span[4]/text()')[0]
            quote = data.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                               '/p[@class="quote"]/span[@class="inq"]/text()')[0]
            print(quote + '\n')

            with open('./豆瓣/电影评分top250.txt', 'a', encoding='utf-8') as f:
                f.write('NO.' + str(rank) + '\n')
                if len(title) >= 2:
                    f.write('电影名称：\t' + title[0] + title[1] + '\n')
                else:
                    f.write('电影名称：\t' + title[0] + '\n')
                f.write('演职人员：\t' + staff + '\n')
                f.write('年代/类型：\t' + age_type + '\n')
                f.write('豆瓣评分：\t' + score + '分\n')
                f.write('评分人数：\t' + people + '\n')
                if quote:
                    f.write('描    述：\t' + quote + '\n')
                f.write('封面地址：\t' + cover_pic_url + '\n')
                f.write('简介地址：\t' + subject_intro_url)
                f.write('\n\n' + ('==' * 35) + '\n\n')
            i += 1


for i in range(10):
    print('-' * 50 + '开始爬取第' + str(i) + '页...' + '-' * 50)
    crawl_main(25 * i)
    # break
