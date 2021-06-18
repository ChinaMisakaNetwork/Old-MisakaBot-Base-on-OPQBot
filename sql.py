# 导入pymysql模块
import pymysql
#定义数据库连接
#请自行更改以下服务器相关信息
host = 'host ip'
user = 'database user name'
password = 'database password'
database = 'database name'
charset = 'utf8'
# 连接database


def write(sql):
    conn = pymysql.connect(
        host=host, user=user, password=password, database=database, charset=charset)
# 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
# 执行SQL语句
    cursor.execute(sql)
    conn.commit()
# 关闭光标对象
    cursor.close()
# 关闭数据库连接
    conn.close()


def read(SQL):
    conn = pymysql.connect(
        host=host, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()
    cursor.execute(SQL)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    return(ret)
