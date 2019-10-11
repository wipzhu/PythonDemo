# MySQL操作类
import pymysql


class OperateMysql():

    def __get_conn(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test_demo',
                                        charset='utf8mb4')
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
        if table_name == 'douban_movie_top250':

            ins_data = [data['rank'], data['movie_name'], data['staff'], data['age_type'], data['score'],
                        data['people_num'], data['quote'], data['cover_pic_url'], data['summary_url']]
            sql = """insert into douban_movie_top250 (`rank`, `movie_name`, `staff`, `age_type`, `score`, `people_num`, `quote`, `cover_pic_url`, `summary_url`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        elif table_name == 'netease_cloud_music_comment':

            ins_data = [data['song_id'], data['song_name'], data['artist_name'], data['user_id'], data['nickname'], data['avatar_url'],
                        data['comment_id'], data['content'], data['time'], data['liked_count'], data['is_hot']]
            sql = """insert into netease_cloud_music_comment (`song_id`, `song_name`, `artist_name`, `user_id`, `nickname`, `avatar_url`, `comment_id`, `content`, `time`, `liked_count`, `is_hot`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        elif table_name == 'netease_cloud_music_comment_reply':

            ins_data = [data['song_id'], data['song_name'], data['comment_id'], data['re_user_id'], data['re_nickname'], data['re_avatar_url'], data['re_comment_id'], data['re_content']]
            sql = """insert into netease_cloud_music_comment_reply (`song_id`, `song_name`, `comment_id`, `re_user_id`, `re_nickname`, `re_avatar_url`, `re_comment_id`, `re_content`) values (%s,%s,%s,%s,%s,%s,%s,%s);"""
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
