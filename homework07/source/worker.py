from jobs import q, update_job_status, add_worker_ip
import time
import os

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    worker_ip = os.environ.get('WORKER_IP')
    add_worker_ip(jid, worker_ip)
    time.sleep(15)
    update_job_status(jid, 'complete')

execute_job()