---
layout: default
---

CMakeLists.txt简单例子
======================

1 这篇文章写了什么？
==================
对于常见的`src`,`include`,`3rdLib`结构的工程，给出一个简明的CMakeLists.txt的写法。


2 例子
===================
{% highlight CMake%}
# Version，这是CMake的要求 。方便用户检查自己的CMake够格不。
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

# 必要的变量。方便后面引用代码位置。
PROJECT(Native_Android_Framework)
SET(PROJECT_ROOT_PATH "../")
SET(EXECUTABLE_OUTPUT_PATH "${PROJECT_ROOT_PATH}/bin")
SET(LIBRARY_OUTPUT_PATH "${PROJECT_ROOT_PATH}/lib")

# include path 指定头文件
INCLUDE_DIRECTORIES("${PROJECT_ROOT_PATH}/inc/" "../../../ThirdPartyLibrary/CUnit/include")

# Lib path 指定第三方库的路径
LINK_DIRECTORIES("../../../ThirdPartyLibrary/CUnit/lib" "../lib")

##############################
### 用什么源码，加什么库，编译生成什么？
# src
FILE(GLOB SOURCE_FILE "${PROJECT_ROOT_PATH}/jni/*.cpp")
# target
ADD_LIBRARY(native_android_framework SHARED ${SOURCE_FILE})
# external lib
TARGET_LINK_LIBRARIES(native_android_framework CUnit)
################################


##############################
###用什么源码，加什么库，编译生成什么？
#src
FILE(GLOB SOURCE_TEST "${PROJECT_ROOT_PATH}/test/*.cpp")
#target
ADD_EXECUTABLE(test_main ${SOURCE_TEST})
# external lib
TARGET_LINK_LIBRARIES(test_main CUnit native_android_framework pthread)
################################
{% endhighlight %}

3 补充
====

3.1 如何增加编译选项
-----------------
CMake定义了变量`CMAKE_CXX_FLAGS`
{% highlight CMake %}
SET(CMAKE_CXX_FLAGS "-Wall -Werror")
{% endhighlight %}

3.2 编译Debug版本
------------------
{% highlight bash %}
cmake -DCMAKE_BUILD_TYPE=Debug -G "Unix Makefiles"
{% endhighlight %}

4 总结
======
- 编译不在乎形式。
- CMake真的很方便。
