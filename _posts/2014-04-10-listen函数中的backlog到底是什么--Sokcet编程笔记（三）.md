---
layout: default
---

listen()函数中的backlog到底是是什么
===================================

1 问题
====

socket编程，作为Server端，用到listen()函数。根据[man7 page][1]，定义如下：
{% highlight c%}
int listen(int sockfd, int backlog);
{% endhighlight %}

对第二个参数`backlog`的解释是：
>定义了queue的最大长度。哪个queue呢？用来放置'pending
connections'的queue。什么是pending
connections呢？就是那些悬而未决的链结。

什么是“悬而未决”的链结呢？ 

2 方法
====

这里是回答上面问题的一些知识。

2.1 TCP的三次握手
-------------
参考[维基百科][2]，Server与Client的链结分为三步：

1. Client 发送 SYN 请求
2. Server 发送 SYN-ACK 回复，表示“我收到了你的SYN”
3. Client 发送 ACK 回复，表示“我知道你收到了” 

之后就可以愉快的对话了。

2.2 SYN flood攻击
------------

这个也叫'half-open'攻击。

- 心怀恶意的Client做了第一步，发送了SYN
- 老实的Server做了第二步，回送了SYN-ACK
- 狡诈的Client不吭声了……

于是Server端就一直在等待那个SYN-ACK的ACK……同时，分配空间，以存储这些尚未成正果的链结。

心怀恶意的Client又发了一个链结……

心怀恶意的Client又发了一个链结……

心怀恶意的Client又发了一个链结……

Server的queue被塞的满满的，无法接受那些正常的链结。OK，攻击目的达到了。

有没有应对的措施呢？[当然有][3]，但已经不是我关心的范围了。

2.3 backlog的改变
---------------
在man7 page的NOTE里，提到从内核2.2以后放生了变化:
>backlog这个关于TCP
socket的参数，在内核2.2以后，行为发生了变化。现在，它里面放的是完整的（三次握手后）链结，而不是尚未成正果（缺了最后一步ACK）的链结。

已经三次握手完了，还放在queue里干什么？这是因为，这些链结已经建立，但是还没有被`accept`。就是说，操作系统（内核）与请求发起者(Client)建立了关系，还没有交给应用程序。如果此时程序调用:
{% highlight c%}
addr_size = sizeof their_addr;
new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &addr_size);//重点
{% endhighlight %}

操作系统就将这关系(file descriptor)移交给应用程序使用了。

所以，2.2内核以后的backlog，指定的是另外一个queue的长度。这个queue用来存放已经三次握手完毕、但尚未accept的链结。

一个很自然的实验就是：服务端设置backlog为5，开始listen()。但都不accept。——如果第六个client发起链结，会得到什么响应？


3 实验
========

3.1 queue，还是queue
----------------
如果这样调用：
{% highlight c%}
listen(socetfd, 5);
//i will not call accept()
{% endhighlight %}

将queue的长度设置为5，并且不接受任何链结。这时我发起链结请求，6个。会发生什么？

理论上，按照man7 page的描述：

>If a connection request arrives when the queue is full, the client may receive an error with an indication of ECONNREFUSED or, if the underlying protocol supports retansmission, the request may be ignored so that later reattempt at connection succeeds

就是说：
>如果queue满了，你还连，怎么办？可能给你报个错，ECONNREFUSED；也可能不吭声，待会重新连一下，就成功了。

果然一个`may`道尽了不确定性。在Android盒子与Fedora
20上做实验，都没有收到错误。Client只是被阻塞，并没有收到ECONNREFUSED的错误。有网友用[OpenGroup的规范][4]来解释。

3.2 accept()与TCP的三次握手有关系吗？
---------------------------------
accept()显然与TCP的三次握手没有关系。那是操作系统所关心的。accept()只是伸手接管。——调用后，返回一个新的file descriptor，就可以send/recv啦！

4 总结
====
- listen()函数主要用来listen，即监听链结。
- 用backlog来限制链结数，是不可行的。
- Server如何限制链结数，是另外一个话题。

[1]: http://man7.org/linux/man-pages/man2/listen.2.html
[2]: http://en.wikipedia.org/wiki/Transmission_Control_Protocol#Connection_establishment
[3]: http://en.wikipedia.org/wiki/SYN_cookies
[4]: http://pubs.opengroup.org/onlinepubs/009695399/functions/listen.html
