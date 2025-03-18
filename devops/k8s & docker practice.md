by Qinyu Chen

# 配置Cluster
测试集群：

| node name | ip | role |
| --- | --- | --- |
| atlas | 10.86.1.157 | master |
| aiden | 10.86.1.156 | worker |
| joshuatree | 10.86.1.161 | worker |






1. 每个node装docker

```python
sudo apt-get update
```

sudo apt-get install docker.io


2. 每个node安装kubelet kubeadmin kubectl

```python
echo "deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg |sudo apt-key add -
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
```


3. master节点（atlas）


```plain
查看守护进程状态
systemctl status kubelet
systemctl status docker

关闭交换分区
swapon -s
sudo swapoff -a
swapon -s

sudo kubeadm init --apiserver-advertise-address=10.86.1.157 --pod-network-cidr=10.244.0.0/16
```

output:

```plain
qinyuchen@atlas:~$ sudo kubeadm init --apiserver-advertise-address=10.86.1.157 --pod-network-cidr=10.244.0.0/16
[init] Using Kubernetes version: v1.28.1
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
W0913 16:50:30.360824   24023 checks.go:835] detected that the sandbox image "registry.k8s.io/pause:3.6" of the container runtime is inconsistent with that used by kubeadm. It is recommended that using "registry.k8s.io/pause:3.9" as the CRI sandbox image.
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [atlas kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 10.86.1.157]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [atlas localhost] and IPs [10.86.1.157 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [atlas localhost] and IPs [10.86.1.157 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 5.503219 seconds
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --upload-certs
[mark-control-plane] Marking the node atlas as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers]
[mark-control-plane] Marking the node atlas as control-plane by adding the taints [node-role.kubernetes.io/control-plane:NoSchedule]
[bootstrap-token] Using token: 87wpfv.y4whl8j58bbztq08
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.86.1.157:6443 --token 87wpfv.y4whl8j58bbztq08 \
	--discovery-token-ca-cert-hash sha256:583b493f6c718b1e253e1f9d78de6cc69ddbe7bb848850595a8f30ee4b7dc5f7
```



4. 使非root能使用kubectl

```plain
qinyuchen@atlas:~$ mkdir -p $HOME/.kube
qinyuchen@atlas:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
qinyuchen@atlas:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```



5. 配置pod网络

```plain
sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

6. 加入cluster

在master拿到加入命令

```plain
qinyuchen@atlas:~$ kubeadm token create --print-join-command
kubeadm join 10.86.1.157:6443 --token 3qof1r.1fp95ykjxqzj0goi --discovery-token-ca-cert-hash sha256:583b493f6c718b1e253e1f9d78de6cc69ddbe7bb848850595a8f30ee4b7dc5f7 
```

在node运行

```plain
qinyuchen@aiden:~$ sudo kubeadm join 10.86.1.157:6443 --token 3qof1r.1fp95ykjxqzj0goi --discovery-token-ca-cert-hash sha256:583b493f6c718b1e253e1f9d78de6cc69ddbe7bb848850595a8f30ee4b7dc5f7 
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...


This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.


Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

7. 查看nodes状态

```plain
qinyuchen@atlas:~$ kubectl get nodes
NAME         STATUS     ROLES           AGE   VERSION
aiden        NotReady   <none>          72s   v1.28.1
atlas        Ready      control-plane   13m   v1.28.1
joshuatree   NotReady   <none>          29s   v1.28.1

qinyuchen@atlas:~$ kubectl get pod --all-namespaces
NAMESPACE      NAME                            READY   STATUS     RESTARTS   AGE
kube-flannel   kube-flannel-ds-hcxwn           1/1     Running    0          12m
kube-flannel   kube-flannel-ds-lwv8m           1/1     Running    0          2m21s
kube-flannel   kube-flannel-ds-w2rc7           0/1     Init:1/2   0          98s
kube-system    coredns-5dd5756b68-2zk2q        1/1     Running    0          14m
kube-system    coredns-5dd5756b68-fld9q        1/1     Running    0          14m
kube-system    etcd-atlas                      1/1     Running    1          14m
kube-system    kube-apiserver-atlas            1/1     Running    1          14m
kube-system    kube-controller-manager-atlas   1/1     Running    0          14m
kube-system    kube-proxy-bvrcp                1/1     Running    0          98s
kube-system    kube-proxy-rjf4j                1/1     Running    0          2m21s
kube-system    kube-proxy-t68h7                1/1     Running    0          14m
kube-system    kube-scheduler-atlas            1/1     Running    1          14m

发现有一个在init，等待一段时间后

qinyuchen@atlas:~$ kubectl get pod --all-namespaces
NAMESPACE      NAME                            READY   STATUS    RESTARTS   AGE
kube-flannel   kube-flannel-ds-hcxwn           1/1     Running   0          14m
kube-flannel   kube-flannel-ds-lwv8m           1/1     Running   0          4m
kube-flannel   kube-flannel-ds-w2rc7           1/1     Running   0          3m17s
kube-system    coredns-5dd5756b68-2zk2q        1/1     Running   0          16m
kube-system    coredns-5dd5756b68-fld9q        1/1     Running   0          16m
kube-system    etcd-atlas                      1/1     Running   1          16m
kube-system    kube-apiserver-atlas            1/1     Running   1          16m
kube-system    kube-controller-manager-atlas   1/1     Running   0          16m
kube-system    kube-proxy-bvrcp                1/1     Running   0          3m17s
kube-system    kube-proxy-rjf4j                1/1     Running   0          4m
kube-system    kube-proxy-t68h7                1/1     Running   0          16m
kube-system    kube-scheduler-atlas            1/1     Running   1          16m

qinyuchen@atlas:~$ kubectl get nodes
NAME         STATUS   ROLES           AGE     VERSION
aiden        Ready    <none>          4m19s   v1.28.1
atlas        Ready    control-plane   16m     v1.28.1
joshuatree   Ready    <none>          3m36s   v1.28.1
```

8.直接创建并运行一个nginx pod

```plain
qinyuchen@atlas:~$ kubectl run nginx --image=nginx
pod/nginx created
qinyuchen@atlas:~$ kubectl get pod -o wide
NAME    READY   STATUS    RESTARTS   AGE   IP           NODE         NOMINATED NODE   READINESS GATES
nginx   1/1     Running   0          19m   10.244.2.2   joshuatree   <none>           <none>
```

删除

```plain
qinyuchen@atlas:~$ kubectl delete pod nginx
pod "nginx" deleted
```



9.deployment

```plain
qinyuchen@atlas:~$ kubectl create deployment nginx-deployment  --image=nginx:1.7.9 --replicas=2
deployment.apps/nginx-deployment created
qinyuchen@atlas:~$ kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   0/2     2            0           90s
qinyuchen@atlas:~$ kubectl get deployments nginx-deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2/2     2            2           2m12s
```

kubectl 创建 deployment

deployment 创建 replicaset

replicaset 创建 pod



删除deployment

```plain
qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2/2     2            2           3h34m
qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl delete deployment nginx-deployment
deployment.apps "nginx-deployment" deleted
```



使用yaml deployment

```plain
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

执行

```plain
qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl apply -f nginx-deployment.yaml 
deployment.apps/nginx-deployment created

qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl get pod -o wide
NAME                                READY   STATUS    RESTARTS   AGE     IP           NODE         NOMINATED NODE   READINESS GATES
nginx-deployment-86dcfdf4c6-d5zqp   1/1     Running   0          7m16s   10.244.1.5   aiden        <none>           <none>
nginx-deployment-86dcfdf4c6-qwh82   1/1     Running   0          7m16s   10.244.2.6   joshuatree   <none>           <none>
```



10. 容器分类

服务类容器：Deployment, Replicaset, DaemonSet 长期运行

工作类容器：Job (一次性任务)， CronJob(定时任务)



运行Job

```plain
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

执行

```plain
qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl apply -f job.yaml 
job.batch/pi created

qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl get job
NAME    COMPLETIONS   DURATION   AGE
myjob   1/1           67s        94s
pi      1/1           9m38s      10m

qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl logs pi-qcvk4 
3.14159265358979323846264338327950288419716939937510582097494459230781


qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl logs myjob-9s4dj
hello k8s job!
```



并行任务

```plain
apiVersion: batch/v1
kind: Job
metadata:
  name: myjob
spec:
  completions: 6   # 每次运行2个pod，直到6个pod成功
  parallelism: 2	
  template:
    spec:
      containers:
      - name: hello
        image: busybox
        command: ["echo",  "hello k8s job!"]
      restartPolicy: Never
```

执行

```plain
qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl apply -f job2.yaml 
job.batch/myjob created

qinyuchen@atlas:/nfs/workspace/qinyuchen/k8s$ kubectl get job
NAME    COMPLETIONS   DURATION   AGE
myjob   6/6           21s        30s
```





# 创建本地registry
主机执行
docker run -d -p 5000:5000 --restart=always --name registry registry:2

docker pull python:3.8.13

docker tag python:3.8.13 10.86.1.157:5000/python:3.8.13

docker push 10.86.1.157:5000/python:3.8.13

每台node配置 /etc/docker/daemon.json

```plain
{
  "insecure-registries": [
    "http://10.86.1.157:5000"
  ]
}
```

重启  
sudo systemctl restart docker

运行docker info 验证配置生效

根据我的测试，该配置仅用于docker pull，对k8s拉取镜像没有影响



每个node执行以下步骤：

参考[https://stackoverflow.com/questions/65681045/adding-insecure-registry-in-containerd](https://stackoverflow.com/questions/65681045/adding-insecure-registry-in-containerd)

1. 若不存在 /etc/containerd/config.toml 

执行containerd config default 生成默认配置

2. 修改内容

```yaml
# /etc/containerd/config.toml
# change <IP>:5000 to your registry url

[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."<IP>:5000"]
      endpoint = ["http://<IP>:5000"]
  [plugins."io.containerd.grpc.v1.cri".registry.configs]
    [plugins."io.containerd.grpc.v1.cri".registry.configs."<IP>:5000".tls]
      insecure_skip_verify = true
```

3. 重启服务

sudo systemctl restart containerd

测试yaml:

```plain
apiVersion: batch/v1
kind: Job
metadata:
  name: pyjob
spec:
  template:
    spec:
      containers:
      - name: py-container
        image: 10.86.1.157:5000/python:3.8.13
        imagePullPolicy: IfNotPresent
        command: ["python", "-c", "print('hello')"]
      restartPolicy: Never
  backoffLimit: 4
```

kubectl apply -f test.yaml

# 制作镜像
在docker build时能够使用gpu，需执行：

```plain
sudo curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
sudo curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update

sudo apt-get install nvidia-container-runtime
sudo vim /etc/docker/daemon.json

添加或修改以下内容
'''
{
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
         } 
    },
    "default-runtime": "nvidia" 
}
''''

sudo systemctl restart docker
```



准备Dockerfile

```plain
FROM nvidia/cuda:11.4.3-devel-ubuntu20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y build-essential && apt-get install -y curl wget && \
    apt-get -y install cmake && \
    apt-get -y install gfortran && \
    apt-get -y install flex && \
    apt-get -y install bison && \
    apt-get -y install libboost-all-dev && \
    apt-get -y install libbz2-dev && \
    rm -rf /var/lib/apt/lists/*

COPY Miniconda3-latest-Linux-x86_64.sh .

RUN mkdir /software && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh  && \
    ./Miniconda3-latest-Linux-x86_64.sh -b -p /software/miniconda3 && \
    rm Miniconda3-latest-Linux-x86_64.sh

COPY condarc /root/.condarc

ENV PATH=/software/miniconda3/bin:$PATH

RUN conda install -c conda-forge mamba

COPY environment.yml /tmp/environment.yml

RUN mamba env create -f /tmp/environment.yml && \
    echo "source activate apps" >> ~/.bashrc
```



build

```plain
docker build -t my_image_name:latest .
```



踩坑：

cuda版本与gcc版本不匹配问题：[https://stackoverflow.com/questions/6622454/cuda-incompatible-with-my-gcc-version](https://stackoverflow.com/questions/6622454/cuda-incompatible-with-my-gcc-version)



# 清理docker占用空间
```python
docker system prune
```
Remove all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes.


# 添加用户到docker组
sudo usermod -aG docker user_name

# 迁移DOCKER
```python
sudo systemctl stop docker
sudo systemctl stop docker.socket
sudo systemctl stop containerd

sudo mkdir -p /new_dir_structure

sudo mv /var/lib/docker /new_dir_structure # 确保filesystem一致

sudo vim /etc/docker/daemon.json

add
{ ...
  "data-root": "/new_dir_structure/docker"
}

sudo systemctl start docker

docker info -f '{{ .DockerRootDir}}'
```

note: 实测从/var/lib/docker迁移到/nfs/ or /zfs/都无法再启动docker，也就是以前的image用不了了，可能是因为filesystem不同导致，所以需要重新拉取镜像

PS: 不建议迁移docker到共享目录，build和启动镜像会很慢

# 迁移kubelet
```python
vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
vi /etc/default/kubelet

add
KUBELET_EXTRA_ARGS=--root-dir=/nfs/workspace/aiden/k8s/kubelet

systemctl daemon-reload
systemctl restart kubelet
```


# DOCKER RUN 挂载目录/使用gpu
```python
docker run -it --gpus all -v /src_path:/docker_path my_image:latest bash
```



# FIX: node not ready 
```plain
systemctl status kubelet
journalctl -e -u kubelet
sudo swapoff -a
sudo systemctl restart kubelet
```

# FIX: node missing from cluster
```plain
kubeadm reset
kubeadm join 10.86.1.157:6443 --token laapdk.8w54b14mr1jtddai --discovery-token-ca-cert-hash sha256:5cfc210c3145fa689d4040bb921ffcd61c7867054e9a72cc85c7974b9345bceb 
```

# Enable GPU nodes in K8S
[https://github.com/NVIDIA/k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)


# 进入POD容器
```plain
kubectl exec -it  <pod name> -- /bin/bash
```
