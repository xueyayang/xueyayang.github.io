---
layout: default
tag: English
---

如何理解callback--reactor模式的web服务器
========================================

1 问题
====

如何理解callback?

2 解答
====

2.1 从call和back开始
----------

在程序里，`call`是调用，`back`表示“回来，反向”。以两个操作系统api为例，`usleep`与`signal`。

- 程序员希望程序暂停一会，所以会调用`uslepp(10*1000);`，这就是`call`。
- 程序员希望有人按下`Ctrl+C`时，程序不要停止，而是输出一句话“我不会停止的！除非停电。”。	
	- 定义一个`signal_handler()`函数，里面打印"我不会停止的！除非停电"。
	- 作为`signal()	`的参数传入进去。
	- 当`Ctrl+C`的事件发生时，操作系统就不再按照默认的模式，退出程序，而是调用`signal_handler()`。这就是`callback`。
	
简单讲，你(Application)调用操作系统(OS/Server)的API，这叫`call`。
反过来，操作系统/系统（OS/Server）调用你(Application)提供的API，这叫`callback`。

理解callback，分清楚立场非常重要。


2.2 为什么要有callback这个概念
---------

上面的[signal例子][1]已经基本上说明了这种需求：

1. 你希望指定程序的某种形为/指定处理特定情况的方式
2. 但那个程序运行起来后就不受你控制了，如你不知道什么时候用户会按下`Ctrl+C`
3. 所以，你需要**预先**告诉程序，你的处理方式（通常是函数指针）

通常这种情况发生在具有实时性、并且作为服务端的应用上（如库）。如提供图像处理服务的库：

{% highlight cpp %}
//what_do_u_want_to_do_with_result() 就是需要用户指定的函数
while(running){
	frame = capture_frame();
	result = process_frame(frame);
	what_do_u_want_to_do_with_result(result);
}
{% endhighlight %}

当作为Server的这段代码运行起来后，要实时从摄像头抓取帧并处理，得到结果`result`。`while`循环显然不能打断。那么如何将`result`传出去，供application使用？就是个问题。

callback很容易就解决了这个问题：

- 我的处理结果`result`类型是已经知的，假设是`RES_TYPE`
- 我希望你处理完后，返回值最好是整型，我好判断是否成功

所以，我定义如下函数指针：
{% highlight cpp %}
typedef int (*what_do_u_want_to_do_with_result)(RES_TYPE)
{% endhighlight %}

需要使用该库的程序员，拿到API定义后，按照该定义实现一个函数，将其指针作为参数传进去即可。 这时候Server端就可以妥妥地说声：***Don't call me, I'll call back!!***。就是说，当有处理结果时，自己会调用`what_do_u_want_to_do_with_result`接口。


3 总结
====

- 想想正常的call是什么，callback就是反过来
- callback意味着已经分开了｀你我｀两方。想想:

    -自己写while，自己处理中间结果

   	-自己写while，别人处理中间结果
- CPP的话，可以不传函数指针，传个对象进去也可以。当然要求类有固定的处理接口。
- 这几乎就是reactor模式的全部了。

[1]: http://xueyayang.github.io/2014/01/23/%E8%AE%BAtypedef%E7%9A%84%E9%87%8D%E8%A6%81%E6%80%A7.html
