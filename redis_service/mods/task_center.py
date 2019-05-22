# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:32:52 2018

@author: luolei

任务处理中心
"""
import redis
import yaml
import sys

sys.path.append('../')


def load_redis_config():
	"""
	载入redis连接配置
	:return:
		redis_config, dict, redis连接配置字典
		task_name, str, 任务名
		jobs_limit, int, 任务队列容量
	"""
	config_path = '../config/config.yml'
	with open(config_path, 'r', encoding = 'utf-8') as f:
		config = yaml.load(f)
	redis_config = config[config['redis_loc']]
	task_name, jobs_limit = config['redis_task_params']['task_name'], config['redis_task_params']['jobs_limit']
	return redis_config, task_name, jobs_limit


class TaskCenter(object):
	"""
	redis任务处理
	"""
	def __init__(self, redis_config, task_name, jobs_limit):
		"""
		初始化
		:param redis_config: dict, redis连接配置字典
		:param task_name: str, 当前redis任务名
		:param jobs_limit: int, redis中任务job数量上限
		"""
		if 'password' in redis_config.keys():
			self._rds = redis.Redis(host = redis_config['host'], password = redis_config['password'], port = redis_config['port'])
		else:
			self._rds = redis.Redis(host = redis_config['host'], port = redis_config['port'], decode_responses = redis_config['decode_responses'], db = redis_config['db'])
		self._task_name = task_name
		self._jobs_limit = jobs_limit

	def jobs_count(self):
		"""
		已有任务计数
		:return: int
		"""
		return self._rds.llen(self._task_name)

	def is_queue_full(self):
		"""
		判断任务队列是否已满
		:return: bool
		"""
		assert self._jobs_limit is not None
		return self.jobs_count() >= self._jobs_limit

	def push_a_job(self, job_value):
		"""
		向redis任务队列中推送一条待处理任务记录
		:param job_value: str, 待处理记录
		"""
		if self.is_queue_full():
			raise ValueError('队列满了', )
		else:
			self._rds.rpush(self._task_name, str(job_value))

	def pull_a_job(self):
		"""
		拉取job
		:param pop: bool, 是否同时在任务队列中删除该记录
		:return:
			job: str, 拉取的任务记录
		"""
		job = self._rds.lpop(self._task_name)  # 从序列中左取并删除该任务，原子性操作, 不会产生重复拉取
		if job is not None:
			return job
		elif job is None:
			return None

	def flushall(self):
		self._rds.flushall()

	def shutdown(self):
		self._rds.shutdown()


redis_config, task_name, jobs_limit = load_redis_config()
task_center = TaskCenter(redis_config, task_name, jobs_limit)

# task_center.shutdown()




