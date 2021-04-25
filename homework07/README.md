# Homework07: Asynchronous Programming

This directory contains all of the files required for homework 7. In this homework, a Flask API system and a scalable worker system are deployed to Kubernetes. See prompt [here](https://coe-332-sp21.readthedocs.io/en/main/homework/homework07.html).

# Dependencies

Kubernetes is required. Docker is needed if the user wishes to edit the application.

# Installation

The files can be cloned from this repo:

```bash
git clone https://github.com/bradenpecora/bsp825-coe332.git
```

Navigate to the `homework07/` directory to view the relevant files for this homework.

A redis database in k8s is required. Necessary files are included in `deploy/db`. These files are copied here from [Homework06](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework06) for completeness. Please see [Homework06](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework06) for information on deploying this system. Adjust the `REDIS_IP` environment variable in `deploy/api/bradenp-hw7-flask-deployment.yml` and `deploy/worker/bradenp-hw7-worker-deployment.yml` to match the IP of your redis service. It is worth noting that the `HotQueue` is stored on `db=2` and the `jobs` data is stored on `db=3`.

A single image containing all required python scripts is published to [Dockerhub](https://hub.docker.com/repository/docker/bradenpecora/hw7), and these sources files can viewed and edited in `source/`. The image can be built locally using the `Dockerfile`.

The following commands applies the necessary Kubernetes resources.

```bash
[bradenp@isp02 homework07]$ kubectl apply -f deploy/api
deployment.apps/bradenp-hw7-flask-deployment created
service/bradenp-hw7-flask-service created
[bradenp@isp02 homework07]$ kubectl apply -f deploy/worker
deployment.apps/bradenp-hw7-worker-deployment created
```

Verify that the resources are running:

```bin
[bradenp@isp02 homework07]$ kubectl get pods --selector env=hw7
NAME                                             READY   STATUS    RESTARTS   AGE
bradenp-hw7-flask-deployment-8bf4fd48-4fp22      1/1     Running   0          52s
bradenp-hw7-worker-deployment-568456f7b8-qhkdk   1/1     Running   0          44s
[bradenp@isp02 homework07]$ kubectl get services --selector env=hw7
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
bradenp-hw7-flask-service   ClusterIP   10.107.239.99   <none>        5000/TCP   63s
```
Take note of the `CLUSTER-IP` of the flask service as it will be required later.

# Usage

On isp02, we must `exec` interactively into a python debug pod to interact the app on Kubernetes. Again, see [Homework06](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework06) for more information. Within this debug pod, install the python package `redis` using pip.

On the command line, we can make a POST request with `curl` to the Flask API. Make sure to replace `<Flask-Service-IP>` with the `CLUSTER-IP` found earlier.

```bash
curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}' <Flask-Service-IP>:5000/jobs
```

This should return an output similar to the following:

```bash
{"status": "submitted", "start": "go!", "end": "stop!", "id": "7ff41c0c-b49c-4473-80e4-d4a5f8acd187"}
```

To see if a worker has processed the job, open up an interactive python interpreter (e.g. `python` or `ipython`) in the debug pod. Check the following:

```python
In [1]: import redis

In [2]: rd = redis.StrictRedis(host="<Redis-service-IP", port=6379, db=3)
# Replace <Redis-service-IP> with the IP of your redis service.

In [3]: rd.keys()
Out[3]: [b'job.7ff41c0c-b49c-4473-80e4-d4a5f8acd187']
# The job ID will not be the same, but copy it accordingly for the next input.

In [4]: rd.hgetall('job.7ff41c0c-b49c-4473-80e4-d4a5f8acd187')
Out[4]: 
{b'status': b'complete',
 b'start': b'go!',
 b'end': b'stop!',
 b'id': b'7ff41c0c-b49c-4473-80e4-d4a5f8acd187',
 b'worker': b'10.244.15.176'}
 # The worker has updated the job's status to complete and appended it's IP to the job's data.
```

To scale the worker deployment to a different number of pods, edit line 10 of `deploy/worker/bradenp-hw7-worker-deployment.yml` to the desired number of pods. From the command line of your machine (not the debug pod), re-apply the deployment.

```bash
[bradenp@isp02 homework07]$ kubectl apply -f deploy/worker
deployment.apps/bradenp-hw7-worker-deployment configured
```

See if any additional pods are running and find their IPs. For instance, I scaled up to 2 replicas:

```bash
[bradenp@isp02 homework07]$ kubectl get pods --selector app=bradenp-hw7-worker -o wide
NAME                                             READY   STATUS    RESTARTS   AGE   IP              NODE                         NOMINATED NODE   READINESS GATES
bradenp-hw7-worker-deployment-568456f7b8-dt4q4   1/1     Running   0          15m   10.244.15.176   c03                          <none>           <none>
bradenp-hw7-worker-deployment-568456f7b8-fmdf2   1/1     Running   0          84s   10.244.10.173   c009.rodeo.tacc.utexas.edu   <none>           <none>
```

Return to the debug pod. Create 10 more jobs by making POST requests using curl. Simply repeat the earlier command on the command line.

```
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "a015d4ea-ea2f-4ebf-9e9a-6283cd4b1b14"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "5acddbfe-7ed7-4d1e-b909-b12437870908"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "23c64332-b4a2-40ec-b882-bb122dda6b49"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "5d333127-b825-43c4-af67-5f048dc4d72a"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "945b64b4-dcde-499b-a251-9bcecec1d7bb"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "2847f92d-887d-485c-bbdd-7dfbf641504b"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "7a69c18a-136c-47c5-8417-b1bd92368605"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "0a79bfbb-23e0-469f-8948-1ba864030278"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "03667a99-bfee-485a-8591-110f29f4bf4a"}
root@py-debug-deployment-5cc8cdd65f-6kjfd:/# curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
{"status": "submitted", "start": "go!", "end": "stop!", "id": "3ac4ec76-f5b1-4c22-9382-ad6f727c818c"}
```
Navigate back to an interactive python interpreter within the debug pod.

```python
In [1]: import redis

In [2]: rd = redis.StrictRedis(host="10.104.165.3", port=6379, db=3)

In [3]: for key in rd.keys():
   ...:     print(rd.hgetall(key))
   ...: 
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'23c64332-b4a2-40ec-b882-bb122dda6b49', b'worker': b'10.244.15.176'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'945b64b4-dcde-499b-a251-9bcecec1d7bb', b'worker': b'10.244.15.176'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'2847f92d-887d-485c-bbdd-7dfbf641504b', b'worker': b'10.244.10.173'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'a015d4ea-ea2f-4ebf-9e9a-6283cd4b1b14', b'worker': b'10.244.15.176'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'03667a99-bfee-485a-8591-110f29f4bf4a', b'worker': b'10.244.15.176'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'7a69c18a-136c-47c5-8417-b1bd92368605', b'worker': b'10.244.15.176'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'3ac4ec76-f5b1-4c22-9382-ad6f727c818c', b'worker': b'10.244.10.173'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'0a79bfbb-23e0-469f-8948-1ba864030278', b'worker': b'10.244.10.173'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'5acddbfe-7ed7-4d1e-b909-b12437870908', b'worker': b'10.244.10.173'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'5d333127-b825-43c4-af67-5f048dc4d72a', b'worker': b'10.244.10.173'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'7ff41c0c-b49c-4473-80e4-d4a5f8acd187', b'worker': b'10.244.15.176'}
```

This output tells us that both workers did some of the jobs. The `worker` key in each job dictionary either contains `10.244.15.176` or `10.244.10.173`, which indicates that the pod with that IP address preformed that job. Of the 10 jobs we just made (the bottom job is from earlier), 5 jobs were handled by each worker. It seems the jobs were distributed evenly.