'''
封装一个mysql工具类(需要自己写SQL语句)
功能：mysql数据库操作
步骤：
    1.连接数据库
    2.通过连接对象，获取游标对象
    3.增删改查操作
方法：
    1.查
    2.增删改 commit,rollback
'''
import pymysql

# # 把连接参数定义成字典
# config = {
#     "host": "127.0.0.1",
#     "port": 3307,
#     "database": "lebo",
#     "charset": "utf8",
#     "user": "root",
#     "passwd": "root"
# }


class Mysqldb():
    # 初始化方法
    def __init__(self,config):
        # 初始化方法中调用连接数据库的方法
        self.conn = self.get_conn(config)
        # 调用获取游标的方法
        self.cursor = self.get_cursor()

    # 连接数据库的方法
    def get_conn(self,config):
        # **config代表不定长参数
        conn = pymysql.connect(**config)
        print('连接mysql成功')
        return conn

    # 获取游标
    def get_cursor(self):
        cursor = self.conn.cursor()
        return cursor

    # 创建数据表
    def create_table(self,sql):
        self.cursor.execute(sql)
        # print('创建数据表成功')

    # 查询sql语句返回的所有数据
    def select_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 查询sql语句返回的一条数据
    def select_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 查询sql语句返回的几条数据
    def select_many(self, sql, num):
        self.cursor.execute(sql)
        return self.cursor.fetchmany(num)

    # 增删改除了SQL语句不一样其他都是一样的，都需要提交
    def commit_data(self, sql):
        try:
            # 执行语句
            self.cursor.execute(sql)
            # 提交
            self.conn.commit()
            # print("提交成功")
        except Exception as e:
            print("提交出错\n:", e)
            # 如果出错要回滚
            self.conn.rollback()

    # 当对象被销毁时，游标要关闭,连接也要关闭
    # 创建时是先创建连接后创建游标，关闭时是先关闭游标后关闭连接
    def __del__(self):
        self.cursor.close()
        self.conn.close()
if __name__ == '__main__':
    # 把连接参数定义成字典
    # 连接云数据库
    config = {
        "host": "bj-cynosdbmysql-grp-bzwfkr20.sql.tencentcdb.com",
        "port": 23079,
        "database": "student",
        "charset": "utf8",
        "user": "test",
        "passwd": "Aa123456"
    }
    # 连接本地数据库
    # config = {
    #     "host": "127.0.0.1",
    #     "port": 3307,
    #     "database": "lebo",
    #     "charset": "utf8",
    #     "user": "root",
    #     "passwd": "root"
    # }


    mysql = Mysqldb(config)
    # mysql.cursor.execute("show tables")
    # table_list = [tuple[0] for tuple in mysql.cursor.fetchall()]
    # print(table_list)
    # sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '管院全体学生数据表'"
    # for name in mysql.select_all(sql):
    #     print(name)
    # sql = "SELECT * FROM 管院全体学生数据表"
    # sql = 'SELECT * FROM products'
    # sql = 'alter table 管院全体学生数据表 add id int(11) primary key AUTO_INCREMENT'  #设置自增主键
    # sql = 'alter table 管院全体学生数据表 modify id int(10) unsigned auto_increment first'
    # a = mysql.commit_data(sql)

    # 创建数据表
    tablename = '爬中公教育'
    sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
    print(sql)
    mysql.create_table(sql)

    # print(type(a))
    # print(a)
    # print(a)

