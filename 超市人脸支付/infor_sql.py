import pymysql
import socket
from configparser import ConfigParser



def connectdb():
    dbhost = "39.106.163.99"
    dbuser = "root"
    dbpass = "RWIy1sfYs61L"
    dbname = "BS_TDB"
    print('连接到mysql服务器...')
    db = pymysql.connect(host=dbhost,user=dbuser,passwd=dbpass,database=dbname,charset="utf8")
    print('连接上了!')
    return db

def insertdb(db,infor):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #infor = ['z在','11',500]
    # SQL 插入语句

    sql2 = """INSERT INTO FaceInfor
         VALUES (default,%s, %s, %s)"""
    try:
        if True:
            cursor.execute(sql2,[infor[0],infor[1],infor[2]])
            print('摄像头注册')
        # 提交到数据库执行
            db.commit()
    except:
        # Rollback in case there is any error
        print ( '插入数据失败!')
        db.rollback()
def querydb(db):  # 查询所有信息
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "SELECT * FROM FaceInfor"

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)
        for row in results:
            id = row[0]
            name = row[1]
            gender= row[2]
            money = row[3]
            # 打印结果
            print ( "id: %s,姓名: %s,性别: %s, 余额: %s" % \
                (id,name, gender, money))
        return results
    except:
        print ( "Error: unable to fecth data")
        return None
def updatedb(db,infor): # infor[host_id,time,name]
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 更新语句

    name = infor[0]
    gender = infor[1]
    money = infor[2]
    print(name)
    sql1 = "UPDATE FaceInfor SET gender = %s WHERE name = %s"
    sql2 = "UPDATE FaceInfor SET money = %s WHERE name = %s"
    #sql2 = "UPDATE Security SET Host_id = %s WHERE Time = %s"
    try:
        # 执行SQL语句
        cursor.execute(sql1,[gender,name]) # 更新时间
        cursor.execute(sql2,[money,name]) # 更新姓名

        # 提交到数据库执行
        db.commit()
    except:
        print ( '更新数据失败!')
        # 发生错误时回滚
        db.rollback()
def createtable(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS FaceInfor")
    sql = """CREATE TABLE FaceInfor (
            id int primary key auto_increment ,
            Name CHAR(100)NOT NULL,
            Gender CHAR(40),
            Money int )character set = utf8"""

    # 创建表
    cursor.execute(sql)

def update_infor():
    db = connectdb()
    createtable(db)


    infor_conf = ConfigParser()
    infor_conf.read('information.conf', encoding='gbk')

    for name in infor_conf.sections():
        single_infor = []
        single_infor.append(name)
        single_infor.append(infor_conf.get(name,'性别'))
        single_infor.append(int(infor_conf.get(name, '余额')))
        insertdb(db,single_infor)

    querydb(db)

#update_infor()