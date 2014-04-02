---
layout: default
---

编写JNI代码-Android程序JNI编程（二）
===============


问题
====
[生成JNI接口][1]后，如何编写JNI代码？


方法
====

包含<android/log.h>
----
这样就可以输出日志了。使用`__android_log_write`接口。为了方便定成宏。

{% highlight c%}
#define TAG "ERIC_INFO"
#define LOG_ERIC __android_log_write

LOG_ERIC(ANDROID_LOG_INFO,TAG,"native_process_preview");

{% endhighlight%}

总结
====
- 逐渐补充中……

[1]: 
