import re
import requests
from lxml import etree

req_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def spider_main(crawl_url, uuid, page):
    # 先获取诗词总页数
    result = requests.get(crawl_url, params={'page': 1, 'id': uuid}, headers=req_header)
    if result.status_code == requests.codes.ok:
        # 页面内容
        index_content = result.text
        all_page_re = re.compile(r'<span style=" background-color:#E1E0C7; border:0px; margin-top:22px; '
                                 r'width:auto;">/ (.*?)页</span', re.DOTALL)
        all_page = int(re.findall(all_page_re, index_content)[0])

        if page and isinstance(page, int) and page <= all_page and page >= 1:
            # page参数存在则只爬取当前页
            # c_url = crawl_url + '?page=' + str(page) + '&id=' + uuid
            crawl_by_per_page(crawl_url, uuid, page)
        else:
            for i in range(1, int(all_page) + 1):
                # 遍历爬取所有页
                crawl_by_per_page(crawl_url, uuid, i)


def crawl_by_per_page(crawl_url, uuid, page):
    c_page_res = requests.get(crawl_url, params={'page': str(page), 'id': uuid}, headers=req_header)
    c_page_content = etree.HTML(c_page_res.text)
    content_list = c_page_content.xpath('//*[@class="sons"]')
    # print(content_list)
    print('正在爬取第【' + str(page) + '】页...')
    for content in content_list:
        title = content.xpath('./div[@class="cont"]/p/a/b/text()')
        dynasty = content.xpath('./div[@class="cont"]/p[@class="source"]/a[1]/text()')
        author = content.xpath('./div[@class="cont"]/p[@class="source"]/a[2]/text()')
        comment = content.xpath(
            './div[@class="cont"]/div[@class="contson"]/p[1]/span[@style="font-family:SimSun;"]/text()')
        # print(comment)
        poem_c_list = content.xpath('./div[@class="cont"]/div[@class="contson"]')
        with open('./诗词爬取/' + author[0] + '•' + dynasty[0] + '.txt', 'a', encoding='utf-8') as f:
            # 写入诗词名
            f.write('\n\n' + '【' + title[0] + '】' + '\n')
            if comment:
                for com in comment:
                    # 写入诗词注释
                    f.write('\n' + com + '\n')

            if poem_c_list:
                for poem_c in poem_c_list:
                    c = poem_c.xpath('./p/text()')
                    if c:
                        pass
                    else:
                        c = content.xpath('./div[@class="cont"]/div[@class="contson"]/text()')

                for last in c:
                    # 写入诗词内容
                    f.write('\n' + last.replace('\n', ''))
            f.write("\n\n" + "==" * 50)
            print('\t\t《' + title[0] + '》写入完毕！')


# 诗词首页 https://so.gushiwen.org/authors/authorvsw.aspx?page=1&id=3b99a16ff2dd
host_url = 'https://so.gushiwen.org/authors/authorvsw.aspx'
# 苏轼
spider_main(host_url, '3b99a16ff2dd', page='all')
# 李白
# https://so.gushiwen.org/authors/authorvsw.aspx?page=6&id=b90660e3e492
# spider_main(host_url, 'b90660e3e492', page='all')
# 李清照
# https://so.gushiwen.org/authors/authorvsw.aspx?page=2&id=9cb3b7c0e4a0
# spider_main(host_url, '9cb3b7c0e4a0', page='all')
# 纳兰性德
# spider_main(host_url, '01611cc80faf', page='all')
# 陈寿
# spider_main(host_url, 'bc168825cd92', page='all')
# 王勃
# spider_main(host_url, 'e6b970da08cd', page='all')

