# Homework 6: Deploying Flask API to k8s

This homework builds off of homeworks 1,2,3, and the midterm. This directory contains all of the files required to interact with the animals flask app (from previous homeworks) in Kubernetes.

# Dependencies

Trivially, k8s is required. Docker is required if the user wishes to customize the flask app. All other dependencies are handled by k8s and docker.

# Installation

The files can be cloned from this repo:

```bash
git clone https://github.com/bradenpecora/bsp825-coe332.git
```

Navigate to the `homework06` directory. To start all required deployments, services, and PVCs:

```bash
[bradenp@isp02 homework06]$ kubectl apply -f .
````

Take note of the `.` at the end of the command. If the user is on isp02, everything should be running in my namespace (bradenp). Feel free to interact with these services as opposed to creating everything new. The IPs of the services are described later in the next section of this document.

Notes: 
- The directory `/flask-api` contains all of the necessary files to create a custom docker image for the flask app. 
Luckily, a docker image has already been uploaded to [Dockerhub](https://hub.docker.com/r/bradenpecora/flask-animals) and is used by the k8s flask deployment. 
- Since the flask deployment must communicate with the redis deployment using the redis service's IP, the redis service's clusterIP was set to `10.104.165.3` (this is what it defaulted to in my namespace). The cluster IP can be changed, but it involves changing the IP in line 10 of `bradenp-test-redis-service.yml`, changing the host IP in line 12 of `/flask-api/app.py`, rebuilding the image in `/flask-api` and pushing it to DockerHub, and changing the image in line 25 of `bradenp-test-flask-deployment.yml`; which is a rather time consuming process.
- The deployment `bradenp-debug-python-deployment` is optional. Any debug pod will work.

# Usage

All pods, deployments, and services should be up and running. To test, check to see if the following match:

```bash
[bradenp@isp02 homework06]$ kubectl get pods --selector username=bradenp
NAME                                             READY   STATUS    RESTARTS   AGE
bradenp-debug-py-deployment-59b4df4576-lnjpr     1/1     Running   0          43h
bradenp-test-flask-deployment-647ccd8b66-hjbt7   1/1     Running   0          3m21s
bradenp-test-flask-deployment-647ccd8b66-kk7cg   1/1     Running   0          3m21s
bradenp-test-redis-deployment-56bd9675f6-qv7zq   1/1     Running   0          42h
```

```bash
[bradenp@isp02 homework06]$ kubectl get deployments --selector username=bradenp
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
bradenp-debug-py-deployment     1/1     1            1           22m
bradenp-test-flask-deployment   2/2     2            2           22m
bradenp-test-redis-deployment   1/1     1            1           22m
```

```bash
[bradenp@isp02 homework06]$ kubectl get pvc --selector username=bradenp
NAME                     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
bradenp-test-redis-pvc   Bound    pvc-9bcf12ad-a11a-4ecf-8b38-65cc0ba5e2f3   1Gi        RWO            rbd            4d9h
```

```bash
[bradenp@isp02 homework06]$ kubectl get services --selector username=bradenp
NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
bradenp-test-flask-service   ClusterIP   10.98.225.212   <none>        5000/TCP   23m
bradenp-test-redis-service   ClusterIP   10.104.165.3    <none>        6379/TCP   23m
```
Make sure that the cluster IP of `bradenp-test-redis-service` is exactly `10.104.165.3`, unless you have changed it. Also take note of the cluster IP of `bradenp-test-flask-service`. This does not have to match.

If the user is on isp02, these services should be running with the cluster IPs given above.

Note: The selectors `app=bradenp-test-flask` and `app=bradenp-test-redis` were created to connect the services to the pods, but they can be used to get a specific flask or redis pod as well.

#
## Redis:

Now that we have verified that everything is running, `exec` into a python debug pod. I have provided one:
```bash
kubectl exec -it bradenp-debug-py-deployment-59b4df4576-lnjpr -- /bin/bash
```
The name of your debug pod will be most likely be different. 

To make sure the redis deployment and service are running properly, you can start an interactive python shell. First, you must install the `redis` python package using `pip install redis`. I also like ipython: `pip install ipython`. Start the interactive shell by typing `ipython`. Try connecting to the redis database, setting a key, getting the key, deleting the redis pod, and getting the key again to test the PVC. 
```bash
pip install redis
pip install ipython
ipython
```
```python
In [1]: import redis

In [2]: rd = redis.StrictRedis(host='10.104.165.3', port=6379, db=0)

In [3]: rd.set('k','v')
Out[3]: True

In [4]: rd.get('k')
Out[4]: b'v'

In [5]: # Delete the redis pod: `kubectl delete pods bradenp-test-redis-deployment-56bd9675f6-ph9lv` from another shell.

In [6]: # Wait a bit for the redis deployment to create a new pod.

In [7]: rd.get('k')
Out[7]: b'v'

In [8]: rd.delete('k')
Out[8]: 1

In [9]: exit
```

* Make sure to delete all keys before you leave, or you will probably create issues when interacting with flask.
#
## Flask:
Now that we have verified that the Redis database is working, we can interact with our Flask app. The routes should be the same as those described in the [midterm homework](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework_midterm). `localhost` should be replaced with the cluster IP of the flask service. In my case, it is `10.98.225.212`. The port is `5000`.

One new route was added to generate animals (which was previously done in a separate python script). From the command line of the python debug pod:

```bash
curl '<flask-IP>:5000/animals/generate'
```

All other routes follow the same format. For example, try 
```bash
curl '<flask-IP>:5000/animals'
````
to get all of the animals in the redis database. See [/homework_midterm](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework_midterm) for more routes.

The debug pod can be exited by typing `exit` into the command line.

# Removal

Pods, deployments, services, and PVCs can be deleted with:

```bash
kubectl delete <type> <name>
```
Several names can be inputted at once (separated with a space).