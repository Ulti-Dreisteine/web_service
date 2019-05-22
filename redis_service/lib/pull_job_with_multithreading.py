# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:32:52 2018

@author: luolei

拉取任务
"""
import threading
import time
import sys

sys.path.append('../')

from mods.task_center import task_center

lock = threading.Lock()


def worker(worker_num):
	"""
	任务处理器
	:return:
	"""
	while True:
		lock.acquire()  # 获取锁
		try:
			job = task_center.pull_a_job()
			time.sleep(2)
			print('worker {}, processing job {}, {} jobs left'.format(worker_num, job, task_center.jobs_count()))
		finally:
			lock.release()


if __name__ == '__main__':
	workers_num = 2
	threads = []
	for i in range(workers_num):
		t = threading.Thread(target = worker, args = (i,))
		threads.append(t)

	for i in range(workers_num):
		threads[i].start()

	for i in range(workers_num):
		threads[i].join()


