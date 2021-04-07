# Homework 5: Kubernetes

This directory contains my submission for the fifth homework of COE 332.

## A

Create a pod that prints "Hello $NAME", where `$NAME` is an environment variable.

1. Yaml file used and command issued to create a pod:
```yml
---
apiVersion: v1
kind: Pod
metadata:
  name: hello-personalized-a
  labels:
    greeting: personalized
spec:
  containers:
    - name: hello
      image: ubuntu:18.04
      command: ['sh', '-c', 'echo "Hello, $NAME" && sleep 3600']
```

```bash
[bradenp@isp02 homework05]$ kubectl apply -f bradenp-hello-personalized-a-pod.yml 
pod/hello-personalized-a created
```


2. Issue a command to get the pod using an appropriate `selector`:
```bash
[bradenp@isp02 homework05]$ kubectl get pods --selector greeting=personalized
NAME                                               READY   STATUS    RESTARTS   AGE
hello-personalized-a                               1/1     Running   0          20s
```

3. Check the logs of the pod:
```bash
[bradenp@isp02 homework05]$ kubectl logs hello-personalized-a
Hello, 
```
This is what I expected. The environment variable `$NAME` does not have a definition, so nothing is outputted in its place in the `echo` command.

4. Delete the pod:
```bash
[bradenp@isp02 homework05]$ kubectl delete pods hello-personalized-a
pod "hello-personalized-a" deleted
```

## B

Define an environment variable `NAME` and give it the value of your own name

1. Yaml file used and command issued to create a pod:
```yml
---
apiVersion: v1
kind: Pod
metadata:
  name: hello-personalized-b
  labels:
    greeting: personalized
spec:
  containers:
    - name: hello
      image: ubuntu:18.04
      env:
        - name: "NAME"
          value: "Braden"
      command: ['sh', '-c', 'echo "Hello, $NAME" && sleep 3600']
```


```bash
[bradenp@isp02 homework05]$ kubectl apply -f bradenp-hello-personalized-b-pod.yml 
pod/hello-personalized-b created
```

2. Check the logs of the pod:
```bash
[bradenp@isp02 homework05]$ kubectl logs hello-personalized-b
Hello, Braden
```

3. Delete the pod:
```bash
[bradenp@isp02 homework05]$ kubectl delete pods hello-personalized-b
pod "hello-personalized-b" deleted
```

## C

Create a deployment with the previous properties and three replicas, and have each pod send its IP address in its message. 

1. Yaml file used and command issued to create the deployment:
```yml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-personalized-c-deployment
  labels:
    app: hello-personalized-c
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-personalized-c
  template:
    metadata:
      labels:
        app: hello-personalized-c
        greeting: personalized
    spec:
      containers:
        - name: hellos
          image: ubuntu:18.04
          env:
            - name: "NAME"
              value: "Braden"
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          command: ['sh', '-c', 'echo "Hello, $NAME from IP $POD_IP" && sleep 3600']
```
```bash
[bradenp@isp02 homework05]$ kubectl apply -f bradenp-hello-personalized-c-deployment.yml
deployment.apps/hello-personalized-c-deployment created
```

2. Use kubectl to get all the pods in the deployment and their IP addresses:
```bash
[bradenp@isp02 homework05]$ kubectl get pods --selector greeting=personalized -o wide
NAME                                               READY   STATUS    RESTARTS   AGE    IP              NODE                         NOMINATED NODE   READINESS GATES
hello-deployment-personalized-c-5c449554fc-5d5d8   1/1     Running   0          5m5s   10.244.10.250   c009.rodeo.tacc.utexas.edu   <none>           <none>
hello-deployment-personalized-c-5c449554fc-cw92f   1/1     Running   0          5m5s   10.244.4.127    c02                          <none>           <none>
hello-deployment-personalized-c-5c449554fc-jmfqk   1/1     Running   0          5m5s   10.244.5.101    c04                          <none>           <none>
```

3. Check the logs of each pod:
```bash
[bradenp@isp02 homework05]$ kubectl logs hello-deployment-personalized-c-5c449554fc-5d5d8 
Hello, Braden from IP 10.244.10.250
[bradenp@isp02 homework05]$ kubectl logs hello-deployment-personalized-c-5c449554fc-cw92f
Hello, Braden from IP 10.244.4.127
[bradenp@isp02 homework05]$ kubectl logs hello-deployment-personalized-c-5c449554fc-jmfqk 
Hello, Braden from IP 10.244.5.101
```

The IPs in the log match the IPs we got in `2`.