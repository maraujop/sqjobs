import importlib
import inspect

from .job import Job
from .brokers.standard import Standard
from .brokers.eager import Eager
from .connectors.sqs import SQS
from .worker import Worker

import logging
logger = logging.getLogger('sqjobs')


def create_eager_broker():
    return Eager()


def create_sqs_broker(access_key, secret_key, region='us-west-1', use_ssl=True):
    sqs = SQS(
        access_key=access_key,
        secret_key=secret_key,
        region=region,
        use_ssl=use_ssl,
    )

    return Standard(sqs)


def create_sqs_worker(queue_name, access_key, secret_key, region='us-west-1', use_ssl=True):
    broker = create_sqs_broker(access_key, secret_key, region, use_ssl)
    return Worker(broker, queue_name)


def get_jobs_from_module(module_name):
    jobs = []

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return jobs

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Job) and not obj.abstract:
            logger.info('Found new job: %s', name)
            jobs.append(obj)

    return jobs
