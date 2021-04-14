# Homework 6: Deploying Flask API to k8s

This homework builds off of homeworks 1,2,3, and the midterm. This directory contains all of the files required to interact with the animals flask app (from previous homeworks) in Kubernetes.

# Dependencies

Trivially, k8s is required. Docker is required if the user wishes to customize the flask app. All other dependencies are handled by k8s and docker.

# Installation

The files can be cloned from this repo:

```bash
git clone https://github.com/bradenpecora/bsp825-coe332.git
```

Navigate to the `homework06` directory. The redis service must be the first thing installed since the flask deployment will need its IP. To apply the redis service and find its IP:

```bash
[bradenp@isp02 homework06]$ kubectl apply -f bradenp-test-redis-service.yml
service/bradenp-test-redis-service created
```
```bash
[bradenp@isp02 homework06]$ kubectl get services --selector username=bradenp
NAME                         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
bradenp-test-redis-service   ClusterIP   10.104.165.3   <none>        6379/TCP   14s
```

*** Take note of the Cluster-IP. Open `bradenp-test-flask-deployment.yml` in a text editor. In line 32 of the file, change the value of the environment variable `REDIS_IP` to the Cluster-IP of the redis service. Save the file and return to the command line.

Note: The user can force an IP of the redis service. See line 10 of `bradenp-test-redis-service.yml` and reapply the service if you wish to do so.


To start the remaining deployments, services, and PVCs:

```bash
[bradenp@isp02 homework06]$ kubectl apply -f .
````

Take note of the `.` at the end of the command.

# Usage

All pods, deployments, and services should be up and running. To test, check to see if all of the following are running:

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
Take note of the the Cluster-IP of the flask service. We will use this IP to interact with the app later.

Note: The selectors `app=bradenp-test-flask` and `app=bradenp-test-redis` were created to connect the services to the pods, but they can be used to get a specifically the flask or redis pod(s) as well.

#
## Redis:

Now that we have verified that everything is running, `exec` into a python debug pod. I have provided one, but you can use your own.
```bash
kubectl exec -it <name-of-debug-pod> -- /bin/bash
```


To make sure the redis deployment and service are running properly, you can start an interactive python shell within the debug pod. We can do so using `ipython`, or an alternative. Make sure to install the `redis` python package.

```bash
$ pip install redis ipython
$ ipython
```
```python
In [1]: import redis

In [2]: rd = redis.StrictRedis(host='<Redis IP>', port=6379, db=1) 
# Change <Redis IP> to the IP of the Redis service.
# Use db=1 to not interfere with database used by the flask app (db=0).

In [3]: rd.set('k','v')
Out[3]: True

In [4]: rd.get('k')
Out[4]: b'v'

In [5]: # Delete the redis pod: `kubectl delete pods <name-of-redis-pod>` from another shell.

In [6]: # Wait a few seconds for the redis deployment to create a new pod.

In [7]: rd.get('k')
Out[7]: b'v'

In [8]: exit
```

#
## Flask:
Now that we have verified that the Redis database is working, we can interact with our Flask app. The routes should be the same as those described in the [midterm homework](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework_midterm). The IP address of the URL `localhost` should now be replaced with the Cluster-IP of the flask service, which was found earlier. The port is `5000`. The basic form of a curl against the URL of a route is:

```bash
$ curl '<flask-IP>:5000/route'
```

One new route was added to generate animals (which was previously done in a separate python script). From the command line of the python debug pod:

```bash
$ curl '<flask-IP>:5000/animals/generate'
```

All other routes follow the same format. For example, try 
```bash
$ curl '<flask-IP>:5000/animals'
````
to get all of the animals in the redis database. See [/homework_midterm](https://github.com/bradenpecora/bsp825-coe332/tree/main/homework_midterm) for more routes.

The debug pod can be exited by typing `exit` into the command line.

# Removal

Pods, deployments, services, and PVCs can be deleted with:

```bash
[bradenp@isp02 homework06]$ kubectl delete <type> <name>
```
Several names can be inputted at once, and are separated with a space.