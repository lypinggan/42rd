#coding:utf-8
"""
基于redis的消息队列
"""
import redis
import cPickle

class Queue(object):  
    """An abstract FIFO queue"""  
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=1) 
        self.id_name = "queue"
        #self.id_name = "queue:%s" %(self.r.incr("queue_space"))  

    def push(self, element):
        """插入一个元素到队列的尾部"""
        value = cPickle.dumps(element)      
        push_element = self.r.lpush(self.id_name,value)  
    def pop(self):
        """从队列的头部取出一条记录"""
        popped_element = self.r.rpop(self.id_name)
        try:
            return cPickle.loads(popped_element)
        except:
            return None
"""
Demo

from queue.py import Queue
q = Queue()
添加队列
q.push('123')
提取队列
print q.pop()

"""
