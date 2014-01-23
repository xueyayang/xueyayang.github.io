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
{% highlight sh%}
#3 Version，这是CMake的要求 。方便用户检查自己的CMake够格不。
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

#4 必要的变量。方便后面引用代码位置。
PROJECT(Native_Android_Framework)
SET(PROJECT_ROOT_PATH "../")
SET(EXECUTABLE_OUTPUT_PATH "${PROJECT_ROOT_PATH}/bin")
SET(LIBRARY_OUTPUT_PATH "${PROJECT_ROOT_PATH}/lib")

#5 include path 指定头文件
INCLUDE_DIRECTORIES("${PROJECT_ROOT_PATH}/inc/" "../../../ThirdPartyLibrary/CUnit/include")

#6 Lib path 指定第三方库的路径
LINK_DIRECTORIES("../../../ThirdPartyLibrary/CUnit/lib" "../lib")

###6.0.1 ###########################
###6.0.2 用什么源码，加什么库，编译生成什么？
#7 src
FILE(GLOB SOURCE_FILE "${PROJECT_ROOT_PATH}/jni/*.cpp")
#8 target
ADD_LIBRARY(native_android_framework SHARED ${SOURCE_FILE})
#9 external lib
TARGET_LINK_LIBRARIES(native_android_framework CUnit)
###9.0.1 #############################


###9.0.2 ###########################
###9.0.3 用什么源码，加什么库，编译生成什么？
#10 src
FILE(GLOB SOURCE_TEST "${PROJECT_ROOT_PATH}/test/*.cpp")
#11 target
ADD_EXECUTABLE(test_main ${SOURCE_TEST})
#12 external lib
TARGET_LINK_LIBRARIES(test_main CUnit native_android_framework pthread)
###12.0.1 #############################
{% endhighlight %}

3 总结
======
- 编译不在乎形式。
- CMake真的很方便。
