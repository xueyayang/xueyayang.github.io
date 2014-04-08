---
layout: default
---

getaddrinfo()接口与struct addrinfo
====================

1 问题
====
理解getaddrinfo()接口。结合struct addrinfo来进行。

2 介绍
====

根据著名教程[beej's guide][1]，getaddrinfo() + addrinfo是一对更现代、方便的组合，用于取代gethostbyname() + sockaddr_in。

不仅可以做DNS lookups，也可以做services name lookups。二合一。

思路为，传入服务器的地址和端口，外加一个addrinfo（用于描述服务器），就可以得到
一个更具体的addrinfo。这个结果可以在创建socket时使用。

2.1 getaddrinfo()的定义
-------------------
{% highlight c%}
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

int getaddrinfo(const char *node,     // e.g. "www.example.com" or IP
                const char *service,  // e.g. "http" or port number
                const struct addrinfo *hints, //指定一些基本值
                struct addrinfo **res);//得到链表
{% endhighlight %}

2.2 struct addrinfo定义
-------------------
定义于netdb.h。[这份文档][2]解释了各成员变量，关键字高亮，看着很舒服。
MSDN的文档[在这里][3]。
{% highlight c %}
struct addrinfo {
    int              ai_flags;
    int              ai_family;// ipv4,ipv6...
    int              ai_socktype;//SOCK_STREAM SOCK_DGRAM
    int              ai_protocol;//TCP UDP...
    socklen_t        ai_addrlen;
    struct sockaddr *ai_addr;
    char            *ai_canonname;
    struct addrinfo *ai_next;
};
{% endhighlight %}

- ai_flags常用的值是`AI_PASSIVE`。与`node`为NULL作为组合，用来做服务端。
	- `passive`就是被动、被动接入的意思。（学好英语很有必要啊，可以顾名思义。）
- ai_family常用的值是`AF_UNSPEC`，表示ipv4，ipv6皆可。

2.3 一个使用例子
-------------
原封不动，来自beej的教程。
{% highlight c%}
...
#define PORT "3490"
struct addrinfo hints;
//Step1. 指定选项
memset(&hints, 0, sizeof hints);
hints.ai_family = AF_UNSPEC;
hints.ai_socktype = SOCK_STREAM;
hints.ai_flags = AI_PASSIVE; // use my IP

//Step2. 调用getaddrinfo
if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
	fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
	return 1;
}

//Step3. Use the result
// loop through all the results and bind to the first we can
for(p = servinfo; p != NULL; p = p->ai_next) {
	if ((sockfd = socket(p->ai_family, p->ai_socktype,
			p->ai_protocol)) == -1) {
		perror("server: socket");
		continue;
	}

	if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
			sizeof(int)) == -1) {
		perror("setsockopt");
		exit(1);
	}

	if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
		close(sockfd);
		perror("server: bind");
		continue;
	}

	break;
}

if (p == NULL)  {
	fprintf(stderr, "server: failed to bind\n");
	return 2;//不需要freeaddrinfo()
}

//Step4. Be tidy。释放得到的serverinfo。
//注意该语句位置在return 之后
//说明，只有成功时，才会分配内存（需要释放）
freeaddrinfo(servinfo); // all done with this structure
{% endhighlight %}

2.4 创建socket需要？
-----------------
getaddrinfo()接口返回的东西，正是创建socket所需要的。参考socket的接口：
{% highlight c%}
int socket(int domain, //即communication domain，用ai_family
		int type,//socket type, 用ai_socktype
		int protocol//通讯协议，用ai_protocol
		)
{% endhighlight %}

2.5 其他
----
MSDN上，[Server][4]与[Client][5]的例子。

3 总结
=====
getaddrinfo()是socket编程的万里长征第一步。要求懂些网络知识。

[1]: http://beej.us/guide/bgnet/output/html/singlepage/bgnet.html#getaddrinfo
[2]: http://man7.org/linux/man-pages/man3/getaddrinfo.3.html
[3]: http://msdn.microsoft.com/en-us/library/windows/desktop/ms737530(v=vs.85).aspx
[4]: http://msdn.microsoft.com/en-us/library/windows/desktop/ms737593(v=vs.85).aspx
[5]: http://msdn.microsoft.com/en-us/library/windows/desktop/ms737591(v=vs.85).aspx
