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

[1]: http://xueyayang.github.io/2014/01/15/%E7%94%9F%E6%88%90JNI%E6%8E%A5%E5%8F%A3-Android%E7%A8%8B%E5%BA%8FJNI%E7%BC%96%E7%A8%8B%EF%BC%88%E4%B8%80%EF%BC%89.html
