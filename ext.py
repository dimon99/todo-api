#!flask/bin/python
import sqlite3 as lite
from flask import Flask, jsonify
import sys
from collections import OrderedDict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cache import Cache
import memcache


db = SQLAlchemy()
migrate = Migrate()
cache = Cache()



#mc = memcache.Client(['127.0.0.1:11211'], debug=1);
def dbtasks_count():
    con = lite.connect('/todo-api/app.db')
    cur = con.cursor()
    count = cur.execute("SELECT Count(*) from 'todo_list' ")
    count = count.fetchone()
    con.close()
    return count


def dbtasks():
    mc = memcache.Client(['memcached:11211'], debug=1);
    con = lite.connect('/todo-api/app.db')
    cur = con.cursor()
    all_tasks = []

#mcdata = mc.get('tasks')

    try:
        cur.execute("select * from todo_list")
        results = cur.fetchall()

        all_tasks = mc.get('tasks')
        if not all_tasks:
            all_tasks = []
            for row in results:
                id = row[0]
                desc = row[1]
                title = row[2]
                uri = row[3]
                status = row[4]
                dictionary = {'num': id, 'desc': desc, 'title': title, 'uri': uri, 'status': status }
                #dict = OrderedDict([('num',id), ('desc', desc), ('title', title), ('uri',uri), ('status',status)])
                #print(dict)
                all_tasks.append(dictionary)
    #            mc.set('tasks',dictionary,60)
                #print "id=%s,desc=%s,title=%s,uri=%s,status=%s" % \
                # (id,desc,title,uri,status)
            mc.set('tasks', all_tasks, 360)
            print all_tasks
        else:
            print "Loaded from MEMCACHED"
            print all_tasks
    except Exception as e:
        print"Error: unable to fetch data: {}".format(str(e))

    con.close()
    return all_tasks
    #con.close()

#dbtasks()
task_num = 0
def dbtasks_del(task_num):
    mc = memcache.Client(['memcached:11211'], debug=1);
    con = lite.connect('/todo-api/app.db')
    cur = con.cursor()
    try:
       cur.execute("DELETE from 'todo_list' where id = '%s' " % (task_num,))
    except Exception as e:
        print "Error: unable to fetch data {}".format(str(e))
    con.commit()
    con.close()
    mc.delete('tasks')
#    return jsonify({'result': True})

def dbtasks_upd(task_num, status=None, description=None, title=None, uri=None):
    mc = memcache.Client(['memcached:11211'], debug=1);
    fields = []
    if status:
        fields.append('status = "{status}"'.format(status=status))
    if description:
        fields.append('description = "{descr}"'.format(descr=description))
    if title:
        fields.append('title = "{title}"'.format(title=title))
    if uri:
        fields.append('uri = "{uri}"'.format(uri=uri))

    result = ",".join(fields)

    con = lite.connect('/todo-api/app.db')
    cur = con.cursor()
    try:
       cur.execute("UPDATE 'todo_list' SET {result} where id = '{id}' ".format(
           result=result, id=task_num))
    except Exception as e:
        print "Error: unable to fetch data {}".format(str(e))
    mc.delete('tasks')
    con.commit()
    con.close()

def dbtasks_last():
    con = lite.connect('/todo-api/app.db')
    cur = con.cursor()
    last_id = cur.execute("SELECT MAX(id) from 'todo_list' ")
    last_id = last_id.fetchone()[0]
    con.close()
    return last_id