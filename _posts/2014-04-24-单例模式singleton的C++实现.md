---
layout: default
---

单例模式的C++实现
==================

1 问题
====
实现单例模式。保证一个类只能有一个实例（instance）存在。

使用场景：如在实现Reactor模式里的Initiation Dispatcher，就需要只有一个。如果多于一个，发送消息就会出问题。



2 实现
====

2.1 思路
----
- 主要用到静态函数与静态方法。
- 为了防止用户调用构造函数，new/声明，形成新的对象。需要将构造函数声明为protected的。

2.2 代码
----
{% highlight cpp %}
class InitiationDispatcher
{
protected://the singleton necessary
	InitiationDispatcher();

public:
	~InitiationDispatcher();

	static InitiationDispatcher* instance();

	static InitiationDispatcher* single_instance_;
}

//complete
InitiationDispatcher* InitiationDispatcher::instance()
{
	if(NULL != single_instance_)
	{
		return single_instance_;
	}
	else
	{
		single_instance_ = new InitiationDispatcher();
		return single_instance_;
	}
}
{% endhighlight %}

3 总结
=====
- 不知道是因为平时对这个概念已经有了解还是怎样，觉得好简单的样子。


