# 歌单地址，歌单内歌曲列表为ajax获取(去掉 /#)
# https://music.163.com/#/playlist?id=2232237850
# https://music.163.com/#/playlist?id=2353471182
# https://music.163.com/#/playlist?id=2331414535

# 歌曲地址(去掉 /#)
# https://music.163.com/#/song?id=1393048618

# 歌曲评论地址
# https://music.163.com/weapi/v1/resource/comments/R_SO_4_1393048618?csrf_token=
import json
import re

import requests
from lxml import etree

from netease_cloud_music_decrypt import NeteaseCloudMusicDecrypt
from op_mysql import OperateMysql


class NeteaseCloudMusicSpider():

    # 技术实现参考地址：
    # https://blog.csdn.net/csdnsevenn/article/details/80746589
    # https://blog.csdn.net/weixin_33816946/article/details/88834274

    def __init__(self):
        self.req_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/76.0.3809.132 Safari/537.36'
        }
        # 每页获取条数
        self.pagesize = 20
        # self.form_data = {'params': 'rOI9TRJfe1kpYofPQHYiEkAX72qNRULwxp2XndEhWs6BeHvA+7vEkH8mcIbrHXrmjkxJaNyNxUihud11j/yxG2jn71nXGqPqLIwmUi7W2iqpzPHFlKrUBnh0w721e6DTlmRyT4lqfGAXv81sCM8em2P0tPpx227PWnZRM/346yWCtL4VLMc86usfpNnc59cR','encSecKey': '285e0ced32d186c418af7b4b8da69f2bfd79c4f551126ae5ce35a36dd3722192b854227f27f9b8a8a7bf50d41fe519974bc14561d2ad8f687ad156530ce6293bf63086de591d6af85e465992918b7e7fea64659df37c13c5cf2c0226447d4b86a6325fb22367aef9f20d0f2a684fe07cf2d65b02ce7cf05b58aebc141fa3056a'}
        # self.form_data = {'params': 'XiPJr+QBh8y08qmLTJFGzx6lqOYr/Kt599ojZCdBFfaH2tTqv0sxX8c5f6mg4QEiy0eWfq8c0lKmGlLAfS/MVrUKjqP5RS859HvJbiSBnIMqk4obaW6+9DUB09YaD9t5qDpvbcNRmj1uIaCT2S2SmzBmd3fz6zlrPiliGsFuEzbwLrmohIFvPExCH1exV3QQ','encSecKey': '4f5ff4756ebd9d357004d06b4e67773008285aa3e3714ad5e304edb6b0fb46f9f0f5f03c9a326d346ceb344e888d30e3c3006a4c5e4d665e20729af40e822948f5f9d214a331a10c252fe0e51e17963c1657b72b6d21251293bdd77858a9b35c816950abd5afb1e06102188d2b13e3f33d4d3ec21ea590aa963e0d779e432325'}

    def get_songs_in_list(self, playlist_id):
        """获取某个歌单内的所有歌曲"""
        song_list_url = 'https://music.163.com/playlist?id=' + playlist_id

        result = requests.get(song_list_url, headers=self.req_header)
        # print(result.content)
        song_list = []
        if result.status_code == requests.codes.ok:
            doc = etree.HTML(result.content)
            li_list = doc.xpath('//div[@id="song-list-pre-cache"]/ul[@class="f-hide"]/li')
            # print(li_list)
            for li in li_list:
                song_name = li.xpath('./a/text()')[0]
                song_url = li.xpath('./a/@href')[0]
                song_id = re.findall('\d+', song_url)[0]
                item = {'song_name': song_name, 'song_id': song_id}
                # print(song_id)
                # print(song_url)
                song_list.append(item)

        # print(song_list)
        return song_list

    def get_comment_list(self, song_id):
        """获取某个歌曲下的评论以及对应的点赞信息"""
        # song_url = 'https://music.163.com/song?id=' + song_id
        # print(song_id)
        comment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + song_id + '?csrf_token='

        # 实例化数据库操作类
        op_mysql = OperateMysql()

        # 爬取歌曲详细信息
        print('---开始爬取歌曲信息：' + song_id)
        song_info = self.get_song_info(song_id)
        print(song_info)
        song_name = song_info['song_name']
        artist_name = song_info['artist_name']
        print('---歌曲信息爬取完成：' + '【' + song_name + '】 | ' + song_id)

        print('---开始爬取评论：' + '【' + song_name + '】 | ' + song_id)

        page = 1
        while True:
            print('---正在爬取第【' + str(page) + '】页评论...')
            # 获取分页数据，涉及解密，见class NeteaseCloudMusicDecrypt()
            if page <= 1:
                decrypt = NeteaseCloudMusicDecrypt(song_id, (page - 1) * self.pagesize, self.pagesize, 'true')
            else:
                decrypt = NeteaseCloudMusicDecrypt(song_id, (page - 1) * self.pagesize, self.pagesize, 'false')
            params = decrypt.get_param()
            encSecKey = decrypt.get_encSecKey()
            form_data = {'params': params.decode(), 'encSecKey': encSecKey}

            jsons = requests.post(comment_url, data=form_data, headers=self.req_header)
            loaded_json = json.loads(jsons.text)
            # print(loaded_json)

            # 热门评论--- in 判断json中是否存在这个key
            if 'hotComments' in loaded_json:
                for hotComment in loaded_json['hotComments']:
                    user_id = str(hotComment['user']['userId'])
                    nickname = hotComment['user']['nickname']
                    avatar_url = hotComment['user']['avatarUrl']
                    comment_id = str(hotComment['commentId'])
                    content = str(hotComment['content'])
                    time = str(hotComment['time'])
                    liked_count = str(hotComment['likedCount'])
                    is_hot = 1

                    # 数据入库
                    ins_data = {'song_id': song_id, 'song_name': song_name, 'artist_name': artist_name,
                                'user_id': user_id, 'nickname': nickname, 'avatar_url': avatar_url,
                                'comment_id': comment_id, 'content': content, 'time': time,
                                'liked_count': liked_count, 'is_hot': is_hot}
                    # print(ins_data)
                    op_mysql.add_data('netease_cloud_music_comment', ins_data)

                    if hotComment['beReplied']:
                        for reply in hotComment['beReplied']:
                            re_user_id = str(reply['user']['userId'])
                            re_nickname = reply['user']['nickname']
                            re_avatar_url = reply['user']['avatarUrl']
                            re_comment_id = str(reply['beRepliedCommentId'])
                            re_content = str(reply['content'])

                            # 数据入库
                            ins_data = {'song_id': song_id, 'song_name': song_name, 'comment_id': comment_id,
                                        're_user_id': re_user_id, 're_nickname': re_nickname,
                                        're_avatar_url': re_avatar_url, 're_comment_id': re_comment_id,
                                        're_content': re_content}
                            op_mysql.add_data('netease_cloud_music_comment_reply', ins_data)

                # print('*' * 20 + '以下为【热门评论】' + '*' * 20)
                # for hotComment in loaded_json['hotComments']:
                #     # print(hotComment)
                #     print('-' * 30)
                #     print('用户ID：' + str(hotComment['user']['userId']))
                #     print('用户昵称：' + hotComment['user']['nickname'])
                #     print('头像地址：' + hotComment['user']['avatarUrl'])
                #     print('评论ID：' + str(hotComment['commentId']))
                #     print('评论内容：' + hotComment['content'].replace('\n', ' '))
                #     print('评论时间：' + str(hotComment['time']))
                #     print('点赞数：' + str(hotComment['likedCount']))
                #     if hotComment['beReplied']:
                #         print('评论回复：')
                #         for reply in hotComment['beReplied']:
                #             print(' ' * 8 + '用户 ID：' + str(reply['user']['userId']))
                #             print(' ' * 8 + '用户昵称：' + reply['user']['nickname'])
                #             print(' ' * 8 + '头像地址' + reply['user']['avatarUrl'])
                #             print(' ' * 8 + '回复 ID：' + str(reply['beRepliedCommentId']))
                #             print(' ' * 8 + '回复内容：' + str(reply['content']))
                #     print('-' * 30, end='\n')

            # 最新评论--- in 判断json中是否存在这个key
            if 'comments' in loaded_json:
                for comment in loaded_json['comments']:
                    user_id = str(comment['user']['userId'])
                    nickname = comment['user']['nickname']
                    avatar_url = comment['user']['avatarUrl']
                    comment_id = str(comment['commentId'])
                    content = str(comment['content'])
                    time = str(comment['time'])
                    liked_count = str(comment['likedCount'])
                    is_hot = 0

                    # 数据入库
                    ins_data = {'song_id': song_id, 'song_name': song_name, 'artist_name': artist_name,
                                'user_id': user_id, 'nickname': nickname, 'avatar_url': avatar_url,
                                'comment_id': comment_id, 'content': content, 'time': time,
                                'liked_count': liked_count, 'is_hot': is_hot}
                    # print(ins_data)
                    op_mysql.add_data('netease_cloud_music_comment', ins_data)

                    if comment['beReplied']:
                        for reply in comment['beReplied']:
                            re_user_id = str(reply['user']['userId'])
                            re_nickname = reply['user']['nickname']
                            re_avatar_url = reply['user']['avatarUrl']
                            re_comment_id = str(reply['beRepliedCommentId'])
                            re_content = str(reply['content'])

                            # 数据入库
                            ins_data = {'song_id': song_id, 'song_name': song_name, 'comment_id': comment_id,
                                        're_user_id': re_user_id, 're_nickname': re_nickname,
                                        're_avatar_url': re_avatar_url, 're_comment_id': re_comment_id,
                                        're_content': re_content}
                            op_mysql.add_data('netease_cloud_music_comment_reply', ins_data)

                # print('+' * 20 + '以下为【最新评论】' + '+' * 20)
                # for comment in loaded_json['comments']:
                #     print('-' * 30)
                #     print('用户 ID：' + str(comment['user']['userId']))
                #     print('用户昵称：' + comment['user']['nickname'])
                #     print('头像地址：' + comment['user']['avatarUrl'])
                #     print('评论 ID：' + str(comment['commentId']))
                #     print('评论内容：' + comment['content'].replace('\n', ' '))
                #     print('评论时间：' + str(comment['time']))
                #     print('点 赞 数：' + str(comment['likedCount']))
                #     if comment['beReplied']:
                #         # print('评论回复：')
                #         for reply in comment['beReplied']:
                #             print(' ' * 8 + '用户 ID：' + str(reply['user']['userId']))
                #             print(' ' * 8 + '用户昵称：' + reply['user']['nickname'])
                #             print(' ' * 8 + '头像地址' + reply['user']['avatarUrl'])
                #             print(' ' * 8 + '回复 ID：' + str(reply['beRepliedCommentId']))
                #             print(' ' * 8 + '回复内容：' + str(reply['content']))
                #     print('-' * 30, end='\n')

            print('---第【' + str(page) + '】页评论爬取完毕。')

            # 页码 +1
            page += 1

            if len(loaded_json['comments']) < self.pagesize:
                print('---评论爬取完成：' + '【' + song_name + '】 | ' + song_id)
                break

    def get_song_info(self, song_id):
        song_url = 'https://music.163.com/song?id=' + song_id

        result = requests.get(song_url, headers=self.req_header)
        # print(result.content)
        if result.status_code == requests.codes.ok:
            # print(result.content.decode())
            # return
            doc = etree.HTML(result.content)

            # song_id
            song_id = doc.xpath('//div[@id="content-operation"]/@data-rid')[0]
            # 歌曲名称
            song_name = doc.xpath('//div[@class="tit"]/em/text()')[0]
            # 歌曲子名称
            sub_name = doc.xpath('//div[@class="subtit f-fs1 f-ff2"]/text()')
            if sub_name:
                sub_name = sub_name[0]
            else:
                sub_name = ''

            # 歌手和专辑信息的HTML元素
            list_info = doc.xpath('//div[@class="cnt"]/p[@class="des s-fc4"]')

            # 歌手信息
            artist_name = list_info[0].xpath('./span/a/text()')[0]
            artist_url = list_info[0].xpath('./span/a/@href')[0]
            artist_id = re.findall('\d+', artist_url)[0]

            # 专辑信息
            album_name = list_info[1].xpath('./a/text()')[0]
            album_url = list_info[1].xpath('./a/@href')[0]
            album_id = re.findall('\d+', album_url)[0]

            song_info = {
                'song_id': song_id, 'song_name': song_name, 'sub_name': sub_name,
                'artist_name': artist_name, 'artist_url': artist_url, 'artist_id': artist_id,
                'album_name': album_name, 'album_url': album_url, 'album_id': album_id,
            }

            return song_info


def main():
    spider = NeteaseCloudMusicSpider()

    # # 爬取歌曲详细信息
    # song_info = spider.get_song_info('30431366')
    # print(song_info)

    # 爬取某个歌单中的歌曲列表
    song_list = spider.get_songs_in_list('2331414535')
    song_list = song_list[3:]
    # print(song_list)
    # return

    # 爬取某个歌曲中的评论列表
    for song in song_list:
        spider.get_comment_list(song['song_id'])


main()

# ------------------------------建表语句---------------------------------
# CREATE TABLE `netease_cloud_music_comment` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `song_id` varchar(10) NOT NULL DEFAULT '' COMMENT '歌曲ID',
#   `song_name` varchar(255) NOT NULL DEFAULT '' COMMENT '歌曲名称',
#   `artist_name` varchar(255) NOT NULL COMMENT '歌手',
#   `user_id` varchar(15) NOT NULL DEFAULT '' COMMENT '用户ID',
#   `nickname` varchar(255) NOT NULL DEFAULT '' COMMENT '昵称',
#   `avatar_url` varchar(200) NOT NULL DEFAULT '' COMMENT '头像地址',
#   `comment_id` varchar(255) NOT NULL DEFAULT '' COMMENT '评论ID',
#   `content` text NOT NULL COMMENT '评论内容',
#   `time` varchar(15) NOT NULL DEFAULT '' COMMENT '评论时间',
#   `liked_count` varchar(10) NOT NULL DEFAULT '' COMMENT '评论点赞数',
#   `is_hot` tinyint(3) NOT NULL DEFAULT 0 COMMENT '是否热评',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

# CREATE TABLE `netease_cloud_music_comment_reply` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `song_id` varchar(10) NOT NULL DEFAULT '' COMMENT '歌曲ID',
#   `song_name` varchar(255) NOT NULL DEFAULT '' COMMENT '歌曲名称',
#   `comment_id` varchar(255) NOT NULL DEFAULT '' COMMENT '评论ID',
#   `re_user_id` varchar(15) NOT NULL DEFAULT '' COMMENT '用户ID',
#   `re_nickname` varchar(255) NOT NULL DEFAULT '' COMMENT '昵称',
#   `re_avatar_url` varchar(255) NOT NULL DEFAULT '' COMMENT '头像地址',
#   `re_comment_id` varchar(255) NOT NULL DEFAULT '' COMMENT '回复ID',
#   `re_content` text NOT NULL COMMENT '回复内容',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


# ------------------------------DEMO---------------------------------
# def main_fun(crawl_url):
#     req_header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                       ' Chrome/76.0.3809.132 Safari/537.36'
#     }
#     result = requests.get(crawl_url, headers=req_header)
#     print(result.content)
#     return
#     if result.status_code == requests.codes.ok:
#
#         host = 'https://music.163.com'
#
#         doc = etree.HTML(result.content)
#         li_list = doc.xpath('//div[@id="song-list-pre-cache"]/ul[@class="f-hide"]/li')
#         print(li_list)
#         for li in li_list:
#             song_name = li.xpath('./a/text()')[0]
#             song_url = li.xpath('./a/@href')[0]
#             print(song_url)
#
#             # https: // blog.csdn.net / csdnsevenn / article / details / 80746589
#
#
# main_fun('https://music.163.com/playlist?id=2331414535')
