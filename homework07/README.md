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

A redis database in k8s is required. Necessary files are included in `/deploy/db`. These files are copied here from [Homework06](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework06) for completeness. Please see [Homework06](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework06) for information on deploying this system. Adjust the `REDIS_IP` environment variable in `/deploy/api/bradenp-hw7-flask-deployment.yml` and `/deploy/worker/bradenp-hw7-worker-deployment.yml` to match the IP of your redis service. It is worth noting that the `HotQueue` is stored on `db=2` and the `jobs` data is stored on `db=3`.

A single image containing all required python scripts is published to [Dockerhub](https://hub.docker.com/repository/docker/bradenpecora/hw7), and these sources files can viewed and edited in `/source`. The image can be built locally using the `Dockerfile`.

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
{"status": "submitted", "start": "go!", "end": "stop!", "id": "9b6f4822-95b9-440c-99ba-e2c5b87b42d4"}
```

To see if a worker has processed the job, open up an interactive python interpreter (e.g. `python` or `ipython`) in the debug pod. Check with the following:

```python
In [1]: import redis

In [2]: rd = redis.StrictRedis(host="<Redis-service-IP", port=6379, db=3)
# Replace <Redis-service-IP> with the IP of your redis service.

In [3]: rd.keys()
Out[3]: [b'job.9b6f4822-95b9-440c-99ba-e2c5b87b42d4']
# The job ID will not be the same, but copy it accordingly for the next input.

In [4]: rd.hgetall('job.9b6f4822-95b9-440c-99ba-e2c5b87b42d4')
Out[4]: 
{b'status': b'complete',
 b'start': b'go!',
 b'end': b'stop!',
 b'id': b'9b6f4822-95b9-440c-99ba-e2c5b87b42d4',
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
NAME                                             READY   STATUS    RESTARTS   AGE   IP              NODE   NOMINATED NODE   READINESS GATES
bradenp-hw7-worker-deployment-568456f7b8-jxnx6   1/1     Running   0          14m   10.244.12.172   c12    <none>           <none>
bradenp-hw7-worker-deployment-568456f7b8-qbr42   1/1     Running   0          84s   10.244.3.161    c01    <none>           <none>
```

Return to the debug pod. Create 10 more jobs by making POST requests using curl. Use a for loop to repeat the earlier command in bash on the debug pod.

```bash
root@bradenp-debug-py-deployment-59b4df4576-lnjpr:/# \
> for i in {1..10}
> do
> curl -X POST -H "content-type: application/json" -d '{"start": "go!", "end": "stop!"}'  10.107.239.99:5000/jobs
> done
{"status": "submitted", "start": "go!", "end": "stop!", "id": "43853f24-1542-46e0-8d0d-926af0408347"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "e88428fe-9e38-4705-a790-8900cc2bf8a4"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "e1dce25d-3ec9-48cc-9c7e-24a01b638ff2"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "7e5246c5-1537-480b-a82a-da43891bda84"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "0827867a-3993-4422-9122-7d8d136c2dea"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "40c4a8f5-c02e-4064-ac91-2f15806cf15f"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "db9bbd0f-482d-4c7b-82c9-8267a0c34262"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "dd2bbe8a-f040-49f8-9a8f-ae76535f0be8"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "27a99161-8755-4dd0-a064-18f1c96769ed"}
{"status": "submitted", "start": "go!", "end": "stop!", "id": "b832a217-5559-459a-81ce-67b758afb87a"}
```
Navigate back to an interactive python interpreter within the debug pod.

```python
In [1]: import redis

In [2]: rd = redis.StrictRedis(host="10.104.165.3", port=6379, db=3)

In [3]: for key in rd.keys():
   ...:     print(rd.hgetall(key))
   ...: 
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'40c4a8f5-c02e-4064-ac91-2f15806cf15f', b'worker': b'10.244.3.161'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'e88428fe-9e38-4705-a790-8900cc2bf8a4', b'worker': b'10.244.3.161'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'9b6f4822-95b9-440c-99ba-e2c5b87b42d4', b'worker': b'10.244.3.161'} # from earlier
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'db9bbd0f-482d-4c7b-82c9-8267a0c34262', b'worker': b'10.244.12.172'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'27a99161-8755-4dd0-a064-18f1c96769ed', b'worker': b'10.244.12.172'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'7e5246c5-1537-480b-a82a-da43891bda84', b'worker': b'10.244.3.161'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'0827867a-3993-4422-9122-7d8d136c2dea', b'worker': b'10.244.12.172'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'dd2bbe8a-f040-49f8-9a8f-ae76535f0be8', b'worker': b'10.244.3.161'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'b832a217-5559-459a-81ce-67b758afb87a', b'worker': b'10.244.3.161'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'43853f24-1542-46e0-8d0d-926af0408347', b'worker': b'10.244.12.172'}
{b'status': b'complete', b'start': b'go!', b'end': b'stop!', b'id': b'e1dce25d-3ec9-48cc-9c7e-24a01b638ff2', b'worker': b'10.244.12.172'}
```

This output tells us that both workers did some of the jobs. The `worker` key in each job dictionary either contains `10.244.3.161` or `10.244.12.172`, which indicates that the pod with that IP address preformed that job. Of the 10 jobs we just made (the job from earlier is noted), 5 jobs were handled by each worker. It seems the jobs were distributed evenly.