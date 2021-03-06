import importlib

from django.db.models.loading import get_apps
from sqjobs.utils import get_jobs_from_module

import logging
logger = logging.getLogger('sqjobs.contrib.django.utils')


def register_all_jobs(worker):
    """
    Register all the jobs in a worker
    """
    jobs = get_all_jobs()

    for job in jobs:
        worker.register_job(job)

    return jobs


def get_all_jobs():
    """
    Get all the jobs of the django INSTALLED_APPS
    """
    jobs = []

    for app in get_apps():
        try:
            module = importlib.import_module(app.__name__[:-6] + 'jobs')
            jobs.extend(get_jobs_from_module(module))
        except ImportError:
            pass

    return jobs
