# MySQL操作类
import pymysql


class OperateMysql():

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
        if table_name == 'douban_movie_top250':


            ins_data = [data['rank'], data['movie_name'], data['staff'], data['age_type'], data['score'],
                        data['people_num'], data['quote'], data['cover_pic_url'], data['summary_url']]

            sql = """insert into douban_movie_top250 (`rank`, `movie_name`, `staff`, `age_type`, `score`, `people_num`, `quote`, `cover_pic_url`, `summary_url`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        elif table_name == 'wipzhu':
            ins_data = []
            sql = ''
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
