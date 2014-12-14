import logging
logger = logging.getLogger('sqjobs')


class Worker(object):

    def __init__(self, broker, queue_name):
        self.broker = broker
        self.queue_name = queue_name
        self.registered_jobs = {}

    def __repr__(self):
        return 'Worker({connector})'.format(
            connector=type(self.broker.connector).__name__
        )

    def register_job(self, job_class):
        self.registered_jobs[job_class.name()] = job_class

    def execute(self):
        for payload in self.broker.jobs(self.queue_name):
            job, args, kwargs = self._build_job(payload)
            job.run(*args, **kwargs)

    def _build_job(self, payload):
        job_class = self.registered_jobs[payload['name']]
        job = job_class()

        job.retries = payload['_metadata']['retries']
        job.created_on = payload['_metadata']['created_on']
        job.first_execution_on = payload['_metadata']['first_execution_on']

        return job, payload['args'], payload['kwargs']
