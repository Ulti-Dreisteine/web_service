# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:32:52 2018

@author: luolei

多机拉取执行任务
"""
import threading
import time
import sys

sys.path.append('../')

from mods.task_center import task_center


def worker(worker_num):
	"""
	任务处理器
	:return:
	"""
	while True:
		job = task_center.pull_a_job()
		time.sleep(2)
		print('\nworker {}, processing job {}'.format(worker_num, job))


if __name__ == '__main__':
	workers_num = 6
	threads = []
	for i in range(workers_num):
		t = threading.Thread(target = worker, args = (i,))
		threads.append(t)

	for i in range(workers_num):
		threads[i].start()

	for i in range(workers_num):
		threads[i].join()

