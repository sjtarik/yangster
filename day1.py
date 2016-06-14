from flask import Flask, request, app
from time import sleep
from random import random, seed
from threading import Lock
app = Flask(__name__)
counter = 0

dev_list = {'se1.dc5': None, 'se1.dc6': None, 'se1.sv5': None, 'se1.sv4': None}
dev_counters = {'se1.dc5': 0, 'se1.dc6': 0, 'se1.sv5': 0, 'se1.sv4': 0}


def hello_world():
    print "hello!"


@app.route('/api/v1/prov/<dev_name>', methods=['GET', 'POST'])
def add_message(dev_name):
    global counter
    global dev_list
    global dev_counters
    content = request.get_json(silent=True)
    print content
    if dev_name in dev_list:
        dev_lock = dev_list.get(dev_name)
        dev_lock.acquire()
        dev_counters[dev_name] += 1
        dev_lock.release()
    else:
        return 'device: ' + dev_name + ' does not exist '
    counter += 1
    sleep(random()*10)
    print_stats()
    return dev_name + " " + str(counter)


@app.route('/')
def index_page():
    global counter
    hello_world()
    sleep(random()*10)
    counter += 1
    return str(counter) + " OK "


def print_stats():
    for dev_name in dev_counters:
        print dev_name + ' ' + str(dev_counters[dev_name])

if __name__ == "__main__":
    for dev in dev_list.keys():
        dev_list[dev] = Lock()
    seed(123)
    app.run(host="0.0.0.0", port=6532, threaded=True)