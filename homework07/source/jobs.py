# jobs.py
import uuid
from hotqueue import HotQueue
from redis import StrictRedis
import os
import sys

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

q = HotQueue("queue", host=redis_ip, port=6379, db=2)
rd = StrictRedis(host=redis_ip, port=6379, db=3)

# Allows print statements to be viewed in logs:
original_stdout = sys.stdout
sys.stdout = sys.stderr

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, start, end):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'start': start,
                'end': end
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(start, end, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, start, end)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def update_job_status(jid, new_status):
    """Update the status of job with job id `jid` to status `new_status`."""
    rd.hset(_generate_job_key(jid), 'status', new_status)

def add_worker_ip(jid, worker_ip):
    """Add a new key called 'worker' with value of the worker's IP address to the job with ID 'jid'"""
    print("adding worker ip")
    rd.hset(_generate_job_key(jid), 'worker', worker_ip)