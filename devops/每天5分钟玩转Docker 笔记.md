# 1启程
```plain
docker run -d -p 80:80 httpd
```

1. 下载 httpd 镜像
2. -d在后台启动容器，容器80端口映射到主机的80端口。



# 2容器技术
## 2.1容器
1. what：一种软件打包技术，使程序可以几乎在任何地方以相同方式运行。
2. why：使软件具备超强的可移植能力，应用可以轻松部署到不同的环境。
    1. for dev: build once, run anywhere
    2. for ops: configure once, run anything
3. how: 
    1. docker架构
        1. docker客户端：client
            1. 通过docker命令行工具构建和运行容器
        2. docker服务器：docker daemon
            1. 以Linux后台服务的方式运行，运行在docker host上，响应客户端请求
            2. 默认只处理host上的请求，若要允许远程客户端请求，需在配置文件中打开tcp监听
        3. docker镜像：Image
            1. 一个用于创建docker容器的只读模版
            2. 构建镜像的步骤可以放在Dockerfile中，通过docker build Dockfile可以构造出镜像
        4. registry
            1. 存放镜像的仓库
        5. docker容器：container
    2. docker run -d -p 80:80 httpd 背后的过程
        1. docker客户端执行命令
        2. docker daemon发现本地没有httpd镜像
        3. daemon从docker hub下载镜像
        4. 下载完成
        5. daemon启动容器



## 2.2Docker镜像
### 最简单的镜像
```plain
docker pull hello-world  # 下载镜像
docker images hello-world # 查看镜像
docker run hello-world # 启动镜像
```

hello-world镜像的Dokcerfile只包含三行：

1. FROM scratch       从0开始构建
2. COPY hello /         将文件'hello' copy到镜像的根目录
3. CMD ["/hello"]	   容器启动时，执行 /hello



该镜像中只有一个可执行文件'hello'，打印出一堆信息，没有什么实际用途。



### base镜像
+ 不依赖其他镜像，从scratch构建。
+ 其他镜像可以以之为基础拓展。
+ Linux操作系统由kernel和rootfs（包含/dev, /proc, /bin等目录）构成，对于base镜像，底层直接且**只能**使用host的kernel，镜像只提供rootfs（centos 200MB）。



### 镜像的分层结构
```plain
FROM debian
RUN apt-get install emacs
RUN apt-get install apache2
CMD ["/bin/bash"]
```

如Dockerfile中描述的一样，在base镜像的基础上，每安装一个软件，就在现有镜像的基础上增加一层。

这样做的好处是资源共享，若多个镜像都由同个base镜像构建而来，那么host上只需要保存一份base镜像，内存中也只需加载一份base镜像，就可以为所有容器服务了。

**容器本身是无法修改基础镜像的内容的**，当容器启动后，一个新的可写层会被加载到镜像的顶部，称为“容器层”，之下的都叫“镜像层”。

所有对容器的改动，都发生在容器层；容器层是**可写**的，镜像层是**只读**的。

所有的镜像层联合在一起组成了一个文件系统，如果不同镜像层有相同的文件，那么上层的会覆盖下层的，即用户只能访问到更上层的文件。

1. 添加文件：在容器中创建文件，新文件被添加到容器层。
2. 读取文件：docker从上到下依次查找此文件，一旦找到，则打开并读入内存。
3. 修改文件：docker从上到下依次查找此文件，一旦找到，**将其复制到容器层**，然后修改之。
4. 删除文件：docker从上到下依次查找此文件，一旦找到，在容器层记录下此删除操作。

**只有当需要修改时才复制一份数据，这种特性被称为 Copy-on-Write。**



### 构建镜像
大多数情况下我们可以直接使用现成的镜像，除非找不到现成的镜像，或需要在镜像中加入特定的功能。

#### docker commit
+ 运行容器
+ 修改容器
+ 将容器保存为新的镜像

```plain
# # on host
docker run -it ubuntu

# inside container
apt-get install -y vim

# on host
docker ps
docker commit silly_goldberg ubuntu-with-vi
```

这种方法是**不推荐**的，原因是容易出错且可复制性弱，也不知道镜像是如何创建出来的。



#### Dockerfile
```plain
FROM ubuntu
RUN apt-get update && apt-get install -y vim
```

1. 将Dockfile准备在当前目录
2. 执行docker build -t ubuntu-with-vi-dockerfile . (.指示在当前目录寻找Dockerfile)



##### 查看镜像的分层结构：
docker history ubuntu-with-vi-dockerfile

##### 镜像缓存
在构建新镜像时，如果某镜像层已经存在，则会直接使用，无需重新创建。

##### 调试Dockerfile
当执行docker build后，在某一行指令出错后，比如step3，那么可以执行docker run -it <step2的镜像id> 运行容器，手动执行step3调试错误。



##### Dockerfile常用指令
###### FROM
指定base镜像

###### MAINTAINER
设置镜像作者

###### COPY
将文件从build context复制到镜像

支持COPY src dest，COPY ["src","dest"]

###### ADD
与COPY类似

###### ENV
设置环境变量，供后续指令使用

###### EXPOSE
指定容器中的进程监听某个端口

###### VOLUMN
将文件或目录声明为 volumn

###### WORKDIR
为后面的RUN, CMD, ENTRYPOINT, ADD, COPY设置当前的工作路径

###### RUN
在容器中运行指定的命令，一般用来安装包

注意：apt-get update && apt-get install 会被放在一个RUN命令执行，这是为了防止使用apt-get update缓存的镜像层，可能已经过时。

###### CMD
容器启动时运行指定的命令，用于为容器设置默认的启动命令

如果docker run 指定了其他命令，CMD指定的命令会被忽略

多个CMD指令，只有最后一个会生效

###### ENTRYPOINT
设置容器启动时运行的命令  
即使docker run 指定了其他命令，也不会被忽略，一定会执行

多个ENTRYPOINT指令，只有最后一个会生效



### 分发镜像
构建镜像后，在多个host使用镜像的方法有：

+ 用相同的Dockerfile构建镜像
+ 将镜像上传到公有Registry，host下载使用
+ 搭建私有的Registry，供本地host使用



#### 为镜像命名
构建镜像时会为镜像指定名字：由仓库和tag构成

docker build -t [repo]:[tag]



默认tag是latest，建议设置成版本号，如1.9

通过docker tag 可以给镜像打tag，如

docker tag myimg-v1.9.1 myimg:1.9



#### 使用公用Registry
在Dokcer hub注册账号后，在host上登陆

docker login -u qinyuchen



为镜像指定远端repo

<font style="color:rgb(23, 25, 30);">docker tag getting-started qinyuchen/getting-started</font>

<font style="color:rgb(23, 25, 30);"></font>

推送镜像

docker push <font style="color:rgb(23, 25, 30);">qinyuchen</font>/getting-started



#### 搭建本地Registry
启动registry docker容器作为本地仓库



### 小结
常用docker命令

+ images: 显示镜像列表
+ history: 镜像构建历史
+ commit: 从容器创建镜像
+ build: 从Dockerfile构建镜像
+ tag：给镜像打tag
+ pull：从registry下载镜像
+ push：将镜像上传到registry
+ rmi：删除Docker host中的镜像
+ search：搜索Docker hub中的镜像



## 2.3Docker容器
### 运行容器
docker run ubuntu pwd



docker ps # 查看正在运行的容器



docker ps -a # 查看所有运行和运行过的容器



docker run -d ubuntu --name 'ubuntu'

-d可以让容器在后台运行

--name可以为容器命名



docker stop [CONTAINER_ID] 可以停止容器



#### 进入容器
+ docker attach [CONTAINER_ID]

ctrl+p, ctrl+q组合键退出终端

+ docker exec

docker exec it  [CONTAINER_ID] bash

-it 以交互模式打开psesudo-TTY, 执行 bash

exit退出容器



attach直接进入容器启动的终端，不会启动新的进程；exec则是在容器中打开新的终端。



#### 运行容器最佳实践
服务类容器，如Web服务器、数据库等，通过-d在后台启动是合适的，需要故障排查时，通过exec -it进入容器。

工具类容器，提供了临时的工作环境，通常以run -it启动，完成工作后执行exit退出终端。



### stop/start/restart
docker stop可以停止容器，实际容器只是一个在host中的进程，如果想快速停止容器，可以使用docker kill命令。

对于停止的容器，可以通过docker start重新启动，会保留第一次启动时的所有参数。

docker restart = docker stop + docker start



对于服务类容器，我们通常希望容器能自动重启：

docker run -d --restart=always httpd

--restart=always意味无论何种原因退出，都将立即重启。

--restart=on-failure:3，意思是若退出代码非0则重启容器，最多重启3次。

#### 
### pause/unpause
docker pause让容器暂停工作一段时间，此时容器不会占用cpu资源。

docker unpauser让容器恢复工作。



### 删除容器
退出了的容器仍会占用host的文件系统资源，可以通过docker rm 删除无用的容器。

docker rm -v $(docker ps -aq -f status=exited) 可以批量删除所有已经退出的容器。



### state machine
![](https://cdn.nlark.com/yuque/0/2023/png/33590654/1693294665017-aa9861c0-92db-4485-ad0d-51f65d0a27b6.png)



### 资源限制
#### 内存限额
docker run -m 200M --memory-swap=300M ubuntu

-m设置内存的使用限额

--memory-swap设置内存+swap（虚拟内存）的使用限额

含义是最多使用200MB的内存和100MB的swap，默认情况下没有限制。



docker run -it -m 200M ubuntu

如果只设置-m，那么默认--memory-swap是-m的两倍。



#### CPU限额
docker -c设置容器使用cpu的权重（优先级），默认为1024。



#### Block IO 带宽限额
设置权重、限制bps和iops的方式来控制容器读写磁盘的带宽。

--blkio-weight 设置权重值，默认是500



bps是byte per second，每秒读写数据量；iops是io per sec，每秒IO的次数。

可通过以下参数控制bps, iops：

+ --device-read-bps
+ --device-write-bps
+ --device-read-iops
+ --device-write-iops



### 实现容器的底层技术
#### cgroup
control group，linux通过cgroup设置进程使用cpu，内存和io资源的限额。上面限制资源实际上是在配置cgroup。

在/sys/fs/cgroup/cpu/docker下，linux会为每个容器创建一个cgroup目录，以长id命名，同样也有memory/docker, bikio/docker保存内容和io的配置。



#### namespace
namespace实现了容器资源间的隔离，使得容器更像一台独立的计算机。

Mount namespace: 让容器有自己的根目录

UTS namespace: 让容器有自己的hostname

IPC namespace：让容器有自己的共享内存和信号量来实现进程间通信

PID namespace：容器在host中以进程的形式运行

Network namespace：让那个容器拥有独立的网卡、ip等资源

User namespace：让容器能够管理自己的用户



### 小节
create: 创建容器

run：运行容器

pause：暂停容器

unpause：取消暂停继续运行容器

stop：发送SIGTERM停止容器

kill：发生SIGKILL快速停止容器

start：启动容器

restart：重启容器

attach：attach到容器启动进程的终端

exec：在容器中开启并进入新终端，使用-it

logs：显示容器启动进程的控制台输出，使用-f持续打印

rm：从磁盘删除容器



## 2.4Docker网络
dokcer在安装时会在host上创建3个网络，可以使用docker network ls查看：

```plain
chenqinyu@chenqinyus-MacBook-Pro ~ % docker network ls
NETWORK ID     NAME          DRIVER    SCOPE
10b6248fb035   bridge        bridge    local
e6ab6c21ca04   host          host      local
cf9c6039bcbf   none          null      local
```

### none网络
挂在该网络下的容器只有localhost，没有其他任何网卡。

一般用于安全性要求高且不需要联网的应用，比如用于生成随机密码的应用。



### host网路
连接到host网络的容器与host共享网络栈，容器的网络配置与host一样。

可通过--network=host指定使用host网络。

好处是性能好，容器可以直接配置host网络，但是要避免端口冲突。



### bridge网络
docker安装时会创建一个名为docker0的linux bridge，若不指定--network，所有容器默认挂到docker0上。

当创建容器时，一个新的网络接口会挂到docker0上，该接口名与容器内的虚拟网卡是一对veth(<font style="color:rgb(0, 0, 0);background-color:rgb(247, 247, 247);">Virtual Ethernet</font>) pair，这两个接口通过一个虚拟网络连接相互关联。



### user-defined网络
docker提供三种user-defined网络驱动：bridge, overlay和macvlan。

overlay和macvlan用于跨主机，后续学习。



可通过

docker network create --driver bridge my_net

创建bridge网络。



在创建时可以指定ip网段：

docker network create --driver bridge --subnet 172.22.16.0/24 --gateway 172.22.16.1 my_net

  
在启动容器时可以指定静态ip

docker run -it --network=my_net --ip 172.22.16.8 busybox



挂在相同network上的两个容器间网络是互通的。



### 容器间通信
容器间可通过IP, Docker DNS Server或joined容器三种方式通信。



#### IP通信
为不同容器指定相同的network，同一network里的容器可以通过ip通信。



#### Docker DNS Server
IP通信虽然满足通信，但不够灵活，在启动容器时，使用--name为容器命名即可通过容器名通信：

docker run -it --network=my_net --name=box1 busybox

docker run -it --network=my_net --name=box2 busybox

ping -c 3 box1



-c 3表示发送3个ping请求到box1上，并在收到所有请求到回应后终止。



DNS服务只能在user-defined网络中使用，默认bridge网络是无法使用DNS的。



#### joined容器
可以使多个容器共享一个网络栈，共享网卡和配置信息（网卡mac地址和ip完全一样）

docker run -d -it --name=web1 httpd 

docker run -it --network=container:web1 busybox



适合场景：

1. 不同容器中的程序希望通过loopback（本地主机上的通信，不需要经过物理网络）高速通信，比如Web Server和App Server。
2. 希望监控其他容器的网络流量，比如运行在独立容器的网络监控程序。



### 将容器与外部世界连接
#### 容器访问外部
默认情况下，host可以访问外网的话，容器也能访问外网。

容器位于docekr0这个网络下，当向外ping时，根据NAT（网络和网络地址转换）表的规则，除了私有subnet内的请求，其他请求由MASQUERADE处理。

p.s. 当网络设备收到一个数据包时，它会检查 NAT 表以确定数据包的源地址和目标地址是否需要进行转换。如果需要转换，设备将根据 NAT 表中的规则修改数据包的地址和端口信息，然后将数据包转发到适当的目的地。

MASQUERADE（马斯克雷德，意为伪装）是一种NAT技术，用于修改出站数据包的源IP地址，将其替换为NAT设备的出口接口的IP地址。



masquerade会把包的源地址替换为host的地址发送出去。



#### 外部访问容器
docker可将容器对外提供服务的端口映射到host的某个端口，外网通过该端口访问容器。

```plain
chenqinyu@chenqinyus-MacBook-Pro ~ % docker run -d -p 80 httpd
dc7a9eb0102cf95bfdca497ac76c275db1930642da646cdb75579fb1ac9ee9c7
chenqinyu@chenqinyus-MacBook-Pro ~ % docker port dc7a9eb0102cf95bfdca497ac76c275db1930642da646cdb75579fb1ac9ee9c7
80/tcp -> 0.0.0.0:54703
```

httpd容器的80端口被映射到host的54703上，这样就可以通过<host ip>:54703访问容器的Web服务了。



上面的端口是随机分配，也可以指定固定端口映射：

docker run -d -p 8080:80 httpd

将容器的80映射到host的8080



每一个映射的端口，host都会启动一个docker-proxy进程来处理访问容器的流量。

![](https://cdn.nlark.com/yuque/0/2023/png/33590654/1693385858215-12276781-3e4c-49f8-a8d3-e5dbf896da3c.png)

### 小节
none: 无网络连接

host：与host一样的网络配置

bridge：docker会创建默认网络docker0(linux bridge)，新建的容器会有一个接口挂在docker0上，容器内的虚拟网卡与这个接口是一对veth pair



## 2.5Docker存储
docker为容器提供了两种存放数据的资源：

1. 由storage driver管理的镜像层和容器层
2. Data Volumn



### storage driver
根据docker镜像的分层结构：

1. 新数据直接存放到容器层（容器启动时，自动创建容器层）
2. 修改现有数据，先复制到容器层，再修改
3. 对于多层中的相同文件，用户只能看到最上层的文件

正是storage driver实现了多层数据的堆叠并为用户提供一个单一的合并后的统一视图。

docker会根据当前系统配置选择默认的driver， 如ubuntu默认driver用的是AUFS(Advanced Multi-Layered Unification Filesystem) 

对于无状态的应用，无状态意味没有需要持久化的数据，直接将数据放在storage driver维护的层是很好的选择，使用完直接退出，容器退出后容器层将被丢弃；再次启动后容器将以初始状态启动。

对于需要持久化数据的应用，就需要使用data volumn。



### data volumn
data volumn本质是docker host文件系统中的目录或文件，能够被直接mount到容器的文件系统中。

1. 容器可以读写volumn中的数据
2. volumn数据可被永久保存，即使使用它的容器已被销毁。

#### bind mount
bind mount将host上已存在的目录或文件mount到容器。

docker run -d -p 80:80 -v ~/htdocs:/usr/local/apache2/htdocs httpd

-v <host path>:<container path>:<container permisson>

<container permisson>设为ro，让容器只有读取权限



应用场景：

将源代码目录mount到容器中，修改代码就能看到实际效果；将MySQL容器的数据放在bind mount里，host方便备份迁移数据。

缺点是bind mount要指定host的文件路径，限制了容器的可移植性。



#### docker managed volumn
docker managed volumn不需要指定mount源

docker run -d -p 80:80 -v /usr/local/apache2/htdocs httpd



每当容器申请mount docker managed volumn时，docker都会生成一个目录作为mount源，

通过docker inpect <id> 可以找到volumn在host的位置。

如果需要mount的目录已存在，那么会将数据复制到mount源。



| 不同点 | bind mount | docker managed mount |
| --- | --- | --- |
| volumn 位置 | 任意指定 | docker指定 |
| 对已有mount point影响 | 隐藏并替换为volumn（host），容器中的文件/目录将被隐藏 | 原有数据复制到volumn |
| 是否支持单个文件 | 支持 | 不支持，只支持目录 |
| 移植性 | 弱，与host绑定 | 强，无需指定host目录 |




### 数据共享
#### 容器与host共享数据
1. bind mount直接将要共享的目录mount到容器。
2. docker managed volumn是在容器启动后才生成在host的目录，需要将要共享的数据拷贝到volumn中。

docker cp 可以帮助在host和容器之间拷贝数据：

docker cp <host file path> <container id>:<container file path>



#### 容器之间共享数据
使用bind mount，将相同的volumn挂载到多个容器。



### volumn container
专门为其他容器提供volumn的容器



docker create --name vc_data -v ~/htdocs:/usr/local/apache2/htdocs -v ~/tools busybox

使用create表示只是创建并不运行容器，该容器挂载了两个volumn



其他容器可以使用这个vc_data

docker run --name web -d -p 80 --volumns-from vc_data httpd

这样web容器就使用了和vc_data一样的volumn



好处：

1. 不必为每个容器指定host path，只需与volumn container关联，实现了容器与host的解耦。
2. 使用volumn container的容器，其mount point是一致的，有利于配置的规范和标准化，也带了一定局限性。

### data volumn生命周期管理
#### 备份
实际上是备份host上的文件/目录



#### 恢复
将备份数据拷贝到volumn里



#### 销毁
对于bind mount，删除数据由host负责。

对于docker managed volumn，在删除容器docker rm时使用-v，可以一同销毁容器使用的volumn，前提是没有其他容器也使用该volumn。若没有带-v，可能产生孤儿volumn，可以使用docker volumn ls查看， docker volumn rm删除。



### 小节
1. docker的两种数据存储：数据层、Data Volumn
2. 数据层包括镜像层、容器层，由storage driver管理
3. Data Volumn有两种：bind mount、docker managed volumn
4. bind mount实现容器与host间、容器与容器间共享数据
5. volumn container 是专为容器提供volumn的容器，实现了容器与host的解耦





# 3容器进阶
## 3.1多主机管理
用docker machine可以批量安装和配置docker host，host可以是虚拟机、物理机、云主机。

创建host

docker-machine --driver generic --generic-ip-address=192.168.56.104 host1

执行命令后，会ssh到远程主机并安装docker，配置docker daemon并启动docker



docker-machine ls

可以看到运行的host



docker-machine env host1

可以看到host1的docker相关的环境变量



eval $(docker-machien env host1)

此时使用docker命令等同于在host1上执行



docker-machine upgrade host1

更新host1的docker



docker-machine config host1

查看host1的配置



docker-machine scp host1:/tmp/a host2:/tmp/b

在不同host间复制文件

## 3.2容器网络
跨主机网络方案包括：

1. docker原生的overlay和macvlan
2. 第三方方案：flannel、weave、calico



### libnetwork & CNM
libnetwork是docker容器网络库，核心内容是定义了Container Networkf Model，该模型对容器网络进行了抽象，由以下三类组件组成：



1. Sandbox

容器的网络栈，包含接口、路由器、DNS设置。 Sandbox可以包含来自不同网络的Endpoint

2. Endpoint

将Sandbox接入Network，典型实现是veth pair(容器内的虚拟网卡与挂在docker0上的网络接口是一对veth pair)，一个endpoint只能属于一个网络，只能属于一个Sandbox

3. Network

包含一组endpoint，同一网络的endpoint可以直接通信



![](https://cdn.nlark.com/yuque/0/2023/png/33590654/1693551063069-87447da4-ef3b-4cef-98e0-e9cc1d025a34.png)



### overlay


#### 创建overlay
Docker overlay网络需要一个k-v数据库用于保存网络状态，如Consul



1. 首先在主机上以容器方式运行Consul

docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -boostrap



2. 修改host1, host2的docker daemon配置文件 /etc/systemd/system/docker.service，

在[Service]下增加

--cluster-store=consul://192.168.56.101:8500 # 指定consul的地址

--cluster-advertise=enp0s8:2376 # 告知consul自己的链接地址



3. 在host1, host2重启daemon

systemctl daemon-reload systemctl restart docker.service

host1， host2将自动注册到Consul数据库



4. 在host1中创建overlay网络

docker network create -d overlay ov_net1

-d 指定driver为 overlay



5. 此时在host2上也能看到ov_net1，这是因为创建ovnet1时host1将ovnet1的信息存入了consul，被host2读取到了。



#### 使用overlay网络运行容器
在host1运行容器

docker run -itd --name bbox1 --network ov_net1 busybox



docker exec bbox1 ip r

此时该容器会有两个网络接口

1. overlay网络中的ip地址 - 10.0.0.2
2. 用于访问外网的地址（docker会创建一个bridge网络-docker_gwbridge，为所有连接到overlay网络的容器提供访问外网的能力）- 172.17.0.2



#### overlay网络连通性
在host2中运行容器

docker run -itd --name bbox2 --network ov_net1 busybox



docker exec bbox2 ping -c 2 bbox1

能与bbox1直接通信



#### overlay网络隔离
不同的overlay网络是相互隔离的





### macvlan
macvlan本身是linux内核模块，允许同一个物理网卡配置多个mac地址， 每个地址可以配置自己的IP，本质是网卡虚拟化技术。

优点是性能极好，不需要创建linux bridge。



#### 创建macvlan
docker network create -d macvlan --subnet=172.16.86.0/24 --gateway=172.16.86.1 -o parent=enp0s9 mac_net1

-o parent=enp0s9: parent interface - 物理网卡



跨主机创建容器：

host1: docker run -itd --name bbox1 --ip=172.16.86.10 --network mac_net1

host2: docker run -itd --name bbox2 --ip=172.16.86.11 --network mac_net1



验证：

host2: docker exec bbox2 ping -c 2 bbox1





### flannel
为每个host分配一个subnet，容器从此subnet中分配ip，这些ip可以在host间路由，容器间无需NAT(替换源地址)即可跨主机通信。

每个host会运行一个叫flanneld的agent，其职责就是分配subent。

flannel用etcd（类似consul的k-v db）存放网络配置等信息。





### weave
weave就像一个巨大的交换机（Switch-工作在第二层-数据链路层，根据数据包的目的地 MAC 地址（物理地址）来决定将数据包转发到哪个接口，通常是j。），所有容器都被接入这个交换机，容器可以直接通信。





### calico
为每个容器分配一个IP，每个host都是router（工作在第三层-网络交换层，根据目的 IP 地址来决定将数据包转发到哪个网络），把不同host的容器连接起来。

依赖etcd在不同主机间共享和交换信息。





### 比较各网络方案
pass - 用k8s就完事了





## 3.3容器监控
### docker自带
docker contrainer ps 查看运行的容器

docker container top [container] 查看某个容器运行了哪些进程

docker container stats 显示每个容器各种资源的使用情况

### 
其他工具：

sysdig(提供加强版的top)/weave scope（可视化页面）/cAdivor（可视化页面）/Prometheus



## 3.4日志管理
不用-d直接运行容器的话，stdout和stderr会直接打印在终端上。

使用-d在后台运行容器，可以：

1. docker attach <container id>

但是attach只能看到attach之后的日志，以前的日志不可见

2. 更好的方法是dokcer logs -f <container id>

能够打印出自容器启动以来完整的日志，且-f能持续打印新产生的日志



docker提供了冬种logging driver，默认是json-file，也就是以json格式保存日志。



### ELK
1. Elasticsearch：全文搜索引擎
2. Logstash：读取原始日志，并进行分析和过滤，转发个其他组件进行索引或存储
3. Kibana：基于js的web界面程序，用于可视化Elasticsearch的数据





## 3.5数据管理
有状态容器：需要存储并处理数据，如数据库

无状态容器：不需要保存数据，如web服务器



data volumn可以保存容器的状态，本质是host的目录，可是如果host宕机了，如何恢复容器？

一个好的方案是由专门的storage provider提供volumn，Docker可以从provider那里获取volumn并挂载到容器，即使host挂了，也可以立即从其他可用host启动相同镜像的容器并挂载之前使用的volumn。



每个volumn都有一个driver，默认情况下使用local类型的driver，即从host的本地目录分配空间，如果要支持跨主机的volumn，则需要使用第三方driver，如Rex-Ray。



