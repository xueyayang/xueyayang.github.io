---
layout: default
---

How To Use libutils.so
=======================


1 问题
====

想要使用Android系统自带的Looper机制。所以需要使用libutils.so库。

> android/frameworks/native/include/utils/Looper.h

2 方法
====

2.1 源程序
------

新建jni文件夹，在下面

{% highlight c %}
// File: use\_looper.cpp

#include "utils/Looper.h"

int main()
{
	printf("hello~\n");
	android::Looper *looper = new android::Looper(true);
}
{% endhighlight %}

2.2 准备所需的头文件
----------------

根据层层依赖关系，所用到的头文件将会非常多。所以，

1.  在jni的同级目录，先建一个`utils_inc`目录。

2.  将Looper.h所在的整个`utils`文件夹拷贝进去。

2.3 准备所需的库
------------

根据层层依赖的关系，所用到的so文件非常多，所以，

1.  在`jni`的同级目录，先建一个`pre_built_lib`目录

2.  找到libutils.so文件

    1.  从编译好的源码包里找：`find . -name libutils.so`

    2.  从目标设备上下载：`adb pull /system/lib/libutils.so`

3.  将libutils.so拷贝进去

2.4 编写mk文件如下
--------------

Android.mk文件的编写，可以参考[Android.mk简易入门][1].

{% highlight Makefile %}
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := use_Looper
LOCAL_C_INCLUDES := ../utils_inc
LOCAL_SRC_FILES := ./use_looper.cpp
LOCAL_LDLIBS := -L../pre_built_lib -lutils
include $(BUILD_EXECUTABLE)
{% endhighlight %}

3 解决几个错误
============

3.1 找不到头文件的错误
------------------

按照以上的配置，直接编译，会提示：

{% highlight bash %}
Compile++ thumb : use_Looper <= use_looper.cpp
In file included from ../utils_inc/utils/AndroidThreads.h:27:0,
from ../utils_inc/utils/threads.h:28,
from ../utils_inc/utils/Looper.h:20,
from /home/znuser/eric/test_looper/jni/./use_looper.cpp:1:
../utils_inc/utils/ThreadDefs.h:22:29: fatal error: system/graphics.h: No such file or directory
compilation terminated.
make: *** [/home/znuser/eric/test_looper/obj/local/armeabi/objs/use_Looper/./use_looper.o] Error 1
{% endhighlight %}

显然是缺少头文件的错误。因为Looper.h又依赖了threads.h，又依赖了……。最终靠到了`system/graphics.h`，却发现找不到。解决方法：

1.  在源码包里寻找头文件。`find . -name graphics.h`

2.  将其所在的文件夹system整个拷贝进`utils_inc`。

重复这个过程，解决所有的头文件缺少的问题。

3.2 找不到依赖库的问题
------------------

集齐所有的头文件后，错误类型就变了。会提示：
{% highlight bash %}
Compile++ thumb : use_Looper <= use_looper.cpp
StaticLibrary : libstdc++.a
Executable : use_Looper
/home/znuser/android-ndk-r8b/toolchains/arm-linux-androideabi-4.6/prebuilt/linux-x86/bin/../lib/gcc/arm-linux-androideabi/4.6.x-google/../../../../arm-linux-androideabi/bin/ld: warning: liblog.so, needed by ../pre_built_lib/libutils.so, not found (try using -rpath or -rpath-link)
/home/znuser/android-ndk-r8b/toolchains/arm-linux-androideabi-4.6/prebuilt/linux-x86/bin/../lib/gcc/arm-linux-androideabi/4.6.x-google/../../../../arm-linux-androideabi/bin/ld: warning: libcutils.so, needed by ../pre_built_lib/libutils.so, not found (try using -rpath or -rpath-link)
/home/znuser/android-ndk-r8b/toolchains/arm-linux-androideabi-4.6/prebuilt/linux-x86/bin/../lib/gcc/arm-linux-androideabi/4.6.x-google/../../../../arm-linux-androideabi/bin/ld: warning: libcorkscrew.so, needed by ../pre_built_lib/libutils.so, not found (try using -rpath or -rpath-link)
/home/znuser/android-ndk-r8b/toolchains/arm-linux-androideabi-4.6/prebuilt/linux-x86/bin/../lib/gcc/arm-linux-androideabi/4.6.x-google/../../../../arm-linux-androideabi/bin/ld: warning: libz.so, needed by ../pre_built_lib/libutils.so, not found (try using -rpath or -rpath-link)
{% endhighlight %}
显然是缺少依赖库的问题。因为`libutils.so`依赖了其它库。 解决方法：

-   从目标盒子上下载这些库 `adb pull /system/lib/xxx.so`

-   修改Andriod.mk文件，添加这些库

        LOCAL_LDLIBS := -L../pre_built_lib -lutils -lz -llog -lcorkscrew -lcutils \
            -lgccdemangle

3.3 奇怪的错误
----------

集齐所有的依赖库后，还（可能）会报如下的错误：
{% highlight bash %}
Compile++ thumb  : use_Looper <= use_looper.cpp
Executable     : use_Looper
../pre_built_lib/libcutils.so: undefined reference to ‘__strcpy_chk’
../pre_built_lib/libutils.so: undefined reference to ‘__strcat_chk’
../pre_built_lib/libcutils.so: undefined reference to ‘ioprio_set’
../pre_built_lib/libcorkscrew.so: undefined reference to ‘dladdr’
../pre_built_lib/libutils.so: undefined reference to ‘__strlen_chk’
../pre_built_lib/libcutils.so: undefined reference to ‘ioprio_get’
../pre_built_lib/libcorkscrew.so: undefined reference to ‘tgkill’
../pre_built_lib/libutils.so: undefined reference to ‘pread64’
../pre_built_lib/libcutils.so: undefined reference to ‘__system_property_set’
../pre_built_lib/libcutils.so: undefined reference to ‘__memmove_chk’
../pre_built_lib/libcutils.so: undefined reference to ‘__memcpy_chk’
../pre_built_lib/libcutils.so: undefined reference to ‘__strncpy_chk’
../pre_built_lib/libutils.so: undefined reference to ‘__sprintf_chk’
../pre_built_lib/libutils.so: undefined reference to ‘__pthread_gettid’
collect2: ld returned 1 exit status
make: *** [/home/znuser/eric/test_looper/obj/local/armeabi/use_Looper] Error 1
{% endhighlight %}

这个是因为目标盒子上的`libc.so`与本地ndk目录下的`libc.so`不一致。解决办法：

1.  指定要使用ndk目录下哪个libc.so。因为ndk目录下有几个不同版本的libc.so
{% highlight bash %}
znuser@znpc: find /home/znuser/android-ndk-r8b/ -name "libc.so"

/home/znuser/android-ndk-r8b/platforms/android-14/arch-mips/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-14/arch-arm/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-14/arch-x86/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-8/arch-arm/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-5/arch-arm/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-3/arch-arm/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-9/arch-mips/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-9/arch-arm/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-9/arch-x86/usr/lib/libc.so
/home/znuser/android-ndk-r8b/platforms/android-4/arch-arm/usr/lib/libc.so
{% endhighlight %}

2.  编写Application.mk文件，这里指定android-8
{% highlight Makefile %}
#4  File: Application.mk
APP_PLATFORM = android-8
{% endhighlight %}

3.  替换android-8下的libc.so
{% highlight bash %}
cd /home/znuser/android-ndk-r8b/platforms/android-8/arch-arm/usr/lib
mv libc.so libc.so.bak
adb pull /system/lib/libc.so
{% endhighlight %}

5 编译&运行
=========

此时可以编译通过。

6 总结
====

1.  这是一个典型的交叉编译的过程。编译机上并无目标机上的库与头文件，所以需要从目标机统统pull下来。
2.  编译与链接程序，就是找头文件与库(中包含的符号symbol)的过程。
2.  ndk下暴露的接口及`libutils.so`库，只是Android源码包里的一个子集。
3.  这种方法如果没有源码包，比较难实行。不推荐。
4.  这里聚焦于如何使用系统的so库。Looper的使用参见[另一篇文章][2]。


[1]: http://xueyayang.github.io/2014/03/07/Android.mk%E4%B8%AD%E7%9A%84%E5%87%A0%E4%B8%AA%E5%8F%98%E9%87%8F.html
[2]: http://
