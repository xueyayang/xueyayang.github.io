---
layout: default
---

从源码编译Clang
====================

问题
====
使用YouCompleteMe的语法补全时，需要使用clang编译器。官方只提供ubuntu的64位二进制包。
所以需要从源码开始编译。

方法
====
理清楚clang与llvm的编译关系，就好搞了。引用官方网页的口径：

>LLVM工程是一个关于编译器和工具链的技术汇总，这些技术已经被模块化，因此可以被很好地重用。...
这货跟虚拟机（Virtual Machine）无关，虽然可以用来开发虚拟机。...
LLVM不是缩写（！！），就是工程的正式名字。（还是全称！虽然有点怪。）

>Clang是一个LLVM原生的编译器，是C/C++/Objective-C。这个编译器致力于提供飞一般的感觉，比如，已经是GCC的3倍啦（生成带debug信息的objective-C）。除了快，另外一个优点是，提供易于理解的编译信息，包括错误与警告。这个可以用来开发一些源码工具。比如blabla...

显然，YouCompleteMe就是一个基于Clang的源码工具——补全。编译Clang，
也离不开LLVM的源码。参考Clang项目的[Getting Started][1]，两步：

下载源码
--------

编译
--------

总结
====
搞清楚关系，找到官方文档。编译无忧。

[1]: http://clang.llvm.org/get_started.html
