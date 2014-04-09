---
layout: default
---

处理SIGPIPE信号
===============

1 问题
====
背景：

编写socket程序，Client连上Server后，Server端就开始向Client发送数据。直到
链结断开。

问题：

Client端小程序如果用`Ctrl+C`终止，有可能导致Server端也挂掉。——没有任何提示！

2 方法
====

2.1 原因
----

经过搜索，这是对`SIGPIPE`信号的默认处理机制造成的：

- 客户端`Ctrl+C`强行终止了程序，导致socket关闭。
- 此时服务端正在进行`send`操作，但已经发生了`pipe broken`，发出信号`SIGPIPE`。
- 默认的处理机制，就是终止程序。

参考资料见[这里][1]。

2.2 解决
----
知道原因就好办了：为SIGPIPE设置新的handler。
{% highlight c%}
void pipe_broken_handler(int arg)
{
	printf("get pipe broken signal!\n");
}

int main()
{
	signal(SIGPIPE,pipe_broken_handler);
	...
}
{% endhighlight %}

这样在Client意外关闭socket时，就不会导致Server端挂掉了。

2.3 附
----
send程序为了保证一次发送数据完整，使用了while循环。
{% highlight c%}
int send_long_data(int socket_fd,const char *data_ptr, int size_to_send)
{
	int pos = 0;
	int sent_len = 0;	
	while(pos < size_to_send) 
	{
		sent_len = send(socket_fd,data_ptr + pos,size_to_send - pos,0);
		if (sent_len < 0)
		{
			perror("send error!\n");//perror很关键
			printf("sent_len < 0. send error!\n");
			return -1;
		}
		if(sent_len == 0)
		{
			printf("sent_len is 0. Peer performs orderly shutdown!\n");
			return -2;
		}
		pos += sent_len;
	}
	return 0;
}
{% endhighlight %}

注意其中的perror。会将`broken pipe`的异常报出来。

3 总结
====

- 处理异常很重要。
- 如何获知异常是个问题。——要学会使用perror()。


[1]: http://stackoverflow.com/questions/6824265/sigpipe-broken-pipe

