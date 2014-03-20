---
layout: default
---

incomplete-type错误的解决
==========================


1 问题
====
包含某个头文件时，会报`incomplte-type`的错误。我这次是在使用`<linux/videodev2>`时，报这样的错误：

{% highlight bash %}
android-ndk-r8b/platforms/android-8/arch-arm/usr/include/linux/videodev2.h:270:17:
error: field 'timestamp' has incomplete type
{% endhighlight%}

2 解决
====
打开`videodev2.h`文件，找到270行：
{% highlight bash %}
struct timeval timestamp;
{% endhighlight %}

可以看到是声明了一个结构体，现在抱怨这个结构体不完整。说明应该是没有找到
头文件，单单“前置声明”一下，对编译器来说是不满足的。必须要提供其完整的定
义，才能继续编译。——比如，分配多少空间这样的问题。

经过google搜索，知道这个结构体定义在`<sys/time.h>`中。把这个头文件放到`<linux/videodev2>`
之前，再编译，通过。

3 补充说明
========
- 问题是在我调整头文件顺序后出现的。推测其他头文件也有对`<sys/time.h>`的引用。
- 有[网友认为][1]头文件互相包含也会导致这样的问题。暂时没想通。再遇到这样的问题再研究吧。


4 总结
====
- 知道的越多，碰到的问题也越多。——程序界的`人生识字忧患始`啊。
- May the source be with you!


[1]: http://stackoverflow.com/questions/3999400/error-field-has-an-incomplete-type
