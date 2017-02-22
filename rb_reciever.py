import pika
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

rmq_con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = rmq_con.channel()
channel.queue_declare(queue='tasks')

def callback(ch,method, properties,body):
    from models import Todo_list
    print("[x] Reciever %r" % body)
    data = json.loads(body)
    id = data['id']
    description = data['description']
    uri = data['uri']
    title = data['title']
    status = 'False'
    task = Todo_list(description=description, title=title, uri=uri, status=status)
    db.session.add(task)
    db.session.commit()

#    print("id: {}".format(data['id']))
#    print("description: {}".format(data['description']))
#    print("uri: {}".format(data['uri']))
#    print("title: {}".format(data['title']))
#    print("status: {}".format(data['status']))
channel.basic_consume(callback, queue='tasks', no_ack=True)
print (' [*] Waiting for messages. To exit press CTLC+C')

channel.start_consuming()
