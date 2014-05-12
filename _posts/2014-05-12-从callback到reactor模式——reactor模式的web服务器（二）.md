---
layout: default
tag: design-pattern, c++
---

从callback到reactor模式——reactor模式的web服务器
===============================================

1 问题
====

在[理解callback][1]的基础上，结合[reactor模式的文档][2]实现一个基于web模式的服务器。

2 解答
====

2.1 从callback机制到reactor模式
-------------------------------

callback就是reactor模式的全部，核心在于“指定对某（类）事件的响应/处理方式”。即，如何`react`。这就是`reactor`的含义。

所以从callback到reactor模式，没有额外的需要理解的东西。

2.2 从reactor模式到基于reactor模式的web服务器
--------------------

一个web服务器要做什么？在这里简化成两方面的需求：

- 对于发起连接请求的Client进行响应，即，建立`Server<-->Client`的连接。
- 为已经建立连接的Client提供指定服务，如，读/写数据。当然，用上传与下载更通俗。


2.3 看看最终服务器使用的形式
------------------------

这里直接给出[文档][2]里的示例:

{% highlight cpp %}
int main (void)
{
	...
	Logging_Acceptor la (server_addr);
	for (;;)
		Initiation_Dispatcher::instance()->handle_events();
	...
}
{% endhighlight %}


2.4 从函数指针到对象指针
---------------------

callback里，作为服务端，给出一个函数指针来约束`库/服务`的使用者就如何定义callback函数，即“接口”。函数指针是很'C
style'的东西。

基于reactor模式的服务器，既然在谈设计模式，从`C Style`换到`C++ Style`、引入面向对象的概念也很自然的。
函数指针本质是一个“接口”。用C++的思维考虑问题，interface，自然就是一个纯虚类，里面定义了需要实现的函数。接下来的事情就更自然了：

- callback的概念里，库的使用者需要根据函数指针的定义实现一个函数，将指针作为参数传入，以供事件发生时被调用。
- reactor模式里，库的使用者需要继承纯虚类(接口)，实现里面的接口，以供事件发生时被调用。

取文档里的例子进行说明：

{% highlight cpp %}
class Event_Handler
{
public:
	// Hook methods that are called back by
	// the Initiation_Dispatcher to handle
	// particular types of events.
	virtual int handle_accept (void) = 0;
	virtual int handle_input (void) = 0;
	virtual int handle_output (void) = 0;
	virtual int handle_timeout (void) = 0;
	virtual int handle_close (void) = 0;
	// Hook method that returns the underlying
	// I/O Handle.
	virtual Handle get_handle (void) const = 0;
};
{% endhighlight %}

2.5 如何传递Event_Handler
-----------------------------------

callback使用中，以`signal()`函数为例，程序员定义`signal_handler`后，需要将函数指针作为参数传入。

reactor模式里，提供一个接口，`register_handler(Event_Handler*)`，接收一个对象指针。提供register_handler()接口的，就是上面的提到的
`Initiation_Dispatcher`类。

2.6 Initiation_Dispatcher类做了什么？
--------------------------------

最终对外的接口是通过`Initiation_Dispatcher`类来暴露的，可见是个连接Server/Client的关键类。

###2.6.1  增加删除event_handler
需要提供:

- register\_handler(Event\_Handler*, Event\_Type)
- remove\_handler(Event\_Handler*, Event\_Type)

接口。

###2.6.2  存储<handle, event_handler>的对应关系

Server与Client是通过socket建立连接的,在*nix的概念里，建立的socket,也是一种"file
descriptor"，如同普通文件一样进行读写操作。具体参考[Beej's Guide to Network Programming][3].
Dispatcher，顾名思义，需要为每个*file descriptor*指定对应的`event handler`。

这是一个典型的<key, value>的存储需求。key就是**file descriptor**，value就是与之对应的`event_handler`对象指针。选用unorder\_map来实现（需要开启c++11支持）。

###2.6.3  开启主Loop

如上面展示的最后服务器的使用形式,需要实现`handle_events()`接口。这个接口里面，需要进行`poll`或者`select`机制，来监听I/O.


2.7 建立连接与读写数据的分离
-------------------------
文档里提到，将建立连接与读写数据分离开来，即从`Event_Handler`类生成了两个子类：

- Logging\_Acceptor: 专门用来处理新的连接请求
- EventHandler\_Process: 专门用来处理对已经建立的连接的***读写数据请求***。


2.8 注册Event_Handler的时机
-----------------------

上面服务器的最终形式里，并没有明显地调用`register_handler()`接口，那是如何注册Event\_Handler呢？

1. Logging\_Acceptor在构造函数里完成了对`Accept`事件的接手。
2. 当Logging\_Acceptor建立新的连接时，得到一个新的*file descriptor*，此时，为该`fd`注册对应的`EventHandler_Process`。

这样，两个register的过程，就被巧妙的隐藏起来了。

2.9 单例的必要性
------------

细心地话，会注意到，Logging\_Acceptor在构造函数里调用`register_handler()`时，尚无`Initiation_Dispatcher`的对象被构造出来。

如何在没有对象的情况下调用其函数呢？——显然需要用到静态成员变量。

如何保证Initiation\_Dispatcher只维护一份数据，并且所有的Event\_Handler都被注册到了同个对象，
并且受同个对象来管理呢？——显然要用到[单例模式][2]。

3 总结
====

- 基于Reactor模式的服务器，其实就是对callback机制的使用。
- 好处：降低了多线程的编程复杂性。
- 据文档讲，提高了效率，但为什么，还没想通。因为尚未进行大数据测试，所以也没有数据支撑。
- 理解的还不够。因为文章写的还不够简单、易懂。


[1]: http://xueyayang.github.io/2014/05/12/%E5%A6%82%E4%BD%95%E7%90%86%E8%A7%A3callback%E2%80%94%E2%80%94reactor%E6%A8%A1%E5%BC%8F%E7%9A%84web%E6%9C%8D%E5%8A%A1%E5%99%A8%28%E4%B8%80%29.html
[2]: http://www.cs.wustl.edu/~schmidt/PDF/reactor-siemens.pdf
[3]: http://beej.us/guide/bgnet/
[4]: http://xueyayang.github.io/2014/04/24/%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8Fsingleton%E7%9A%84C%2B%2B%E5%AE%9E%E7%8E%B0.html
