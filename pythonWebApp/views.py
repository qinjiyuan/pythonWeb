from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
import pymysql  # MySQL数据库查询组件

import pymongo  # mongoDb数据库查询组件
from pymongo import MongoClient
from bson.objectid import ObjectId

from redis import *
from redis import StrictRedis

# connected to mysql server
mysql_db = pymysql.connect(host="localhost", user="root",
                           password="199107120319", db="pythonweb", port=3306)

redis_sr = StrictRedis(host='localhost', port=6379, db=0)

mongo_client = MongoClient('mongodb://admin:admin@localhost:27017')

mongo_db = mongo_client.mongo_demo


def index(request):
    results = mysql_connect(request)
    # mongodb_connect()
    # redis_connect()
    return render(request, "index.html", {"results": results})


#  python连接mysql连接数据库
def mysql_connect(request):
    cur = mysql_db.cursor()
    start = 10
    limit = 10
    if request.method == "POST":
        start = request.POST.get("start", None)
        limit = request.POST.get("limit", None)

    sql = "SELECT * FROM `sys_user` WHERE 1 limit %s, %s" % (start, limit)
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        fields = cur.description
    except Exception as e:
        raise e
    # print(type(results))
    #
    # print(results)
    # print(type(fields))
    # print(fields)
    result2json(results, fields)
    return results


def mongodb_connect():
    collection = mongo_db.user
    print("mongo0")
    print(collection)
    result = collection.find_one({'name': 'qinjiyuan'})
    print("mongo1")
    print(result)
    result = collection.find({'age': '16'})
    print("mongo3")
    print(result)
    # 7.更新文档
    # 7.1update()
    condition = {'name': 'qinjiyuan2'}
    student = collection.find_one(condition);
    student['age'] = 30
    result = collection.update(condition, student)
    print("mongo4")
    print(result)

    # 7.2update_one()
    condition = {'name': 'qinjiyuan5'}
    student = collection.find_one(condition);
    student['age'] = 30
    result = collection.update_one(condition, {'$set': student})
    print(result.matched_count, result.modified_count)

    # 7.3update_many()
    # 查询年龄大于20的数据，然后讲年龄增加1
    condition = {'age': {'$gt': 20}}
    result = collection.update_one(condition, {'$inc': {'age': 1}})
    print(result.matched_count, result.modified_count)

    # 8.删除文档
    # 8.1 remove()
    # 将符合条件的所有的数据全部删除
    result = collection.remove({'name': 'rose'})
    print(result)

    # 8.2 delete_one()
    result = collection.delete_one({'name': 'rose'})
    print(result)

    # 8.3 delete_many()
    result = collection.delete_many({'name': 'rose'})
    print(result)


def redis_connect():
    try:
        result = redis_sr.set('py1', 'gj')
        # result如果为true，则表示添加成功
        print("redis1")
        print(result)
    except Exception as e:
        print(e)
    # 2.删
    # result = sr.delete('py1')
    # print(result)

    # 3.改
    result = redis_sr.set('py1', 'he')
    print("redis2")
    print(result)

    # 4.查
    # 如果建不存在，则返回None
    result = redis_sr.get('py1')
    print("redis3")
    print(result)

    # 5.获取建
    result = redis_sr.keys()
    print("redis4")
    print(result)


def result2json(results, fields):
    result_json = []

    field_list = []
    for field in fields:
        field_list.append(field[0])

    for row in results:
        result = {}
        for fieldIndex in range(0, len(field_list)):
            result[field_list[fieldIndex]] = str(row[fieldIndex])
        json_data = json.dumps(result, ensure_ascii=False)
        result_json.append(json_data)
    print(result_json)


# fixme
# todo
def filed2filed(filed):
    filed.split('_')
