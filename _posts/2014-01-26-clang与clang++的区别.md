---
layout: default
---

clang与clang++的区别
====================

问题是什么？
=============
同样的测试程序，用clang++编译正常，用clang编译提示找不到
{% highlight c%}
	undefined reference to `std::cout'  
	undefined reference to `std::basic_ostream<char, std::char_traits<char> >&
	std::operator<< <std::char_traits<char> >(std::basic_ostream<char,
			std::char_traits<char> >&, char const*)'  

{% endhighlight %}
可以看出来，应该是链接时找不到库。哪个库呢？应该是`stdlibc++.so`。

为什么会这样？
=============
`clang++ `实际上是`clang`的一个软链接而已，为什么为会表现不一样？

>znuser@ubuntuvm:~/Downloads/llvm_5_in_1/build-3.3/Release+Asserts/bin$ ls -al|grep clang  
>-rwxr-xr-x 1 znuser znuser 49558324 2014-01-06 23:44 clang  
>lrwxrwxrwx 1 znuser znuser        5 2014-01-06 23:44 clang++ -> clang 

经过网上查找资料，clang程序，对`argv[0]`进行了不一样的处理。具体来讲，当用clang++时，会将输入文件当作c++来处理。

用哪个option?使clang表现的像clang++？
=====================================
`clang --help`，发现有`-x`选项：
> -x <language>           Treat subsequent input files as having type <language>  

但用`clang -x`来编译时，仍然提示上面的错误。

另一步的差别
============
这次用`-v`选项，来查看真正生成的命令有什么区别。
> clang -x test.cpp -v  
> clang++ test.cpp -v

查看输出，发现主要的区别还是在链接的库不一样：
clang++:
>
...  
-lpthread
-lstdc++
-lm
-lgcc_s
-lgcc
-lc
-lgcc_s
-lgcc

clang:
>
...  
-lpthread
-lgcc
--as-needed
-lgcc_s
--no-as-needed
-lc
-lgcc
--as-needed
-lgcc_s
--no-as-needed

可以看到，一个`-lstdc++`,一个`-lgcc`。

总结
====
- 用`clang`主要是为了更友善的提示信息。
- 这篇文章是个中间笔记。讲的很零碎。

