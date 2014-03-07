---
layout: default
---

编译CUnit的Android版本
======================

1 问题
====

用NDK，将CUnit编译Android版本，用于测试在Anroid上跑的代码。

2 方法
====

这实际是一个简单的、标准的NDK编译过程。

2.1 输入什么？——源码
----------------

CUnit的核心源码包括：

>CUnit/include  
>Cunit/source

2.2 NDK build需要什么？
-------------------

### 2.2.1 Android.mk文件 

这里面指定了编译程序通常需要关心的几部分：

-   输入什么？——源码

    -   LOCAL\_C\_INCLUDES

    -   LOCAL\_SRC\_FILES

-   输出什么？——可执行程序，或者库文件（静态/动态）

    -   LOCAL\_MODULE

    -   include $(BUILD\_SHARED\_LIBRARY)

    -   include $(BUILD\_EXECUTABLE)

-   依赖哪些第三方库？——如编译AG**主程序**，显然需要AG**算法库**

    -   LOCAL\_LDLIBS

当然这只是一些简要的概括。
{% highlight Makefile%}
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_ARM_MODE := arm
LOCAL_MODULE := CUnit
LOCAL_C_INCLUDES := ../include/CUnit/
LOCAL_SRC_FILES := ../source/Basic/Basic.c \
			../source/Framework/Util.c \
			../source/Framework/TestDB.c \
			../source/Framework/TestRun.c \
			../source/Framework/CUError.c \
			../source/enhance.c
LOCAL_CXXFLAGS := -D_GLIBCXX_USE_WCHAR_T
LOCAL_LDLIBS := -llog
include $(BUILD_SHARED_LIBRARY)


include $(CLEAR_VARS)
LOCAL_ARM_MODE := arm
LOCAL_MODULE := Test_LibCUnit
LOCAL_C_INCLUDES := ../include
LOCAL_SRC_FILES := HowToUse.cpp
LOCAL_LDLIBS := -llog -L../libs/armeabi-v7a/ -lCUnit
include $(BUILD_EXECUTABLE)
{% endhighlight %}
### 2.2.2 Application.mk文件 

这里给出了一个模板，一般不需要更改。
{% highlight Makefile %}
# Build both ARMv5TE and ARMv7-A machine code.
APP_PLATFORM = android-8

APP_ABI := armeabi-v7a
#APP_ABI := $(ARM_ARCH)

#Sam modify it to release
APP_OPTIM := release
#APP_OPTIM := debug
#APP_OPTIM = $(MY_OPTIM)

APP_CPPFLAGS += -fexceptions
APP_CPPFLAGS += -frtti

#sam modify it from gnustl_static to gnustl_shared
#APP_STL := gnustl_static
#APP_STL := gnustl_shared
APP_STL  := gnustl_shared

#APP_CPPFLAGS += -fno-rtti


#
APP_CPPFLAGS += -Dlinux -fsigned-char
APP_CFLAGS += -fsigned-char
#APP_CPPFLAGS += $(MY_CPPFLAGS) -Dlinux
#STLPORT_FORCE_REBUILD := true
{% endhighlight %}
### 2.2.3 与上面文件对应的目录结构

![image](/images/structure.png)

2.3 开始编译
--------

进入到JNI目录下，输入

    ndk-build

就可以了。输出信息如下：

>Compile arm    : CUnit \<= Basic.c  
>Compile arm    : CUnit \<= Util.c  
>Compile arm    : CUnit \<= TestDB.c  
>Compile arm    : CUnit \<= TestRun.c  
>Compile arm    : CUnit \<= CUError.c  
>Compile arm    : CUnit \<= enhance.c  
>SharedLibrary  : libCUnit.so  
>Install        : libCUnit.so =\> libs/armeabi-v7a/libCUnit.so  
>Compile++ arm    : Test\_LibCUnit \<= HowToUse.cpp  
>Prebuilt       : libgnustl\_shared.so \<= \<NDK\>/sources/cxx-stl/gnu-libstdc++/4.6/libs/armeabi-v7a/  
>Executable     : Test\_LibCUnit  
>Install        : Test\_LibCUnit =\> libs/armeabi-v7a/Test\_LibCUnit  
>Install        : libgnustl\_shared.so =\> libs/armeabi-v7a/libgnustl\_shared.so  

可以看到，生成了***libCUnit.so***库，同时生成一个测试程序***Test\_LibCUnit***。

2.4 上面提到的HowToUse.cpp
----------------------
{% highlight c%}
#include "CUnit/CUnit.h"

int add(int a, int b)
{
	return a+b;
}

TEST(add_test, xxxx)
{
	CU_ASSERT(1 == add(0,1));
}

int main(int argc, char** argv)
{
	RUN_TESTS(argc, argv);
}
{% endhighlight %}
3 总结
====

-   初步测试OK。在实际使用中，看与PC平台有无差异。
