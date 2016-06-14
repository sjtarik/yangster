from Queue import Queue
from threading import Thread
import json
import urllib2

dev_count = 4
dev_names = ['se1.dc5', 'se1.dc6', 'se1.sv5', 'se1.sv4']
unit_wait = 10


def do_stuff(q):
    while True:
        th = q.get()
        req = urllib2.Request(th['url'])
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, None)
        data = response.read()
        print data
        q.task_done()


q = Queue(maxsize=0)


for x in range(100):
    dev_idx = x % dev_count
    th_arg = {}
    th_arg = {'url': 'http://127.0.0.1:6532/api/v1/prov/' + dev_names[dev_idx], 'wait_time': dev_idx * unit_wait}
    q.put(th_arg)


num_threads = 45

for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,))
    worker.setDaemon(True)
    worker.start()


q.join()