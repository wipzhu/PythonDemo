import re
import requests
from lxml import etree


def main_fun(crawl_url):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    host_url = 'http://www.jinyongwang.com'
    #################################### 以下为按书名导出 ###############################
    novel_dir = './金庸武侠小说集2/'
    result = requests.get(crawl_url, headers=req_header)
    if result.status_code == requests.codes.ok:
        s = etree.HTML(result.text)
        li_list = s.xpath('//*[@class="booklist"]/ul[2]/li')

        for li in li_list:
            # 书的的地址
            book_href = li.xpath('./p[2]/a/@href')[0]
            # 获取书名
            book_name = li.xpath('./p[2]/a/text()')[0]
            book_name = book_name.replace('小说', '')
            # 拼装每本小说的路径地址
            book_url = host_url + book_href
            # 获取章节页面信息
            chapter_result = requests.get(book_url, headers=req_header)
            if chapter_result.status_code == requests.codes.ok:
                # 章节列表页内容
                chapter_content = etree.HTML(chapter_result.text)
                chapter_li_list = chapter_content.xpath('//*[@class="mlist"]/li')
                with open(novel_dir + book_name + '.txt', 'w', encoding='utf-8') as f:
                    print('正在写入---【' + book_name + '】')
                    for chapter_li in chapter_li_list:
                        # 章节的相对地址
                        chapter_href = chapter_li.xpath('./a/@href')[0]
                        # 获取章节名
                        chapter_name = chapter_li.xpath('./a/text()')[0]
                        chapter_url = host_url + chapter_href
                        # 获取每个章节的内容
                        chapter_result = requests.get(chapter_url, headers=req_header)
                        if chapter_result.status_code == requests.codes.ok:
                            # 获取章节内容批次写入
                            last_content = chapter_result.text
                            last_re = re.compile(r'<p>(.*?)<p>', re.DOTALL)
                            last_list = re.findall(last_re, last_content)
                            # print(last_list)
                            # 先写入章节名
                            f.write('\n\n' + chapter_name + '\n\n\n')
                            # 写入每个章节的内容
                            for last in last_list:
                                # 全角空格进行段落缩进
                                f.write('　　' + last + "\n")
        #################################### 以上为按书名导出 ###############################
        #################################### 以下为按章节导出 ###############################
        # novel_dir = './金庸武侠小说集/'
        # result = requests.get(crawl_url, headers=req_header)
        # if result.status_code == requests.codes.ok:
        # content = result.text
        # # 小说路径(新修版)
        # url_re = re.compile(r'<p class="img pu_bookrotate"><a href="(/n.*?)">', re.DOTALL)
        # urls = re.findall(url_re, content)
        # for url in urls:
        #     # 拼装每本小说的路径地址
        #     book_url = host_url + url
        #     # 获取章节页面信息
        #     chapter_result = requests.get(book_url, headers=req_header)
        #     if chapter_result.status_code == requests.codes.ok:
        #         # 章节列表页内容
        #         chapter_content = chapter_result.text
        #         book_name_re = re.compile(r'<h1 class="title"><span>(.*?)小说.*?')
        #         # 书名
        #         book_name = re.findall(book_name_re, chapter_content)[0]
        #         # 章节名
        #         chapter_title_re = re.compile(r'<li><a href=".*?">(.*?)</a></li>', re.DOTALL)
        #         chapter_title_list = re.findall(chapter_title_re, chapter_content)
        #         # 章节地址
        #         chapter_url_re = re.compile(r'<li><a href="(.*?)">.*?</a></li>', re.DOTALL)
        #         chapter_url_list = re.findall(chapter_url_re, chapter_content)
        #         # 遍历章节地址获取每个章节的内容
        #         for i in range(len(chapter_url_list)):
        #             print('正在写入----' + book_name + '【' + chapter_title_list[i] + '】...')
        #             # 文件名格式为 书名【章节名】
        #             with open(novel_dir + book_name + '【' + chapter_title_list[i] + '】.txt', 'w', encoding='utf-8') as f:
        #                 # 写入章节名
        #                 f.write(chapter_title_list[i])
        #                 # 获取每个章节的内容
        #                 last_url = host_url + chapter_url_list[i]
        #                 last_result = requests.get(last_url, headers=req_header)
        #                 if last_result.status_code == requests.codes.ok:
        #                     last_content = last_result.text
        #                     last_re = re.compile(r'<p>(.*?)<p>', re.DOTALL)
        #                     last_list = re.findall(last_re, last_content)
        #                     # 写入每个章节的内容
        #                     for last in last_list:
        #                         f.write("\n\n" + last)
        #################################### 以上为按章节导出 ###############################

main_fun('http://www.jinyongwang.com/book')
