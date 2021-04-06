# A

1.
```yml
---
apiVersion: v1
kind: Pod
metadata:
  name: hello-personalized-bspA
  labels:
    greeting: personalized
spec:
  containers:
    - name: hello
      image: ubuntu:18.04
      command: ['sh', '-c', 'echo "Hello, $NAME" && sleep 3600']
```

```bash
[bradenp@isp02 homework05]$ kubectl apply -f pod-personalized-helloA.yml
pod/hello-personalized-bspA created
```


2.
```bash
[bradenp@isp02 homework05]$ kubectl get pods hello-personalized-bspA
NAME                     READY   STATUS    RESTARTS   AGE
hello-personalized-bspA   1/1     Running   0          2m22s
```

3.
```bash
[bradenp@isp02 homework05]$ kubectl logs hello-personalized-bspA 
Hello, 
```

4.
```bash
[bradenp@isp02 homework05]$ kubectl delete pods hello-personalized-bspA
pod "hello-personalized-bspA" deleted
```

# B

1.
```yml
---
apiVersion: v1
kind: Pod
metadata:
  name: hello-personalized-bspB
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
[bradenp@isp02 homework05]$ kubectl apply -f pod-personalized-helloB.yml 
pod/hello-personalized-bspB created
```

2.
```yml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-deployment-personalized-c
  labels:
    app: hello-personalized
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-app
  template:
    metadata:
      labels:
        app: hello-app
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
[bradenp@isp02 homework05]$ kubectl logs hello-personalized-bspB 
Hello, Braden
```

3.
```bash
[bradenp@isp02 homework05]$ kubectl delete pods hello-personalized-bspB
pod "hello-personalized-bspB" deleted
```

# C

1.
```bash
[bradenp@isp02 homework05]$ kubectl apply -f deployment-personalized-helloC.yml
deployment.apps/hello-deployment-personalized-c created
```

2.
```bash
[bradenp@isp02 homework05]$ kubectl get pods -o wide
NAME                                               READY   STATUS    RESTARTS   AGE     IP              NODE                         NOMINATED NODE   READINESS GATES
hello-deployment-personalized-c-5864c4d866-qh5s4   1/1     Running   0          5m30s   10.244.4.123    c02                          <none>           <none>
hello-deployment-personalized-c-5864c4d866-wcczj   1/1     Running   0          5m30s   10.244.10.238   c009.rodeo.tacc.utexas.edu   <none>           <none>
hello-deployment-personalized-c-5864c4d866-zrzkm   1/1     Running   0          5m30s   10.244.5.88     c04                          <none>           <none>
```

3.
```bash
[bradenp@isp02 homework05]$ kubectl logs -f hello-deployment-personalized-c-5864c4d866-qh5s4 
Hello, Braden from IP 10.244.4.123
```

```bash
[bradenp@isp02 homework05]$ kubectl logs -f hello-deployment-personalized-c-5864c4d866-wcczj 
Hello, Braden from IP 10.244.10.238
```

```bash
[bradenp@isp02 homework05]$ kubectl logs -f hello-deployment-personalized-c-5864c4d866-zrzkm 
Hello, Braden from IP 10.244.5.88
```