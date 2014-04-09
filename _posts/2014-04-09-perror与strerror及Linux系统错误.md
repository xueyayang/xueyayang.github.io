---
layout: default
---

perror与strerror及Linux的错误机制
=================================

1 问题
====
学会使用perror与strerror，了解Linux的错误机制。

2 方法
====

2.1 Linux的错误机制
---------------

调用系统函数发生错误时，通常只返回-1。程序员没办法知道发生了什么错误。实际上，系统做的要更多:

- 预先定义一个错误列表const char *sys_errlist[]
- 发生错误时，设置全局变量errno的值，表示发生了什么错误。

这样，通过查表sys_errlist[errno]，就能访问到错误信息。

2.2 perror
-----------------
参考[Linux Man Page][1]，perror的摘要：
{% highlight c%}
//perror
#include <stdio.h>
void perror(const char *s);

//errno
#include <errno.h>
const char *sys_errlist[];
int sys_nerr;
int errno;
{% endhighlight %}

这个函数用来将最近一次发生的错误打印出来。手册建议：

>常见用法是， 将perror(const char *s)的参数，写上错误所处的函数名。这样打印出来的错误信息更易于阅读。

> ...

>虽然系统也是通过errno，去全局变量sys_errlist[]中索引错误信息。但是建议你不要这么做啊。因为很可能新的错误值，还没有加到sys_errlist[]中去。

使用例子与好处参见[捕获SIGPIPE][2]。如果不用这个函数，简单的手动打印错误信息，如`printf("here error")`，会忽略一些系统错误。——程序结束了，但无任何提示。

2.3 strerror()
-----------
如果你不想使用perror，想自己加工一下错误信息。但是又不建议直接访问
sys_errlist[]，怎么办？

strerror(int errno)函数来帮你。传入一个错误号，返回一个指针，指向错误信息。

来自[beej guide][3]的例子：
{% highlight c%}
int s;

s = socket(PF_INET, SOCK_STREAM, 0);

if (s == -1) { // some error has occurred
    // prints "socket error: " + the error message:
    perror("socket error");
}

// similarly:
if (listen(s, 10) == -1) {
    // this prints "an error: " + the error message from errno:
    printf("an error: %s\n", strerror(errno));
}
{% endhighlight %}

3 总结
====
- 熟悉机制，利用机制。

[1]: http://man7.org/linux/man-pages/man3/perror.3.html
[2]: http://xueyayang.github.io/2014/04/09/%E5%A4%84%E7%90%86SIGPIPE%E4%BF%A1%E5%8F%B7-Socket%E7%BC%96%E7%A8%8B%E7%AC%94%E8%AE%B0%28%E4%BA%8C%29.html
[3]: http://www.beej.us/guide/bgnet/output/html/multipage/perrorman.html


