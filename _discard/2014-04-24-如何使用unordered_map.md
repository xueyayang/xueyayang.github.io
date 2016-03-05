---
layout: default
---

如何使用unordered_map
=====================

1 问题
====
C++中使用hash表，存储`<key,value>`这样的数据。

2 方法
====

2.1 unordered_map
-------------
C++11中加入了这种数据。本质就是hash表。

2.2 初始化
------
- 声明为类成员，不在初始化列表/构造函数里做处理。会调用`默认构造函数`。
- `默认构造函数`会处理成一个空的map。
更详细的使用，参见[官方文档][1]。

{% highlight cpp %}
#include <unordered_map>
class InitiationDispatcher
{
	...
	// hash-table, store the <key,value>
	// key:   handle
	// value: the handler obj
	std::unordered_map<int, EventHandler*> fd_handler_table_;
};
{% endhighlight %}

2.3 加入新元素
-----------

- emplace接口
- 用`std::make_pir()`将<key,value>加工成可接受的数据。

{% highlight cpp %}
int InitiationDispatcher::register_handler(EventHandler *eh, Event_Type et)
{
	...
	fd_handler_table_.emplace(std::make_pair(fd,eh));	
	...
}
{% endhighlight %}

2.4 删除元素
--------
- erase即口
- 传入<key,value>中的`key`用来索引

{% highlight cpp %}
int InitiationDispatcher::remove_handler(EventHandler *eh, Event_Type et)
{
	...
	fd_handler_table_.erase(fd);
	...
}
{% endhighlight %}

2.5 编译
------
CMake GCC，需要加上`-std=c++11`这个flag.
{% highlight cmake %}
SET(CMAKE_CXX_FLAGS "-Wall -Werror -std=c++11")
{% endhighlight %}

3 总结
====
- 只是临时简单使用。不考虑复杂场景、效率、容量、hash函数等。
- 以后自己实现个hash表。

[1]: http://en.cppreference.com/w/cpp/container/unordered_map/unordered_map

