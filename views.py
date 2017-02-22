import json
import sqlite3
from flask import Blueprint
from flask import abort, sessions,g
from flask import jsonify
from flask import request
from flask import url_for
from ext import dbtasks
from ext import dbtasks_del
from ext import dbtasks_last
from ext import dbtasks_upd
from ext import dbtasks_count
import pika
from flask import render_template, flash, session, redirect, abort
from flask_paginate import Pagination, get_page_args
from werkzeug.security import generate_password_hash,check_password_hash
from ext import cache


main_blueprint = Blueprint('main', __name__, url_prefix='/todo/api/v1.0/')
root_blueprint = Blueprint('root', __name__, url_prefix='/')
#login_blueprint = Blueprint('login',__name__, url_prefix='/lo')

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_num=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

def rabbit(msg):
    rmq_con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = rmq_con.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_publish(exchange='', routing_key='tasks', body=msg)
    rmq_con.close()


@main_blueprint.route('tasks', methods=['GET'])
####@auth.login_required
def get_tasks():
    # def get_tasks(task_id):Sqlite (Xerial) - app.db
    #return jsonify({'tasks': map(make_public_task, dbtasks())})
    return jsonify({'tasks': dbtasks()})

@main_blueprint.route('tasks_list', methods=['GET','POST'])
#@cache.memoize(timeout=60)
def index(v=1):
    import json
    if request.method == 'POST':
        if request.form['action'] == 'Delete':
            print(request.form.getlist('check'))
            for id in request.form.getlist('check'):
                dbtasks_del(int(id))
        if request.form['action'] == 'Update':
            print(request.form.getlist('check'))
            for id in request.form.getlist('check'):
                dbtasks_upd(int(id),status='Done')

    from flask import render_template
    titles = []
#    if session.get('username'):
    print("Session", session.get('user'))
#Pagination
    search = False
    q = request.args.get('q')
    if q:
        search =True
    g.conn = sqlite3.connect('/todo-api/app.db')
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()
    per_page = 5
    page = request.values.get('page',type=int, default=1 )
    sql = 'select * from todo_list limit :per_page offset :offset '
    print("sql",sql)
    offset = 0 if (page == 1) else ((page - 1) * per_page)
    g.cur.execute(sql,{'per_page':per_page, 'offset':offset})
    tTasks =g.cur.fetchall()
    total = dbtasks_count()

    print("page",page)
    print("rec_num",total)
    print("q", q)
    print("dbtasks",dbtasks())
    print("tTasks",tTasks)
    pagination = Pagination(page = page,total = total[0], per_page=per_page, search=search, record_name='tasks')
    print("paginat",pagination.__dict__)
    print("paginat",dir(pagination))
    return render_template('home.html',tasks = tTasks, page=page,pagination = pagination, login=session.get('user'))

#Pagination end

#return render_template('index.html', tasks=dbtasks(), login = session.get('user') )





@root_blueprint.route('',methods=['GET'])
def home():
     if not session.get('logged_in'):
         return render_template('login.html')
     else:
         #return "Hello Dima!"
          return redirect('http://192.168.1.105:80/todo/api/v1.0/tasks_list')

@root_blueprint.route('login',methods=['POST'])
def login():
    from models import User
    from app import db
    name_ck=request.form.get('username',None)
    pwd_ck = request.form.get('password', None)

    if name_ck is None:
        session['logged_in'] = False
        flash(u'wrong username/password!','error')
        return home()

    if pwd_ck is None:
        session['logged_in'] = False
        flash(u'wrong username/password!', 'error')
        return home()

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    print POST_USERNAME

    s = db.session()
    try:
        dbr = User.query.filter(User.username == POST_USERNAME).first()
        pswd = dbr.password
    except:
        session['logged_in'] = False
        flash(u'wrong username/password!', 'error')
        return home()

    if pswd:
        result = check_password_hash(dbr.password, POST_PASSWORD)
    else:
        result = False
        session['logged_in'] = False
        return home()
#    query = s.query(User).filter(User.username.in_([POST_USERNAME]),User.password.in_([POST_PASSWORD]))
    #print query
    #check_password_hash(pwhash=)
#    result = query.first()

    #print result
    if result == True:
    #if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        session['user'] = POST_USERNAME
    else:
        flash(u'wrong username/password!','error')
    return home()

@root_blueprint.route('logout')
def logout():
    session['logged_in'] = False
    return home()

@main_blueprint.route('tasks', methods=['POST'])
def create_task():
    from models import Todo_list
    from app import db
    last = dbtasks_last()
    num = last + 1
    title = request.json['title']
    done = "False"
    uri = request.url + "/" + str(num)
    desc = request.json['desc']
    task = Todo_list(description=desc, title=title, uri=uri, status=done)
    db.session.add(task)
    db.session.commit()
#Rabbit
#    message = json.dumps({"status": "ok", "id": task.id, "title": title, "uri": uri, "description": desc})
#    message = json.dumps({"status": "ok", "id": num, "title": title, "uri": uri, "description": desc})
#    rabbit(message)

#    return jsonify({"status": "ok", "id": task.id, "title": title, "uri": uri, "description": desc}), 201


    return jsonify({"status": "ok", "id": num, "title": title, "uri": uri, "description": desc}), 201


@main_blueprint.route('tasks/<int:task_num>', methods=['PUT'])
def update_task(task_num):
    if not request.json:
        abort(400)

    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    data = request.get_data()
    key = json.loads(data)
    for k, v in key.items():

        if k == 'done':
            status = v
        else:
            status = None
        if k == 'description':
            description = v
        else:
            description = None
        if k == 'title':
            title = v
        else:
            title = None
        if k == 'uri':
            uri = v
        else:
            uri = None

    dbtasks_upd(task_num,
                status=status,
                description=description,
                title=title,
                uri=uri)
    return jsonify({'task': 'Ok'})


@main_blueprint.route('tasks/<int:task_num>', methods=['DELETE'])
def delete_task(task_num):
    dbtasks_del(task_num)
    return jsonify({'remove task id': task_num, 'result': True})


@main_blueprint.route('tasks/<int:task_num>', methods=['GET'])
def get_task(task_num):
    task = filter(lambda t: t['num'] == task_num, dbtasks())
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})