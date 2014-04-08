---
layout: default
---

编译YCM模块
===========

1 问题
====
这是安装VIM补全插件YCM(You Complete Me)中的一部分，编译YCM核心库。

2 方法
====

依据的是[项目主页][1]上的文档。对其中碰到的问题进行记录。

2.1 下载YCM源码
--------
>git clone https://github.com/Valloric/YouCompleteMe.git

2.2 下载Submodule
--------------
>git submodule update --init --recursive

2.3 下载clang编译器
---------------
到LLVM主页，下载官方编译好的[clang编译器][2]。clang才是YCM补全的核心。
解压。

>tar -xzvf clang+llvm-3.3-amd64-Ubuntu-10.04.4.tar.gz


2.4 编译YCM工程
---------------
###2.4.1  用CMake生成Makefile
YCM的Build采用CMake。ubuntu10.04，经测试，需要2.82.12以上版本的。不然会报诡异的错误。如果你的LINUX发行版本库里没有最新的，需要手动[编译CMake][3]。

{% highlight bash%}
cd ~/.vim/bundle/YouCompleteMe
mkdir ycm_build
cd ycm_build
cmake -G "Unix Makefiles" -DPATH_TO_LLVM_ROOT=~/ycm_temp/llvm_root_dir . ~/.vim/bundle/YouCompleteMe/cpp
{% endhighlight %}

2.5 报错
--------
>Linking CXX shared library /home/znuser/.vim/bundle/YouCompleteMe/python/ycm_core.so  
>/home/znuser/Downloads/clang+llvm-3.3-amd64-Ubuntu-10.04.4/lib/libclang.so: could not read symbols: File in wrong format  
>collect2: ld returned 1 exit status  
>make\[2\]: *** [/home/znuser/.vim/bundle/YouCompleteMe/python/ycm_core.so] Error 1  
>make\[1\]: *** [ycm/CMakeFiles/ycm_core.dir/all] Error 2  
>make: *** [all] Error 2  

这个重点是`libclang.so: ould not read symbols: File in wrong
format`，显然是动态库错误。仔细想了想，下载的二进制包是`Clang Binaries for
Ubuntu-10.04.4 on AMD64`，我的机子是32位的。所以需要[手动编译LLVM+Clang][4]。

然后重复以上步骤，OK。

2.6 总结
========
编译需要一台好机子。



[1]: https://github.com/Valloric/YouCompleteMe
[2]: http://llvm.org/releases/download.html
[3]: http://none 
[4]: http://http://xueyayang.github.io/2014/04/08/Compile-Clang-From-Source.html

