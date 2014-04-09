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

2.6 手动编译LLVM+Clang的问题
-----------------------------
作者的CMake假设使用的是预先编译好的clang。如果手动编译，会报头文件错误：
{% highlight bash %}
In file included from /home/eric/.vim/bundle/YouCompleteMe/cpp/ycm/CandidateRepository.cpp:28:0:
/home/eric/.vim/bundle/YouCompleteMe/cpp/ycm/ClangCompleter/CompletionData.h:23:27: fatal error: clang-c/Index.h: No such file or directory
 #include <clang-c/Index.h>
                           ^
compilation terminated.
{% endhighlight %}
这是因为手动编译时，目录结构与官方发布的二进制包里的目录不一样。

打开`CMakeLists.txt`，找到设置头文件与库的路径的地方，修改即可：
{% highlight Makefile %}
if ( PATH_TO_LLVM_ROOT )
	set( CLANG_INCLUDES_DIR "${PATH_TO_LLVM_ROOT}/include" "${PATH_TO_LLVM_ROOT}/llvm/tools/clang/include/" )

...

else()
  set( LIBCLANG_SEARCH_PATH "${PATH_TO_LLVM_ROOT}/Debug+Asserts/lib" )
{% endhighlight %}

查找时，`PATH_TO_LLVM_ROOT`是关键。重新编译。

3 总结
========
编译需要一台好机子。



[1]: https://github.com/Valloric/YouCompleteMe
[2]: http://llvm.org/releases/download.html
[3]: http://none 
[4]: http://http://xueyayang.github.io/2014/04/08/Compile-Clang-From-Source.html

