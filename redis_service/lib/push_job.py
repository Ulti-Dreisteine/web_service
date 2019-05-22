# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:32:52 2018

@author: luolei

推任务
"""
import numpy as np
import sys

sys.path.append('../')

from mods.task_center import task_center


if __name__ == '__main__':
	# 向任务中心推送任务
	job_values = np.arange(100)
	for i in range(len(job_values)):
		task_center.push_a_job(job_values[i])

	print(task_center.jobs_count())

